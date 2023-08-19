import numpy as np
from typing import Optional

from giford.action.abstract_frame_action import AbstractFrameAction
from giford.frame.frame_batch import FrameBatch

from giford.util.virtual_path import Movement


class Translate(AbstractFrameAction):
    def __init__(self) -> None:
        super().__init__()

    def process(
        self,
        input_batch: FrameBatch,
        horizontal_shift_px: Optional[int] = None,
        vertical_shift_px: Optional[int] = None,
        movement: Optional[Movement] = None,
        wrap_image: bool = False,
    ) -> FrameBatch:
        """
        translate image up down left right
        """
        is_px_mode = horizontal_shift_px is not None or horizontal_shift_px is not None
        is_movement_mode = movement is not None

        if not is_px_mode and not is_movement_mode:
            raise Exception("no translate instructions provided")

        if is_px_mode and is_movement_mode:
            raise Exception("cannot use both px and movement")

        if (
            is_px_mode
            and horizontal_shift_px == 0
            and vertical_shift_px == 0
            or is_movement_mode
            and movement.distance() == 0  # type: ignore
        ):
            return input_batch.clone()

        # TODO support background color per pixel on shift
        # TODO, look at more mathy numpy to see if there is a more better implementation

        output_batch = FrameBatch()
        for frame in input_batch.cloned_frames():
            # data_arr references the img data in the cloned frame
            data_arr = frame.get_data_arr()

            if is_movement_mode:
                h_move = movement.x_distance  # type: ignore
                horizontal_shift_px = int(frame.width * h_move)
                y_move = movement.y_distance  # type: ignore
                vertical_shift_px = int(frame.height * y_move)

            # mypy test
            horizontal_shift_px = (
                0 if horizontal_shift_px is None else horizontal_shift_px
            )
            vertical_shift_px = 0 if vertical_shift_px is None else vertical_shift_px

            # handle horizontal shifts
            if horizontal_shift_px != 0:
                # we have data like [px0, px1, px2, px3, px4]
                # shift h+2 -> [empty, empty, px0, px1, px2]
                # shift h-2 -> [px2, px3, px4, empty, empty]

                # todo - is there way to do this outside of for loop?
                # use np.roll to move data and then zero it with empty pixels
                for h_idx in range(frame.height):
                    tmp_arr = np.roll(
                        data_arr[h_idx], horizontal_shift_px * frame.depth
                    )

                    # roll will wrap the pixel array around on itself
                    # so clear out the pixels if requested
                    if not wrap_image:
                        if horizontal_shift_px > 0:
                            tmp_arr[:horizontal_shift_px] = frame.get_empty_pixel()
                        else:
                            tmp_arr[horizontal_shift_px:] = frame.get_empty_pixel()

                    data_arr[h_idx] = tmp_arr

            # handle vertical shift
            if vertical_shift_px != 0:
                # we have data like [row0, row1, row2, row3, row4]
                # shift v+2 -> [empty, empty, row0, row1, row2]
                # shift v-2 -> [row2, row3, row4, empty, empty]

                # need to specify axis, otherwise shifted for axis0 and axis1

                # np.pad? -> no. does not give us ability to wrap image
                # could do for later optimization, but unsure if needed.
                data_arr = np.roll(data_arr, vertical_shift_px, axis=0)

                if not wrap_image:
                    if vertical_shift_px > 0:
                        data_arr[:vertical_shift_px] = frame.get_empty_pixel()
                    else:
                        data_arr[vertical_shift_px:] = frame.get_empty_pixel()

            # is this update needed?
            frame.update_data_arr(data_arr)
            output_batch.add_frame(frame)

        return output_batch
