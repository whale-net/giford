from typing import Optional

import numpy as np
from PIL import Image as PillowImage

from giford.frame.frame_batch import FrameBatch
from giford.frame.raw_data import RawDataFrame

from .abstract_frame_action import AbstractFrameAction


class Rotate(AbstractFrameAction):
    def __init__(self) -> None:
        super().__init__()

    FULL_ROTATION_DEGREES: int = 360

    def process(
        self,
        input_batch: FrameBatch,
        rotate_degrees: int = 0,
        is_clockwise: bool = True,
    ) -> FrameBatch:
        """
        rotate images in batch

        :param input_batch: input framebatch
        :param rotate_degrees: degrees to rotate, defaults to 0
        :param is_clockwise: rotate clockwise, defaults to True
        :return: batch of rotated frames
        """

        if rotate_degrees == 0:
            return input_batch.clone()

        if not is_clockwise:
            rotate_degrees = Rotate.FULL_ROTATION_DEGREES - rotate_degrees

        output_batch = FrameBatch()
        for frame in input_batch.frames:
            # will clone data
            rdf = RawDataFrame(frame.get_data_arr())

            # cheating using pimg, but tbh idc they did a good job
            # use reference because already cloning data
            pimg = PillowImage.fromarray(rdf.get_data_arr(is_return_reference=True))
            pimg = pimg.rotate(rotate_degrees)
            output_batch.add_frame(RawDataFrame(np.asarray(pimg)))

        return output_batch


class RotateMany(AbstractFrameAction):
    def __init__(self) -> None:
        super().__init__()

    def process(
        self,
        input_batch: FrameBatch,
        rotate_count: int = 30,
        is_clockwise: bool = True,
    ) -> FrameBatch:
        """
        Completes a full rotation for each frame in the input batch

        :param input_batch: input framebatch
        :param rotate_count: number of frames to Rotate, defaults to None
        :param is_clockwise: if true, rotate clockwise
        :return: frame batch
        """

        rotate_degrees = 360
        step_size: float = rotate_degrees / rotate_count

        r = Rotate()
        output_batch = FrameBatch()
        for frame in input_batch.frames:
            for step_idx in range(rotate_count):
                rotate_step: int = int(step_idx * step_size)

                temp_in_batch = FrameBatch.create_from_frame(frame)
                temp_out_batch = r.process(
                    temp_in_batch, rotate_degrees=rotate_step, is_clockwise=is_clockwise
                )
                output_batch.add_batch(temp_out_batch)

        return output_batch
