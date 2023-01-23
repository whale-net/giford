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

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def depth(self) -> int:
        return self._depth

    @property
    def image_data(self) -> np.ndarray:
        return self._image_data

    def __init__(self, img_nd_arr: np.ndarray):
        if not isinstance(img_nd_arr, np.ndarray):
            raise Exception("image_arr not ndarray")
        if img_nd_arr.ndim != 3:
            raise Exception("image_arr has incorrect dimensions. expected h x w x 4")

        # TODO - decide how to handle different types. explicit failure or implict cast?
        #if img_nd_arr.dtype != np.dtype(np.uint8):
        if img_nd_arr.dtype == np.dtype(np.uint8):
            pass
        elif img_nd_arr.dtype in [np.dtype(np.float32), np.dtype(np.float64)]:
            # check if image is scaled, and scale it if so
            if img_nd_arr.max() <= 1.0:
                img_nd_arr = img_nd_arr * 255
            img_nd_arr = img_nd_arr.astype(np.uint8, copy=False)
        else:
            raise Exception(f'invalid dtype {img_nd_arr.dtype}')



        self._height, self._width, self._depth = img_nd_arr.shape

        if self._depth != 4:
            # todo transform d=1->4 and d=3->4. then error on depth not in [1, 3, 4]
            raise Exception("image_arr depth is not 4, this can be fixed, but i cba now")

        self._image_data = img_nd_arr

    def as_3d_ndarray(self) -> np.ndarray:
        return self.image_data

    def as_1d_ndarray(self) -> np.ndarray:
        return self.image_data.ravel()


