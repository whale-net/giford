from giford.frame.frame_batch import FrameBatch
from giford.frame.raw_data import RawDataFrame

from .abstract_frame_action import AbstractFrameAction

from .crop import Crop
from .reshape import Reshape, ReshapeMethod


class Zoom(AbstractFrameAction):
    def __init__(self) -> None:
        super().__init__()

    def process(
        self, input_batch: FrameBatch, zoom_step_size_px: int = 0
    ) -> FrameBatch:
        crop_action = Crop()
        reshape_action = Reshape(ReshapeMethod.RESIZE)

        output_batch = FrameBatch()
        for frame in input_batch.frames:
            temp_batch = FrameBatch.create_from_frame(frame)
            temp_batch = crop_action.process(temp_batch, crop_px=zoom_step_size_px)

            # TODO aa  parameter
            temp_batch = reshape_action.process(
                temp_batch,
                veritcal_resize_px=frame.height,
                horiztonal_resize_px=frame.width,
                enable_anti_aliasing=True,
            )
            output_batch.add_batch(temp_batch)

        return output_batch
