from skimage import transform

from salt_shaker.image_actions.image_action import ChainImageAction
from salt_shaker.image_actions.translate import Translate
from salt_shaker.frame_batch import FrameBatch
from salt_shaker.raw_data import RawDataFrame


class Resize(ChainImageAction):
    def __init__(self):
        super().__init__()

    # TODO tests

    def process(self, input_batch: FrameBatch) -> FrameBatch:
        output_batch = FrameBatch()
        for frame in input_batch.frames:
            # TODO - does this modify? need to test if we need to clone on array.
            img_nd_arr = transform.resize(frame.as_3d_ndarray(), (frame.height // 4, frame.width // 4), anti_aliasing=True)
            output_batch.add_frame(RawDataFrame(img_nd_arr))

        return output_batch