import numpy as np
from skimage import transform

from giford.image_actions.image_action import ChainImageAction
from giford.frame_batch import FrameBatch
from giford.raw_data import RawDataFrame


class BasicSwirl(ChainImageAction):
    def __init__(self):
        super().__init__()

    def process(self, input_batch: FrameBatch) -> FrameBatch:
        output_batch = FrameBatch()
        for frame in input_batch.frames:
            img_nd_arr = frame.as_3d_ndarray()

            img_nd_arr = transform.swirl(img_nd_arr)

            output_batch.add_frame(RawDataFrame(img_nd_arr))

        return output_batch


class VariableSwirl(ChainImageAction):
    def __init__(self):
        super().__init__()

    def process(self, input_batch: FrameBatch, depth: int) -> FrameBatch:
        if not isinstance(depth, int):
            raise Exception(f"depth is not valid int [{depth}]")
        if depth < 0:
            # todo - make fun thing with negatives
            raise Exception(f"depth cannot be negative [{depth}]")

        output_batch = FrameBatch()
        basic_swirl = BasicSwirl()
        for frame in input_batch.frames:
            # turn each image in input_batch into its own batch so we can feed it into another action
            batch = FrameBatch()
            batch.add_frame(frame)
            for i in range(0, depth):
                batch = basic_swirl.process(batch)

            # adding a batch will copy them
            output_batch.add_batch(batch)

        return output_batch


class VaryingVariableSwirl(ChainImageAction):
    def __init__(self):
        super().__init__()

    def process(self, input_batch: FrameBatch, depth: int) -> FrameBatch:
        """
        if multiple images are passed in, array with size len(image_input)*depth return
        index with [image_idx * depth + depth_idx]
        """
        if not isinstance(depth, int):
            raise Exception(f"depth is not valid int [{depth}]")
        if depth < 0:
            # todo - make fun thing with negatives
            raise Exception(f"depth cannot be negative [{depth}]")

        output_batch = FrameBatch()
        variable_swirl = VariableSwirl()
        for frame in input_batch.frames:
            # turn each image in input_batch into its own batch so we can feed it into another action
            batch = FrameBatch()
            batch.add_frame(frame)
            for i in range(0, depth):
                batch = variable_swirl.process(batch, i)
                output_batch.add_batch(batch)

        return output_batch
