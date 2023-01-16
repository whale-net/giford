from __future__ import annotations  # py>=3.7 - make factory return type hints work

import os

from numpy import ndarray
from skimage.io import imread, imsave


class Image:
    """
    simple wrapper for images
    """

    @staticmethod
    def create_from_file(file_path: str) -> Image:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"file doesn't exist: [{file_path}]")

        nd_arr = imread(file_path)
        return Image.create_from_ndarray(nd_arr)

    @staticmethod
    def create_from_ndarray(nd_arr: ndarray) -> Image:
        # hopefully this saves head scratching
        if not isinstance(nd_arr, ndarray):
            raise Exception("nd_arr not type ndarry")

        img = Image(img_nd_arr=nd_arr, _created_from_factory=True)
        return img

    @staticmethod
    def create_from_url(url: str) -> Image:
        # todo URL support?
        raise NotImplementedError()

    def __init__(self, img_nd_arr: ndarray, _created_from_factory: bool = False):
        if not _created_from_factory:
            raise Exception(
                "please use a factory method like Image.create_from_ndarray()"
            )

        self._image_data: ndarray = img_nd_arr
        if not isinstance(self.image_data, ndarray):
            raise Exception("no valid input data provided to Image class")

    def write_to_file(self, file_path, overwrite=True):

        if os.path.isdir(file_path):
            raise Exception(f"provided path is a directory [{file_path}]")

        if not overwrite and os.path.exists(file_path):
            raise FileExistsError(f"file already exists [{file_path}]")

        imsave(file_path, self.image_data)

    @property
    def image_data(self) -> ndarray:
        if self._image_data is None:
            raise Exception("image data is None")

        return self._image_data

    @image_data.setter
    def image_data(self, value: ndarray):
        self._image_data = value
