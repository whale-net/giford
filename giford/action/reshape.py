import enum
from typing import Optional
from skimage import transform

from giford.action.abstract_frame_action import AbstractFrameAction
from giford.frame.frame_batch import FrameBatch
from giford.frame.raw_data import RawDataFrame


class ReshapeMethod(enum.Enum):
    RESCALE = 1
    RESIZE = 2
    DOWNSCALE = 3


class Reshape(AbstractFrameAction):
    """
    turns 120x120 into 60x60 or 240x240
    """

    def __init__(
        self, default_reshape_method: ReshapeMethod = ReshapeMethod.RESIZE
    ) -> None:
        super().__init__()
        self.default_reshape_method = default_reshape_method

    def process(
        self,
        input_batch: FrameBatch,
        scale_factor: float = 1.0,
        enable_anti_aliasing: bool = True,
        veritcal_resize_px: Optional[int] = None,
        horiztonal_resize_px: Optional[int] = None,
        reshape_method: Optional[ReshapeMethod] = None,
    ) -> FrameBatch:
        if scale_factor == 0:
            raise ZeroDivisionError("???????? what are you doing?")
        if (
            scale_factor == 1.0
            and horiztonal_resize_px is None
            and veritcal_resize_px is None
        ):
            return input_batch.clone()

        if reshape_method is None:
            reshape_method = self.default_reshape_method

        output_batch = FrameBatch()
        for frame in input_batch.cloned_frames():
            match reshape_method:
                case ReshapeMethod.RESCALE:
                    frame = Reshape._rescale(frame, scale_factor, enable_anti_aliasing)
                case ReshapeMethod.RESIZE:
                    size_divisor = 1 / scale_factor
                    # when one of these is none, it will default to the same size
                    if horiztonal_resize_px is None:
                        horiztonal_resize_px = int(frame.width // size_divisor)
                    if veritcal_resize_px is None:
                        veritcal_resize_px = int(frame.height // size_divisor)

                    frame = Reshape._resize(
                        frame,
                        veritcal_resize_px,
                        horiztonal_resize_px,
                        enable_anti_aliasing,
                    )
                case ReshapeMethod.DOWNSCALE:
                    frame = Reshape._downscale(frame)

            output_batch.add_frame(frame)

        return output_batch

    @staticmethod
    def _rescale(
        frame: RawDataFrame, scale_factor: float, enable_anti_aliasing: bool
    ) -> RawDataFrame:
        nd_arr = transform.rescale(
            image=frame.get_data_arr(),
            scale=scale_factor,
            anti_aliasing=enable_anti_aliasing,
            channel_axis=RawDataFrame.SHAPE_DEPTH_IDX,
        )
        return RawDataFrame(nd_arr)

    @staticmethod
    def _resize(
        frame: RawDataFrame, height: int, width: int, enable_anti_aliasing: bool
    ) -> RawDataFrame:
        nd_arr = transform.resize(
            image=frame.get_data_arr(),
            output_shape=(height, width),
            anti_aliasing=enable_anti_aliasing,
        )

        return RawDataFrame(nd_arr)

    @staticmethod
    def _downscale(frame: RawDataFrame) -> RawDataFrame:
        raise NotImplementedError()
