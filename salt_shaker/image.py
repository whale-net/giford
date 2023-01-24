from __future__ import annotations  # py>=3.7 - make factory return type hints work

import os
import copy

import numpy as np
from skimage.io import imread, imsave

from salt_shaker.raw_data import RawDataFrame
from salt_shaker.image_formats import ImageFormat


class Image:
    """
    simple wrapper for images

    the internal image format is a 3 dimensional uint8 array of height x width x 4 (depth)
        (in the future, maybe we can make 24bit array?)
    depth is currently hardcoded to 4 for rgba

    """

    @staticmethod
    def create_from_file(file_path: str, fmt: ImageFormat = None) -> Image:
        if not ImageFormat:
            # todo pickup format from file name
            raise Exception("optional argument temporarily mandatory")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"file doesn't exist: [{file_path}]")

        # todo - handle more image formats, for now whatever sci-kit has is what is used
        # this will break when scikit returns something stupid
        nd_arr = imread(file_path)
        # (for now) using scikit image makes RGBA arrays
        return Image.create_from_ndarray(nd_arr, ImageFormat.RGBA)

    @staticmethod
    def create_from_ndarray(nd_arr: np.ndarray, fmt: ImageFormat = None) -> Image:
        # hopefully this saves head scratching
        if not isinstance(nd_arr, np.ndarray):
            raise Exception("nd_arr not type ndarray")

        img_data = RawDataFrame(nd_arr=nd_arr)
        img = Image(fmt=fmt, raw_frame=img_data, _created_from_factory=True)
        return img

    @staticmethod
    def create_from_url(url: str, fmt: ImageFormat = None) -> Image:
        # todo URL support?
        raise NotImplementedError()

    @staticmethod
    def create_from_bytes(byte_data: bytes, fmt: ImageFormat = None) -> Image:
        # TODO byte datatype type hint
        # img_nd_arr = np.frombuffer(byte_data, dtype=np.uint8)
        #        img_nd_arr = np.reshape(img_nd_arr, (height, width, depth))
        return Image(fmt=fmt, byte_data=byte_data, _created_from_factory=True)

    @staticmethod
    def create_from_raw_data_frame(frame: RawDataFrame) -> Image:
        # all raw data frames are RGBA format
        return Image.create_from_ndarray(frame.data_arr, fmt=ImageFormat.RGBA)

    @property
    def raw_frame(self) -> RawDataFrame:
        if self.format != ImageFormat.RGBA:
            raise Exception(
                f"unable to set image data, unsupported format {self.format}"
            )
        if self._raw_frame is None:
            raise Exception("image data is None")

        return self._raw_frame

    @raw_frame.setter
    def raw_frame(self, value: RawDataFrame):
        if self.format != ImageFormat.RGBA:
            raise Exception(
                f"unable to set image data, unsupported format {self.format}"
            )
        self._raw_frame = value

    @property
    def img_byte_data(self):
        """
        data that allows you to write image to disk
        will contain image headers and the like
        """
        if self.format == ImageFormat.GIF:
            return self._byte_data
        else:
            raise Exception(f"unspoorted byte data format{self.format}")

    @property
    def format(self) -> ImageFormat:
        return self._format

    def __init__(
        self,
        fmt: ImageFormat,
        raw_frame: RawDataFrame = None,
        byte_data: bytes = None,
        _created_from_factory: bool = False,
    ):
        if not _created_from_factory:
            raise Exception(
                "please use a factory method like Image.create_from_ndarray()"
            )

        self._format = fmt
        # todo - does this need better type checking
        if not isinstance(self.format, ImageFormat):
            raise Exception("you must provide a valid format")

        # kind of recreating factory pattern, but it cleans up __init__
        # todo - revisit how we create images
        # factory method is effectively re-implemented through the constructor breakout on format
        # may need to come after deciding how to determine formats and their properties
        if self.format == ImageFormat.RGBA:
            self.__create_from_rgba(raw_frame)
        elif self.format == ImageFormat.GIF:
            self.__create_from_bytes(byte_data)

        self._raw_frame = raw_frame

    def __create_from_rgba(self, raw_frame: RawDataFrame):
        if not isinstance(raw_frame, RawDataFrame):
            raise Exception("raw_frame not RawDataFrame")

        self._raw_frame = raw_frame

    def __create_from_bytes(self, byte_data: bytes):
        if not isinstance(byte_data, bytes):
            raise Exception("raw_frame not RawDataFrame")
        self._byte_data = byte_data

    def write_to_file(self, file_path, overwrite=True):
        if os.path.isdir(file_path):
            raise Exception(f"provided path is a directory [{file_path}]")

        if not overwrite and os.path.exists(file_path):
            raise FileExistsError(f"file already exists [{file_path}]")

        if self.format == ImageFormat.GIF:
            with open(file_path, "wb") as fd:
                fd.write(self.img_byte_data)
        elif self.format == ImageFormat.RGBA:
            imsave(file_path, self.raw_frame.as_3d_ndarray())
        else:
            raise NotImplementedError(f"[{self.format}] write not supported")

    def clone(self):
        return copy.deepcopy(self)
