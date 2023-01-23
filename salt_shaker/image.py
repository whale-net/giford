from __future__ import annotations  # py>=3.7 - make factory return type hints work

import os
import copy

import numpy as np
from skimage.io import imread, imsave


class Image:
    """
    simple wrapper for images

    the internal image format is a 3 dimensional uint8 array of height x width x 4 (depth)
        (in the future, maybe we can make 24bit array?)
    depth is currently hardcoded to 4 for rgba

    """

    @staticmethod
    def create_from_file(file_path: str) -> Image:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"file doesn't exist: [{file_path}]")

        nd_arr = imread(file_path)
        return Image.create_from_ndarray(nd_arr)

    @staticmethod
    def create_from_ndarray(nd_arr: np.ndarray) -> Image:
        # hopefully this saves head scratching
        if not isinstance(nd_arr, np.ndarray):
            raise Exception("nd_arr not type ndarray")

        img_data = ImageData(img_nd_arr=nd_arr)
        img = Image(img_data=img_data, _created_from_factory=True)
        return img

    @staticmethod
    def create_from_url(url: str) -> Image:
        # todo URL support?
        raise NotImplementedError()

    def __init__(self, img_data: ImageData, _created_from_factory: bool = False):
        if not _created_from_factory:
            raise Exception(
                "please use a factory method like Image.create_from_ndarray()"
            )

        self._image_data = img_data
        if not isinstance(self.image_data, ImageData):
            raise Exception("no valid input data provided to Image class")

    def write_to_file(self, file_path, overwrite=True):

        if os.path.isdir(file_path):
            raise Exception(f"provided path is a directory [{file_path}]")

        if not overwrite and os.path.exists(file_path):
            raise FileExistsError(f"file already exists [{file_path}]")

        imsave(file_path, self.image_data.as_3d_ndarray())

    def clone(self):
        return copy.deepcopy(self)

    @property
    def image_data(self) -> ImageData:
        if self._image_data is None:
            raise Exception("image data is None")

        return self._image_data

    @image_data.setter
    def image_data(self, value: ImageData):
        self._image_data = value


class ImageData:
    """
    wrapper for ndarray of size h x w x d (d=depth=always 4)
    """

    # ndarray.shape index
    __SHAPE_HEIGHT_IDX = 0
    __SHAPE_WIDTH_IDX = 1
    __SHAPE_DEPTH_IDX = 2

    @property
    def image_data_arr(self) -> np.ndarray:
        return self._image_data

    @property
    def height(self) -> int:
        return self.image_data_arr.shape[ImageData.__SHAPE_HEIGHT_IDX]

    @property
    def width(self) -> int:
        return self.image_data_arr.shape[ImageData.__SHAPE_WIDTH_IDX]

    @property
    def depth(self) -> int:
        return self.image_data_arr.shape[ImageData.__SHAPE_DEPTH_IDX]

    def __init__(self, img_nd_arr: np.ndarray):
        if not isinstance(img_nd_arr, np.ndarray):
            raise Exception("image_arr not ndarray")
        if img_nd_arr.ndim != 3:
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

        self._image_data = img_nd_arr

        if self.depth != 4:
            # todo transform d=1->4 and d=3->4. then error on depth not in [1, 3, 4]
            raise Exception(
                "image_arr depth is not 4, this can be fixed, but i cba now"
            )

    def as_3d_ndarray(self) -> np.ndarray:
        # array is already 3d ndarray
        return self.image_data_arr

    def as_1d_ndarray(self) -> np.ndarray:
        return self.image_data_arr.ravel()

    def is_same_shape(
        self, other_img_data: ImageData, is_check_depth: bool = False
    ) -> bool:
        if not isinstance(other_img_data, ImageData):
            return False
        return (
            self.height == other_img_data.height
            and self.width == other_img_data.width
            and (not is_check_depth or self.depth == other_img_data.depth)
        )
