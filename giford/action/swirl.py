from skimage import transform

from giford.action.abstract_frame_action import AbstractFrameAction
from giford.frame.frame_batch import FrameBatch
from giford.frame.raw_data import RawDataFrame


class BasicSwirl(AbstractFrameAction):
    def __init__(self) -> None:
        super().__init__()

    def process(self, input_batch: FrameBatch) -> FrameBatch:
        output_batch = FrameBatch()
        for frame in input_batch.frames:
            img_nd_arr = frame.get_data_arr()

            img_nd_arr = transform.swirl(img_nd_arr)

            output_batch.add_frame(RawDataFrame(img_nd_arr))

        return output_batch


class VariableSwirl(AbstractFrameAction):
    DEFAULT_DEPTH = 5

    def __init__(self) -> None:
        super().__init__()

    def process(
        self, input_batch: FrameBatch, depth: int = DEFAULT_DEPTH
    ) -> FrameBatch:
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
            for _ in range(0, depth):
                batch = basic_swirl.process(batch)

            # adding a batch will copy them
            output_batch.add_batch(batch)

        return output_batch


class VaryingVariableSwirl(AbstractFrameAction):
    def __init__(self) -> None:
        super().__init__()

    def process(
        self,
        input_batch: FrameBatch,
        depth: int = VariableSwirl.DEFAULT_DEPTH,
        swirl_depth_increment: int = 1,
        is_increasing_swirl_depth: bool = False,
    ) -> FrameBatch:
        """
        if multiple images are passed in, array with size len(image_input)*depth return
        index with [image_idx * depth + depth_idx]

        :param swirl_depth_increment: number of swirls between return swirls, default 1
        :param is_increasing_swirl_depth: tie swirl depth to number of swirls, default False
        # TODO - support swirl_depth_increment + increasing depth???
        """
        if not isinstance(depth, int):
            raise Exception(f"depth is not valid int [{depth}]")
        if depth < 0:
            # todo - make fun thing with negatives
            raise Exception(f"depth cannot be negative [{depth}]")

        variable_swirl = VariableSwirl()

        def recursive_swirl(
            in_batch: FrameBatch,
            swirl_depth: int,
            out_batch: FrameBatch,
            depth_counter: int = 0,
        ) -> None:
            """
            recursively call variable_swirl adding frames into out_batch
            hopefully tail recursive but idk if python supports that

            :param in_batch: batch to process
            :param swirl_depth: number of times left to swirl
            :param out_batch: output batch to append swirls to
            """
            if swirl_depth <= 0:
                return
            depth_counter += 1
            out_batch.add_batch(in_batch)

            if is_increasing_swirl_depth:
                target_depth = depth_counter
            else:
                target_depth = swirl_depth_increment
            next_batch = variable_swirl.process(in_batch, depth=target_depth)
            recursive_swirl(
                next_batch, swirl_depth - 1, out_batch, depth_counter=depth_counter
            )

        output_batch = FrameBatch()

        for frame in input_batch.frames:
            # turn each image in input_batch into its own batch so we can feed it into another action
            batch = FrameBatch()
            batch.add_frame(frame)
            recursive_swirl(batch, depth, output_batch)

        return output_batch
