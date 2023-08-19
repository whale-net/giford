import enum
import os

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
    DEFAULT_FRAMERATE = 15
    DEFAULT_FORMAT = MultiImageFormat.GIF

    def __init__(self) -> None:
        super().__init__()

        self.raw_data_frames: list[RawDataFrame] = []
        self.format = MultiImageFormat.UNKNOWN

    def load(self, path: str) -> None:
        # not currently supported
        raise NotImplementedError()

    def save(
        self,
        path: str,
        target_framerate: int = DEFAULT_FRAMERATE,
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
        if overwrite_existing:
            os.remove(path)

        # TODO - can write to stage and then swap pointer at end to preserve image?
        # TODO type checking and more defaults - see single for ideas
        if self.format == MultiImageFormat.UNKNOWN:
            raise Exception("unknown format not supported")
        elif self.format == MultiImageFormat.GIF:
            self._write_gif(path, target_framerate)
        else:
            raise Exception("unable to save for whatever reason")

    def _write_gif(self, path: str, target_framerate: int) -> tuple[str, str]:
        """
        previously gifify action

        :param path: file path to write to
        :param target_framerate: target framerate of gif
        """

        # TODO - cleanup comments, general refactor of this and RDV
        """
        takes list of images and returns a gif
        """
        if target_framerate is None or target_framerate <= 0:
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

        # this was in memory which was cool but not needed here
        # keeping because it could be useful for later reference in other areas
        # out, err = palleteuse_stream.output("pipe:", format="gif").run(
        #     capture_stdout=True, capture_stderr=True, input=rdv_byte_pipe_input
        # )

        # TODO capture stderr flag
        out, err = palleteuse_stream.output(path, format="gif").run(
            input=rdv_byte_pipe_input
        )

        # assuming these are strings
        return out, err

    @staticmethod
    def create_from_frame_batch(
        batch: FrameBatch, target_format: MultiImageFormat = DEFAULT_FORMAT
    ) -> "MultiImage":  # one day 3.11 -> Self:
        # TODO better type checking and such
        mimg = MultiImage()
        mimg.raw_data_frames += batch.frames
        mimg.format = target_format
        return mimg
