from skimage import transform
import numpy as np

from salt_shaker.image_actions.image_action import ChainImageAction
from salt_shaker.frame_batch import FrameBatch
from salt_shaker.raw_data import RawDataFrame


class Translate(ChainImageAction):

    _empty_frame = np.zeros((4,))

    def __init__(self):
        super().__init__()

    def process(self, input_batch: FrameBatch, horizontal_shift_px=0, vertical_shift_px=0) -> FrameBatch:
        """
        translate image up down left right
        """
        # todo type checking and errors

        if horizontal_shift_px == 0 and vertical_shift_px == 0:
            # todo clone
            return input_batch

        output_batch = FrameBatch()
        for frame in input_batch.frames:
            frame = frame.clone()

            # handle horizontal shifts
            if horizontal_shift_px != 0:
                # create empty array
                arr_builder_iter = (Translate._empty_frame for _ in range(abs(horizontal_shift_px)))
                arr_dtype = np.dtype((frame.data_arr[1].dtype, 4))
                empty_frame_vertical_arr = np.fromiter(arr_builder_iter, arr_dtype)

                for h_idx in range(frame.height):
                    a = empty_frame_vertical_arr
                    b = frame.data_arr[h_idx]

                    intermediate_arr = frame.data_arr[h_idx]
                    if horizontal_shift_px > 0:
                        # shorten array
                        intermediate_arr = intermediate_arr[:frame.width-horizontal_shift_px]
                        # build it back up
                        intermediate_arr = np.concatenate((empty_frame_vertical_arr, intermediate_arr), axis=0)
                    else:
                        # shorten array
                        intermediate_arr = intermediate_arr[abs(horizontal_shift_px):]
                        # build it back up
                        intermediate_arr = np.concatenate((intermediate_arr, empty_frame_vertical_arr), axis=0)

                    frame.data_arr[h_idx] = intermediate_arr

                    # combine arrays and pickup only pixels we want



            # img_nd_arr = transform.swirl(frame.as_3d_ndarray())
            output_batch.add_frame(frame)


        return output_batch