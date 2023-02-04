import ffmpeg
import numpy as np

from giford.image_actions.image_action import ExportImageAction
from giford.raw_data import RawDataVideo
from giford.frame_batch import FrameBatch
from giford.image import Image
from giford.image_formats import ImageFormat


class Gifify(ExportImageAction):
    def __init__(self, default_framerate: int = 5):
        super().__init__()
        self._default_framerate = default_framerate

    def process(self, input_batch: FrameBatch, framerate: int = None) -> Image:
        """
        takes list of images and returns a gif
        """
        if not framerate or framerate < 0:
            framerate = self._default_framerate

        # validate shape and create raw_video
        if not input_batch.is_all_frame_same_shape():
            raise Exception("not all images are same size in input")
        rdv = RawDataVideo()
        rdv.add_batch(input_batch)

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
            framerate=framerate,
        ).filter_multi_output("split")

        stream1 = split_input[0]
        stream2 = split_input[1]

        # generate pallete stream from one of our streams
        # this creates a custom pallete for the gif input to maximize color depth
        # and should also allow for transparency
        palletegen_stream = stream1.filter("palettegen", reserve_transparent=True)

        # apply custom pallete to other input stream
        palleteuse_stream = ffmpeg.filter((stream2, palletegen_stream), "paletteuse")

        out, _ = palleteuse_stream.output("pipe:", format="gif").run(
            capture_stdout=True, input=rdv_byte_pipe_input
        )

        return Image.create_from_bytes(out, fmt=ImageFormat.GIF)
