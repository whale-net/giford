import random
import enum

from giford.action.abstract_frame_action import AbstractFrameAction
from giford.frame.frame_batch import FrameBatch
from giford.util.virtual_path import VirtualPath
from giford.action.translate import Translate


class ShakeMode(enum.Enum):
    RANDOM = 1


class Shake(AbstractFrameAction):
    """
    testing idea, what this whole thing was for in the first place
    """

    DEFAULT_FRAME_COUNT = 30

    def __init__(self) -> None:
        pass

    def process(
        self,
        input_batch: FrameBatch,
        frame_count: int = DEFAULT_FRAME_COUNT,
        shake_mode: ShakeMode = ShakeMode.RANDOM,
        max_horizontal_move: float | None = 0.1,
        max_vertical_move: float | None = 0.1,
        max_horizontal_shift_px: int | None = None,
        max_vertical_shift_px: int | None = None,
        seed: str | int | None = None,
    ) -> FrameBatch:
        """
        Shake frame

        :param input_batch: input FrameBatch
        :param frame_count: number of frames to produce per input frame
        :param shake_mode: which shake algorithm is desired
        :param max_horizontal_move:
            max horizontal variance relative to frame origin, defaults to 0.1
        :param max_vertical_move:
            max vertical variance relative to frame origin, defaults to 0.1
        :param max_horizontal_shift_px: _description_, defaults to None
        :param max_vertical_shift_px: _description_, defaults to None
        :param seed: random seed, defaults to None
        :return: _description_
        """

        if not isinstance(input_batch, FrameBatch):
            raise Exception("wrong type")
        if frame_count <= 0:
            raise Exception("need > 0 frames")

        is_move: bool = max_horizontal_move is not None or max_vertical_move is not None
        is_px: bool = (
            max_horizontal_shift_px is not None or max_vertical_shift_px is not None
        )

        if not is_move and not is_px:
            raise Exception("please specify move or px")
        if is_move and is_px:
            raise Exception("move and px are mutually exclusive")

        output_batch: FrameBatch = FrameBatch()
        t = Translate()
        random.seed(seed)

        for frame in input_batch.frames:
            vp = VirtualPath()
            for _ in range(frame_count):
                x_shift: float = 0
                y_shift: float = 0
                if is_move:
                    # random() is between 0,1 so need to adjust by 0.5
                    # to account for origin at 0,0
                    if max_horizontal_move:
                        x_shift = max_horizontal_move * (random.random() - 0.5)
                    if max_vertical_move:
                        y_shift = max_vertical_move * (random.random() - 0.5)
                elif is_px:
                    # go backwards from px to relative movement
                    if max_horizontal_shift_px:
                        x_shift = max_horizontal_shift_px / frame.width
                    if max_vertical_shift_px:
                        y_shift = max_vertical_shift_px / frame.height

                vp.add_point_from_coords(x_shift, y_shift)

            for movement in vp.calculate_movements():
                process_batch = FrameBatch()
                process_batch.add_frame(frame)

                # TODO play with wrap
                process_batch = t.process(process_batch, movement=movement)
                output_batch.add_batch(process_batch)

        return output_batch
