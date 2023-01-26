import ffmpeg
from skimage import transform
import numpy as np

from salt_shaker.image_actions.image_action import ChainImageAction
from salt_shaker.frame_batch import FrameBatch
from salt_shaker.raw_data import RawDataFrame


class Translate(ChainImageAction):
    def __init__(self):
        super().__init__()

    def process(
        self, input_batch: FrameBatch, horizontal_shift_px=0, vertical_shift_px=0
    ) -> FrameBatch:
        """
        translate image up down left right
        """
        # todo type checking and errors
        # todo support background color per pixel on shift
        # todo some optimizations around which rows run when
        # todo, look at more mathy numpy to see if there is a more better implementation
        if horizontal_shift_px == 0 and vertical_shift_px == 0:
            return input_batch.clone()

        output_batch = FrameBatch()
        for frame in input_batch.frames:
            frame = frame.clone()

            # handle horizontal shifts
            if horizontal_shift_px != 0:
                # we have data like [px0, px1, px2, px3, px4]
                # shift h+2 -> [empty, empty, px0, px1, px2]
                # shift h-2 -> [px2, px3, px4, empty, empty]

                # build array used to shift pixels
                empty_frame_h_shift_arr = np.array(
                    list(
                        frame.get_empty_pixel() for _ in range(abs(horizontal_shift_px))
                    )
                )
                # for each row in the frame, shift pixels with empty data
                for h_idx in range(frame.height):
                    intermediate_arr = frame.get_data_arr(is_return_reference=True)[h_idx]
                    if horizontal_shift_px > 0:
                        intermediate_arr = intermediate_arr[
                            : frame.width - horizontal_shift_px
                        ]
                        intermediate_arr = np.concatenate(
                            (empty_frame_h_shift_arr, intermediate_arr), axis=0
                        )
                    else:
                        intermediate_arr = intermediate_arr[abs(horizontal_shift_px) :]
                        intermediate_arr = np.concatenate(
                            (intermediate_arr, empty_frame_h_shift_arr), axis=0
                        )

                    frame.get_data_arr(is_return_reference=True)[h_idx] = intermediate_arr

            # handle vertical shift
            if vertical_shift_px != 0:
                # we have data like [row0, row1, row2, row3, row4]
                # shift v+2 -> [empty, empty, row0, row1, row2]
                # shift v-2 -> [row2, row3, row4, empty, empty]

                # create all the empty rows that we need to shift
                # i swear this is the best way to do this for this current implementation method
                # TODO - just use reshape. lmao
                empty_frame_pixel_rows = np.array(
                    list(
                        # note: the parens are needed here, turns it into a generator which will yield a list
                        # this makes the outer list function build a list of lists
                        (
                            list(frame.get_empty_pixel() for _ in range(frame.width))
                            for _ in range(abs(vertical_shift_px))
                        )
                    )
                )

                if vertical_shift_px > 0:
                    data_arr = frame.get_data_arr(is_return_reference=True)[: frame.height - vertical_shift_px]
                    frame.update_data_arr(np.concatenate(
                        (empty_frame_pixel_rows, data_arr), axis=0
                    ))
                else:
                    data_arr = frame.get_data_arr(is_return_reference=True)[abs(vertical_shift_px):]
                    frame.update_data_arr(np.concatenate(
                        (data_arr, empty_frame_pixel_rows), axis=0
                    ))

            output_batch.add_frame(frame)

        return output_batch
