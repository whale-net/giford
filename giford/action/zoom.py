from giford.frame.frame_batch import FrameBatch
from giford.frame.raw_data import RawDataFrame

from .abstract_frame_action import AbstractFrameAction

from .crop import Crop
from .reshape import Reshape, ReshapeMethod

class Crop(AbstractFrameAction):
    def __init__(self) -> None:
        super().__init__()

    def process(
        self,
        input_batch: FrameBatch,
    ) -> FrameBatch:
        

        
        return output_batch
