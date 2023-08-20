import enum
import io
import os
from typing import Optional, BinaryIO

import numpy as np

# aliasing to avoid confusion
from PIL import Image as PillowImage

from giford.frame.frame_batch import FrameBatch
from giford.frame.raw_data import RawDataFrame
from giford.image.abstract_image import AbstractImage


class SingleImageFormat(enum.Enum):
    """
    currently supported single image formats
    using the same name as PIL/pillow.format

    should be easy to add more
    """

    UNKNOWN = 0
    PNG = 1
    # JPG = 2 # TODO


class SingleImage(AbstractImage):
    """
    represents a single, non-animated, image (png, jpg)

    datatypes of underlying image data is handled by RawDataFrame
    """

    DEFAULT_FORMAT: SingleImageFormat = SingleImageFormat.PNG

    # replace with strenum in 3.11
    _FORMAT_NAME_MAP = {fmt.name: fmt for fmt in SingleImageFormat}

    def __init__(self) -> None:
        super().__init__()

        self.format: SingleImageFormat = SingleImageFormat.UNKNOWN

    @property
    def raw_data_frame(self) -> RawDataFrame:
        if len(self.raw_data_frames) == 0:
            raise Exception("image is empty")
        return self.raw_data_frames[0]

    def _add_raw_data_frame(self, frame: RawDataFrame) -> None:
        """
        helper function to make sure rdf list never grows beyond one item
        only meant to be called during initialization

        :param frame: raw data frame to add to this image
        """
        if len(self.raw_data_frames) > 0:
            raise Exception("unable to add frame to SingleImage")
        self.raw_data_frames.append(frame)

    def load(self, in_file: str | BinaryIO) -> None:
        if isinstance(in_file, str) and not os.path.exists(in_file):
            raise FileNotFoundError()

        # maybe there is a use case for loading over an existing file
        # but for now im just going to assume it's done in error
        if len(self.raw_data_frames) > 0:
            raise Exception("cannot load second time")

        # using PIL/pillow to load images
        # TODO - always convert to RGBA?
        pimg = PillowImage.open(in_file)  # .convert(mode='RGBA')

        # TODO
        # pimg.info will have an icc_profile, do we want this?

        # TODO - consider passing formats into open instead
        if pimg.format not in SingleImage._FORMAT_NAME_MAP:
            raise Exception(f"provided format not supported [{pimg.format}]")
        self.format = SingleImage._FORMAT_NAME_MAP[pimg.format]

        # NOTE - trusting whatever type I get out of this
        # 4 band PNG uint8 so far, really should just support whatever though
        img_ndarr = np.asarray(pimg)
        self._add_raw_data_frame(RawDataFrame(img_ndarr))

    def save(
        self,
        target_file: str | BinaryIO,
        target_format: Optional[SingleImageFormat] = None,
        overwrite_existing: bool = True,  # TODO - false?
    ) -> None:
        if target_format == SingleImageFormat.UNKNOWN:
            raise Exception("UNKNOWN cannot be saved")

        if len(self.raw_data_frames) == 0:
            raise Exception("no image data to write")

        if target_format is None:
            target_format = self.format

        # using PIL/pillow to save images
        # still not sure WHAT FORMATS THIS SUPPORTs, how does it interpret datatype
        # https://github.com/python-pillow/Pillow/blob/a5b025629023477ec62410ce77fd717c372d9fa2/src/PIL/Image.py#L3119
        # but also not sure it matters because of conversion to uint8 anyways
        # only issue would be shape, and there is already a plan to convert to RGBA shape always

        # pick up copy of data frame in case we need to convert type on export
        img_nd_arr = self.raw_data_frames[0].get_data_arr(is_return_reference=False)
        img_nd_arr = RawDataFrame.convert_data_arr(img_nd_arr, target_dtype=np.uint8)

        pimg = PillowImage.fromarray(img_nd_arr)
        pimg.save(target_file, format=target_format.name)

    @classmethod
    def create_from_frame(
        cls,
        raw_data_frame: RawDataFrame,
        target_format: SingleImageFormat = DEFAULT_FORMAT,
    ) -> "SingleImage":
        img = cls()
        img._add_raw_data_frame(raw_data_frame)
        img.format = target_format
        return img

    @classmethod
    def create_from_frame_batch(
        cls, batch: FrameBatch, target_format: SingleImageFormat = DEFAULT_FORMAT
    ) -> "SingleImage":
        if batch.is_empty():
            raise Exception("batch is empty")
        if batch.size() > 1:
            raise Exception(f"batch is too large [{batch.size()}]")

        return cls.create_from_frame(batch.frames[0])
