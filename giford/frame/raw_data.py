from __future__ import annotations  # py>=3.7

import numpy as np
import itertools
from giford.frame.frame_batch import FrameBatch


class RawDataFrame:
    """
    wrapper for ndarray of size h x w x d (d=depth=always 4)
    """

    # ndarray.shape index
    SHAPE_HEIGHT_IDX = 0
    SHAPE_WIDTH_IDX = 1
    SHAPE_DEPTH_IDX = 2

    SUPPORTED_DATATYPES = (np.uint8, np.float32, np.float64)

    @property
    def height(self) -> int:
        """
        vertical, y
        """
        return self._data_arr.shape[RawDataFrame.SHAPE_HEIGHT_IDX]

    @property
    def width(self) -> int:
        """
        horizontal, x
        """
        return self._data_arr.shape[RawDataFrame.SHAPE_WIDTH_IDX]

    @property
    def depth(self) -> int:
        return self._data_arr.shape[RawDataFrame.SHAPE_DEPTH_IDX]

    @property
    def data_size(self) -> int:
        """
        returns size (number of pixels*depth)
        :return: size of data_arr
        """
        return self._data_arr.size

    def flat_data(self, target_dtype: np.dtype = None):
        """
        iterator for data in array
        """
        # todo this is a really weird property that should be reconsidered
        # seems like it does make things easier, but how much easier? building this way seems bad
        # maybe can make 1ds, concat all at once and then reshape
        data_arr = self.get_data_arr()
        if target_dtype is not None:
            data_arr = RawDataFrame.convert_data_arr(
                data_arr, target_dtype=target_dtype
            )

        for val in data_arr.flat:
            yield val

    def get_data_arr(self, is_return_reference: bool = False) -> np.ndarray:
        """
        return underlying data array
        :param is_return_reference: if true return underlying array (dangerous)
        :return:
        """
        arr = self._data_arr if is_return_reference else np.copy(self._data_arr)
        return arr

    def update_data_arr(self, target_data_arr: np.ndarray):
        # TODO type checking
        if self._data_arr.shape != target_data_arr.shape:
            raise Exception(
                "target array is different shape than existing. if you want to change underlying shape, create new frame"
            )
        self._data_arr = target_data_arr

    def __init__(self, nd_arr: np.ndarray):
        if not isinstance(nd_arr, np.ndarray):
            raise Exception("image_arr not ndarray")
        if nd_arr.ndim != 3:
            raise Exception("image_arr has incorrect dimensions. expected h x w x 4")
        if nd_arr.dtype not in RawDataFrame.SUPPORTED_DATATYPES:
            raise Exception(f"unsupported datatype given {nd_arr.dtype}")

        self._data_arr = np.copy(nd_arr)

        if self.depth != 4:
            # todo transform d=1->4 and d=3->4. then error on depth not in [1, 3, 4]
            raise Exception(
                "image_arr depth is not 4, this can be fixed, but i cba now"
            )

    # unused
    # def as_3d_ndarray(self) -> np.ndarray:
    #     # modifying will modify array in this data frame
    #     # array is already 3d ndarray
    #     return self.get_data_arr()

    # unused
    # def as_1d_ndarray(self) -> np.ndarray:
    #     # modifying will modify array in this data frame
    #     return self.get_data_arr().ravel()

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
        return RawDataFrame(self._data_arr)

    def get_empty_pixel(self):
        return np.zeros((self.depth,)).astype(self._data_arr.dtype)

    @staticmethod
    def convert_data_arr(data_arr: np.ndarray, target_dtype: np.dtype):
        """
        return data_arr as target dtype

        :param data_arr: numpy array containing data
        :param target_dtype: target numpy data type
        :return: data_arr
        """

        current_dtype = data_arr.dtype
        match target_dtype:
            # TODO - better handling of conversion between compatible types (float32 and float64 for example)
            case np.uint8:
                if current_dtype in (np.float32, np.float64):
                    # if max value is 1.0 then assume scaled [0, 1] and rescale
                    if data_arr.max() <= 1.0:
                        data_arr = data_arr.copy()
                        data_arr *= 255

                # we want to modify array
                return data_arr.astype(target_dtype)
            case np.float64:
                data_arr = data_arr.astype(target_dtype)

                if current_dtype == np.uint8:
                    # 0 = 0, 1.0 = 255
                    data_arr /= 255

                return data_arr
            case _:
                raise Exception(f"unsupported target_dtype: [{target_dtype}]")


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

    def as_ndarray(self, target_dtype: np.dtype = None) -> np.ndarray:
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
        flat_frame_iters = [f.flat_data(target_dtype=target_dtype) for f in self.frames]
        # unpack list of iterators as parameters so chain can combine them correctly
        chained_iter = itertools.chain(*flat_frame_iters)

        video_arr: np.ndarray = np.fromiter(
            chained_iter,
            # first_frame.get_data_arr().dtype,
            target_dtype,
            first_frame.data_size * num_frames,
        )

        return video_arr
