import enum
import os
from io import IOBase
from typing import BinaryIO
from tempfile import NamedTemporaryFile

import ffmpeg
import numpy as np

# aliasing to avoid confusion

from giford.frame.frame_batch import FrameBatch
from giford.frame.raw_data import RawDataFrame
from giford.image.abstract_image import AbstractImage


class MultiImageFormat(enum.Enum):
    """
    currently supported multi image formats
    using the same name as PIL/pillow.format
    """

    UNKNOWN = 0
    GIF = 1


class MultiImage(AbstractImage):
    DEFAULT_FRAMERATE: int = 15
    DEFAULT_FORMAT: MultiImageFormat = MultiImageFormat.GIF

    def __init__(self) -> None:
        super().__init__()

        self.raw_data_frames: list[RawDataFrame] = []
        self.format = MultiImageFormat.UNKNOWN

    def load(self, in_file: str | BinaryIO) -> None:
        width: int
        height: int
        frames: int
        if isinstance(in_file, str):
            input_args = {"filename": in_file}
            # TODO - what happens if multiple streams? can we support multiple files???
            # for now assuming one input stream
            vstreams = ffmpeg.probe(in_file, select_streams="v")
            video_stream = vstreams["streams"][0]
            width = video_stream["width"]
            height = video_stream["height"]
            frames = video_stream["nb_frames"]
        elif isinstance(in_file, IOBase):
            # TODO - temp removing probe as a variable for now
            width = 449
            height = 524
            frames = 25

            # TODO - buffered write util function
            BUFFER_SIZE = 1024 * 4  # reasonable block/cluster size
            # something is weird with gif_pipe
            # it correctly interprets as a gif, but doesn't have a duration or length
            # it only picks up one frame worth of data
            # googling was not productive
            # searcing ffmpeg through github was not productive
            # need to dig deeper, but may give up on this for now
            input_args = {
                "filename": "pipe:",
                "format": "gif_pipe",
                # applying codec appeared to cause more problems
                # "codec": "rawvideo",
                # "pix_fmt": "rgb24",
                # "s": f"{width}x{height}",
                # 'frames': frames, # cannot specify frames on input for obvious reasons
            }

            # TODO - revisit probe in memory, can't get it to work
            # vstreams = ffmpeg.probe(in_file, select_streams="v")
            # alternatively, could enforce width/height/frames as input
            # but that may be weird and force users to save file themselves
            # instead of passing it in while in memory
            # so for now going to make pretend and write to a temp file
            # idea - just call subprocess ffmprobe
            # with NamedTemporaryFile('w+b') as file:
            #     buff = in_file.read(BUFFER_SIZE)
            #     while len(buff) > 0:
            #         file.write(buff)
            #         buff = in_file.read(BUFFER_SIZE)
            #     file.flush()

            #     vstreams = ffmpeg.probe(file.name, select_streams="v")
            #     video_stream = vstreams["streams"][0]
            #     width: int = int(video_stream["width"])
            #     height: int = int(video_stream["height"])
            #     frames: int = int(video_stream["nb_frames"])

        else:
            raise ValueError("wrong input type, dolt")

        # TODO - is always default depth?
        # want bgr32, rgb32 is wrong order and I guess we're just wrong everywhere else lolol
        input_process = (
            ffmpeg.input(**input_args).output(
                "pipe:", format="rawvideo", pix_fmt="bgr32", s=f"{width}x{height}"
            )
            # this output is still one frame even when writing to gif, something wrong with input
            # .output("./test_gif_output.gif", format="gif", s=f'{width}x{height}')
            .run_async(
                pipe_stdin=isinstance(in_file, IOBase), pipe_stdout=True
            )  # , cmd='/home/alex/ffmpeg-download/working/ffmpeg')
        )

        # if filepointer, write to ffmpeg stdin
        if isinstance(in_file, IOBase):
            buff = in_file.read(BUFFER_SIZE)
            while len(buff) > 0:
                input_process.stdin.write(buff)
                buff = in_file.read(BUFFER_SIZE)

            # close stdin otherwise we wait on read
            input_process.stdin.flush()
            input_process.stdin.close()

            # waiting appears to break
            # probably because process is done at this point? idk
            # need to poke around a little more

        depth = RawDataFrame.DEFAULT_DEPTH
        while True:
            buff = input_process.stdout.read(width * height * depth)

            if not buff or len(buff) == 0:
                break

            in_frame = np.frombuffer(buff, np.uint8).reshape((height, width, depth))
            rdf = RawDataFrame(in_frame)
            self.raw_data_frames.append(rdf)

        input_process.stdout.close()
        input_process.wait()

    def save(
        self,
        out_file: str | BinaryIO,
        target_framerate: int = DEFAULT_FRAMERATE,
        target_format: MultiImageFormat = DEFAULT_FORMAT,
        overwrite_existing: bool = False,
    ) -> None:
        """
        Save MultiImage to path

        :param path: path to filesystem
        :param target_framerate: framerate of saved file, defaults to DEFAULT_FRAMERATE
        :param overwrite_existing: remove existing file, defaults to False
        :raises Exception: format exception
        :raises Exception: generic it didnt work exception
        """
        # yolo
        if isinstance(overwrite_existing, str):
            os.remove(out_file)

        # TODO - can write to stage and then swap pointer at end to preserve image?
        # TODO type checking and more defaults - see single for ideas
        if target_format == MultiImageFormat.UNKNOWN:
            raise Exception("unknown not supported")
        elif target_format == MultiImageFormat.GIF:
            self._write_gif(out_file, target_framerate)
        else:
            raise Exception("unable to save for whatever reason")

    def _write_gif(self, out_file: str | BinaryIO, target_framerate: int) -> None:
        """
        previously gifify action

        :param path: file path to write to
        :param target_framerate: target framerate of gif
        """

        # TODO - cleanup comments, general refactor of this and RDV
        if target_framerate <= 0:
            target_framerate = MultiImage.DEFAULT_FRAMERATE

        if len(self.raw_data_frames) == 0:
            raise Exception("empty, cannot save")

        # TODO re-introduce validation for frame size consistency and shape
        height = self.raw_data_frames[0].height
        width = self.raw_data_frames[0].width

        ###
        # build ffmpeg command
        # based on: -filter_complex "[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse"
        ###

        # start by splitting input into 2 streams
        split_input = ffmpeg.input(
            "pipe:",
            s=f"{width}x{height}",
            format="rawvideo",
            pix_fmt="rgba",
            framerate=target_framerate,
        ).filter_multi_output("split")

        stream1 = split_input[0]
        stream2 = split_input[1]

        # generate pallete stream from one of our streams
        # this creates a custom pallete for the gif input to maximize color depth
        # and should also allow for transparency
        palletegen_stream = stream1.filter("palettegen", reserve_transparent=True)

        # apply custom pallete to other input stream
        palleteuse_stream = ffmpeg.filter((stream2, palletegen_stream), "paletteuse")

        # TODO capture stderr flag
        # TODO share more between process creation, no need for copy paste
        if isinstance(out_file, str):
            # TODO - overwrite_output()
            write_process = palleteuse_stream.output(out_file, format="gif").run_async(
                pipe_stdin=True
            )
        elif isinstance(out_file, IOBase):
            # read to memory, this is definitely slow, but should be OK for now until async
            write_process = palleteuse_stream.output("pipe:", format="gif").run_async(
                pipe_stdin=True, pipe_stdout=True
            )
        else:
            # this type check should really be earlier
            # but to make mypy work better, I think it is bettr here
            raise ValueError("invalid input type")

        count = 0
        for frame in self.raw_data_frames:
            # convert array, convert_data_arr is non-mutating so it's ok
            data_arr = RawDataFrame.convert_data_arr(
                frame.get_data_arr(is_return_reference=True), np.uint8
            )
            write_process.stdin.write(data_arr.tobytes())
            count += 1

        write_process.stdin.flush()
        write_process.stdin.close()

        if isinstance(out_file, IOBase):
            BUFFER_SIZE = 4096
            buff: bytes = write_process.stdout.read(BUFFER_SIZE)
            while len(buff) > 0:
                out_file.write(buff)
                buff = write_process.stdout.read(BUFFER_SIZE)

            # Close stdout after reading otherwise wait will hang
            write_process.stdout.close()

        write_process.wait()

    @classmethod
    def create_from_frame_batch(
        cls, batch: FrameBatch, target_format: MultiImageFormat = DEFAULT_FORMAT
    ) -> "MultiImage":
        mimg = cls()
        mimg.raw_data_frames += batch.frames
        mimg.format = target_format
        return mimg
