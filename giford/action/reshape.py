import enum
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

    def __init__(self) -> None:
        super().__init__()

    def process(
        self,
        input_batch: FrameBatch,
        reshape_method: ReshapeMethod = ReshapeMethod.RESCALE,
        scale_factor: float = 1.0,
        enable_anti_aliasing: bool = True,
    ) -> FrameBatch:
        if scale_factor == 0:
            raise ZeroDivisionError("???????? what are you doing?")
        if scale_factor == 1.0:
            return input_batch.clone()

        output_batch = FrameBatch()
        for frame in input_batch.cloned_frames():
            match reshape_method:
                case ReshapeMethod.RESCALE:
                    frame = Reshape._rescale(frame, scale_factor, enable_anti_aliasing)
                case ReshapeMethod.RESIZE:
                    frame = Reshape._resize(frame, scale_factor, enable_anti_aliasing)
                case ReshapeMethod.DOWNSCALE:
                    frame = Reshape._downscale(frame)
                case _:  # default case
                    raise Exception(f"unsupported reshape method [{reshape_method}]")

            if frame is None:
                raise Exception("developer error, didn" "t set frame")

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
        frame: RawDataFrame, scale_factor: float, enable_anti_aliasing: bool
    ) -> RawDataFrame:
        size_divisor = 1 / scale_factor
        nd_arr = transform.resize(
            image=frame.get_data_arr(),
            output_shape=(frame.height // size_divisor, frame.width // size_divisor),
            anti_aliasing=enable_anti_aliasing,
        )

        return RawDataFrame(nd_arr)

    @staticmethod
    def _downscale(frame: RawDataFrame) -> RawDataFrame:
        raise NotImplementedError()
