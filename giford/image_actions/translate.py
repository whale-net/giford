import ffmpeg
from skimage import transform
import numpy as np

from giford.image_actions.image_action import ChainImageAction
from giford.frame_batch import FrameBatch
from giford.raw_data import RawDataFrame


class Translate(ChainImageAction):
    def __init__(self):
        super().__init__()

    def process(
        self,
        input_batch: FrameBatch,
        horizontal_shift_px=0,
        vertical_shift_px=0,
        wrap_image=False,
    ) -> FrameBatch:
        """
        translate image up down left right
        """
        # todo type checking and errors
        # todo support background color per pixel on shift
        # -> different function maybe to fill in left side
        # todo, look at more mathy numpy to see if there is a more better implementation
        if horizontal_shift_px == 0 and vertical_shift_px == 0:
            return input_batch.clone()

        output_batch = FrameBatch()
        for frame in input_batch.cloned_frames():
            # data_arr references the img data in the cloned frame
            data_arr = frame.get_data_arr()

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

            frame.update_data_arr(data_arr)
            output_batch.add_frame(frame)

        return output_batch
