import enum
import os
from io import IOBase
from typing import BinaryIO

import ffmpeg
import numpy as np

# aliasing to avoid confusion

from giford.frame.frame_batch import FrameBatch
from giford.frame.raw_data import RawDataFrame, RawDataVideo
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
        if isinstance(in_file, str):
            input_args = {"filename": in_file}
            # TODO - probe
            width: int = 449
            height: int = 524
            frames: int = 25
        elif isinstance(in_file, IOBase):
            input_args = {"filename": "pipe:"}
        else:
            raise ValueError("wrong input type, dolt")

        # TODO - is always default depth?
        # want bgr32, rgb32 is wrong order and I guess we're just wrong everywhere else lolol
        input_process = (
            ffmpeg.input(**input_args)
            .output("pipe:", format="rawvideo", pix_fmt="bgr32", vframes=frames)
            .run_async(pipe_stdout=True)
        )
        depth = RawDataFrame.DEFAULT_DEPTH
        while True:
            buff = input_process.stdout.read(width * height * depth)

            if not buff or len(buff) == 0:
                break

            in_frame = np.frombuffer(buff, np.uint8).reshape((height, width, depth))
            rdf = RawDataFrame(in_frame)
            self.raw_data_frames.append(rdf)

        # TODO - figure out what happens here more
        # if I break loop too early, it will stall
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
        """
        takes list of images and returns a gif
        """
        if target_framerate <= 0:
            target_framerate = MultiImage.DEFAULT_FRAMERATE

        # TODO re-introduce validation
        # validate shape and create raw_video
        # if not input_batch.is_all_frame_same_shape():
        #     raise Exception("not all images are same size in input")
        rdv = RawDataVideo()
        for frame in self.raw_data_frames:
            rdv.add_frame(frame)

        height = rdv.frames[0].height
        width = rdv.frames[0].width

        rdv_byte_pipe_input = rdv.as_ndarray(target_dtype=np.uint8).tobytes()

        # TODO - look at https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md#tensorflow-streaming
        # and make this buffered

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
        if isinstance(out_file, str):
            # returns stdout, stderr
            write_process = (
                palleteuse_stream.output(out_file, format="gif").run_async(
                    pipe_stdin=True
                )
                # TODO - overwrite_output()
            )
        elif isinstance(out_file, IOBase):
            # read to memory, this is definitely slow, but should be OK for now until async
            std_out_buffer, _ = palleteuse_stream.output("pipe:", format="gif").run(
                input=rdv_byte_pipe_input, capture_stdout=True
            )
            out_file.write(std_out_buffer)
        else:
            # this type check should really be earlier
            # but to make mypy work better, I think it is bettr here
            raise ValueError("invalid input type")

        for frame in self.raw_data_frames:
            # convert array, convert_data_arr is non-mutating so it's ok
            data_arr = RawDataFrame.convert_data_arr(
                frame.get_data_arr(is_return_reference=True), np.uint8
            )
            write_process.stdin.write(data_arr.tobytes())

        write_process.stdin.close()
        write_process.wait()

    @classmethod
    def create_from_frame_batch(
        cls, batch: FrameBatch, target_format: MultiImageFormat = DEFAULT_FORMAT
    ) -> "MultiImage":
        mimg = cls()
        mimg.raw_data_frames += batch.frames
        mimg.format = target_format
        return mimg
