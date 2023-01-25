from __future__ import annotations  # py>=3.7

import copy

import numpy as np
import itertools
from salt_shaker.frame_batch import FrameBatch

# TODO remove ImageData references
class RawDataFrame:
    """
    wrapper for ndarray of size h x w x d (d=depth=always 4)
    """

    # ndarray.shape index
    __SHAPE_HEIGHT_IDX = 0
    __SHAPE_WIDTH_IDX = 1
    __SHAPE_DEPTH_IDX = 2

    @property
    def data_arr(self) -> np.ndarray:
        return self._image_data

    @data_arr.setter
    def data_arr(self, value: np.ndarray):
        # i dont really like the idea of this being accessible
        # but by exposing the data_arr in the first place i open myself up to this
        # i suppose that if you want a clone i can make as_3d_ndarray do that
        self._image_data = value


    @property
    def height(self) -> int:
        return self.data_arr.shape[RawDataFrame.__SHAPE_HEIGHT_IDX]

    @property
    def width(self) -> int:
        return self.data_arr.shape[RawDataFrame.__SHAPE_WIDTH_IDX]

    @property
    def depth(self) -> int:
        return self.data_arr.shape[RawDataFrame.__SHAPE_DEPTH_IDX]

    @property
    def flat_data(self):
        """
        iterator for data in array
        """
        # todo this is a really weird property that should be reconsidered
        for val in self.data_arr.flat:
            yield val

    def __init__(self, nd_arr: np.ndarray):
        if not isinstance(nd_arr, np.ndarray):
            raise Exception("image_arr not ndarray")
        if nd_arr.ndim != 3:
            raise Exception("image_arr has incorrect dimensions. expected h x w x 4")

        # TODO - decide how to handle different types. explicit failure or implict cast?
        # NOTE - using uint8 kind of works, except when we cast a bunch of times we lose precision
        # Can we depend on the programmer to use the correct types?
        # or should we be lazy and just let it be until a different type is requested?
        # if img_nd_arr.dtype != np.dtype(np.uint8):
        # if img_nd_arr.dtype == np.dtype(np.uint8):
        #     pass
        # elif img_nd_arr.dtype in [np.dtype(np.float32), np.dtype(np.float64)]:
        #     # check if image is scaled [0, 1] and scale it to [0, 255]
        #     if img_nd_arr.max() <= 1.0:
        #         img_nd_arr = img_nd_arr * 256
        #     img_nd_arr = img_nd_arr.astype(np.uint8, copy=False)
        # else:
        #     raise Exception(f"invalid dtype {img_nd_arr.dtype}")
        #

        self._image_data = nd_arr



        if self.depth != 4:
            # todo transform d=1->4 and d=3->4. then error on depth not in [1, 3, 4]
            raise Exception(
                "image_arr depth is not 4, this can be fixed, but i cba now"
            )

    def as_3d_ndarray(self) -> np.ndarray:
        # modifying will modify array in this data frame
        # array is already 3d ndarray
        return self.data_arr

    def as_1d_ndarray(self) -> np.ndarray:
        # modifying will modify array in this data frame
        return self.data_arr.ravel()

    def is_same_shape(
        self, other_raw_data: RawDataFrame, is_check_depth: bool = False
    ) -> bool:
        if not isinstance(other_raw_data, RawDataFrame):
            return False
        return (
            self.height == other_raw_data.height
            and self.width == other_raw_data.width
            and (not is_check_depth or self.depth == other_raw_data.depth)
        )

    def clone(self):
        return copy.deepcopy(self)

    def get_empty_pixel(self):
        return np.zeros((self.depth,)).astype(self.data_arr.dtype)


class RawDataVideo:
    """
    acts as raw video
    """

    @property
    def frames(self) -> list[RawDataFrame]:
        return self._raw_data_frames

    def __init__(self):
        self._raw_data_frames: list[RawDataFrame] = []

    def add_frame(self, raw_data_frame: RawDataFrame):
        # TODO - somehow validate all frames are same size. that'll break it
        self.frames.append(raw_data_frame)

    def add_batch(self, batch: FrameBatch):
        for frame in batch.frames:
            self.add_frame(frame)

    def as_ndarray(self) -> np.ndarray:
        """
        convert raw_data_frames to array of raw data arrays
        # TODO currently 1d
        """
        num_frames = len(self.frames)
        if num_frames == 0:
            raise Exception("empty rawdatavideo")
        first_frame = self.frames[0]

        ###
        # create video ndarray using iterators
        # will copy memory, one day would like to avoid that, but I think it's needed anyways when
        # piping to ffmpeg, unless there is a way to buffer stdin piping to ffmpeg. that's for another day though
        ###

        # get iterators for each frame into a list
        flat_frame_iters = [f.flat_data for f in self.frames]
        # unpack list of iterators as parameters so chain can combine them correctly
        chained_iter = itertools.chain(*flat_frame_iters)

        video_arr: np.ndarray = np.fromiter(
            chained_iter,
            first_frame.data_arr.dtype,
            first_frame.data_arr.size * num_frames,
        )
        return video_arr
