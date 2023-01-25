from skimage import transform
import numpy as np

from salt_shaker.image_actions.image_action import ChainImageAction
from salt_shaker.frame_batch import FrameBatch
from salt_shaker.raw_data import RawDataFrame


class Translate(ChainImageAction):

    _empty_frame = np.zeros((4,))

    def __init__(self):
        super().__init__()

    def process(self, input_batch: FrameBatch, horizontal_pixels=0, vertical_pixels=0) -> FrameBatch:
        """
        translate image up down left right
        """
        if horizontal_pixels == 0 and vertical_pixels == 0:
            return input_batch

        output_batch = FrameBatch()
        for frame in input_batch.frames:
            frame = frame.clone()

            arr_builder_iter = (Translate._empty_frame for _ in range(30))
            arr_dtype = np.dtype((frame.data_arr[1].dtype, 4))
            empty_frame_vertical_arr = np.fromiter(arr_builder_iter, arr_dtype)


            for h_idx in range(frame.height):
                a = empty_frame_vertical_arr
                b = frame.data_arr[h_idx]
                frame.data_arr[h_idx] = np.concatenate((a, b), axis=0)[:frame.width]


            # img_nd_arr = transform.swirl(frame.as_3d_ndarray())
            output_batch.add_frame(frame)


        return output_batch


