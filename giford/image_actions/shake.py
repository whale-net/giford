import random

from giford.image_actions.image_action import ChainImageAction
from giford.frame_batch import FrameBatch
from giford.image_actions.translate import Translate

class Shake(ChainImageAction):
    """
    testing idea, what this whole thing was for in the first place
    """

    def __init__(self):
        super().__init__()


    def process(self, input_batch: FrameBatch, frame_count: int,
                seed: str|int = None,
                max_horizontal_shift: int = 10, 
                max_vertical_shift: int = 10):
        output_batch: FrameBatch = FrameBatch()
        t = Translate()
        random.seed(seed)

        for frame in input_batch.frames:
            for _ in range(frame_count):
                process_batch = FrameBatch()
                process_batch.add_frame(frame)
                # more randmom seeding options? will
                horizontal_move = random.randint(-max_horizontal_shift/2, max_horizontal_shift/2)
                vertical_move = random.randint(-max_vertical_shift/2, max_vertical_shift/2)

                # TODO play with wrap
                process_batch = t.process(process_batch, horizontal_move, vertical_move)

                output_batch.add_batch(process_batch)

        return output_batch



            

        