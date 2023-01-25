from skimage import transform

from salt_shaker.image_actions.image_action import ChainImageAction
from salt_shaker.image_actions.translate import Translate
from salt_shaker.frame_batch import FrameBatch
from salt_shaker.raw_data import RawDataFrame


class BasicScroll(ChainImageAction):
    def __init__(self):
        super().__init__()

    def process(self, input_batch: FrameBatch) -> FrameBatch:
        # todo custom args, maybe new action instead? meh on that idea
        # vertical shift, horizontal, reverse
        # no jitter, that is different action
        output_batch = FrameBatch()

        # todo empty frames around beginning and end
            # todo empty frame util somehwere. maybe rawdataframe
        t = Translate()
        for frame in input_batch.frames:
            # 30 frames for now
            scroll_base = int(frame.width / 30)

            for i in range(scroll_base):
                output_batch.add_batch(t.process(input_batch, horizontal_shift_px=-int((30-i)*scroll_base)))
            output_batch.add_batch(t.process(input_batch, horizontal_shift_px=0))
            for i in range(scroll_base):
                output_batch.add_batch(t.process(input_batch, horizontal_shift_px=int(i*scroll_base)))

        return output_batch