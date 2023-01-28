from skimage import transform

from salt_shaker.image_actions.image_action import ChainImageAction
from salt_shaker.image_actions.translate import Translate
from salt_shaker.frame_batch import FrameBatch
from salt_shaker.raw_data import RawDataFrame


class BasicScroll(ChainImageAction):
    def __init__(self):
        super().__init__()

    def process(self, input_batch: FrameBatch, num_frames: int = 60) -> FrameBatch:
        # todo custom args, maybe new action instead? meh on that idea
        # vertical shift, horizontal, reverse
        # no jitter, that is different action
        output_batch = FrameBatch()

        # todo empty frames around beginning and end
        # todo empty frame util somehwere. maybe rawdataframe
        t = Translate()
        for frame in input_batch.frames:
            # want to scroll left to right
            # so need to account for travelling 2x distance to get fully on/off
            # TODO renae
            scroll_base = 2 * frame.width // num_frames

            for i in range(num_frames):
                output_batch.add_batch(
                        t.process(input_batch, horizontal_shift_px=-frame.width + (i * scroll_base))
                    )

        return output_batch
