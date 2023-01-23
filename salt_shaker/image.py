from __future__ import annotations  # py>=3.7 - make factory return type hints work

import os
import copy

import numpy as np
from skimage.io import imread, imsave

from salt_shaker.raw_data import RawDataFrame


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

        img_data = RawDataFrame(nd_arr=nd_arr)
        img = Image(img_data=img_data, _created_from_factory=True)
        return img

    @staticmethod
    def create_from_url(url: str) -> Image:
        # todo URL support?
        raise NotImplementedError()

    @staticmethod
    def create_from_bytes(bytes, height, width, depth=4) -> Image:
        # TODO byte datatype type hint
        img_nd_arr = np.frombuffer(bytes, dtype=np.uint8)
        img_nd_arr = np.reshape(img_nd_arr, (height, width, depth))
        return Image.create_from_ndarray(img_nd_arr)


    def __init__(self, img_data: RawDataFrame, _created_from_factory: bool = False):
        if not _created_from_factory:
            raise Exception(
                "please use a factory method like Image.create_from_ndarray()"
            )

        self._image_data = img_data
        if not isinstance(self.image_data, RawDataFrame):
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
    def image_data(self) -> RawDataFrame:
        if self._image_data is None:
            raise Exception("image data is None")

        return self._image_data

    @image_data.setter
    def image_data(self, value: RawDataFrame):
        self._image_data = value
