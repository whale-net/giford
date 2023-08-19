import enum
import os
from typing import Optional

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

    DEFAULT_FORMAT = SingleImageFormat.PNG

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

    def load(self, path: str) -> None:
        if not os.path.exists(path):
            raise FileNotFoundError()

        # maybe there is a use case for loading over an existing file
        # but for now im just going to assume it's done in error
        if len(self.raw_data_frames) > 0:
            raise Exception("cannot load second time")

        # using PIL/pillow to load images
        # TODO - always convert to RGBA?
        pimg = PillowImage.open(path)  # .convert('RGBA')

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
        path: str,
        target_format: SingleImageFormat = SingleImageFormat.UNKNOWN,
        overwrite_existing: bool = True,
    ) -> None:
        if target_format == SingleImageFormat.UNKNOWN:
            raise Exception("UNKNOWN cannot be saved")

        # should rename to error_if_exists?
        if not overwrite_existing and os.path.exists(path):
            raise Exception(f"file at this path already exists [{path}]")

        if len(self.raw_data_frames) == 0:
            raise Exception("no image data to write")

        if target_format == SingleImageFormat.UNKNOWN:
            # if unknown, letting pillow figure it out based on file extension
            pass
        else:
            target_format = self.format
        

        # using PIL/pillow to save images
        # TODO WHAT FORMATS DOES THIS SUPPORT, how does it interpret datatype
        # https://github.com/python-pillow/Pillow/blob/a5b025629023477ec62410ce77fd717c372d9fa2/src/PIL/Image.py#L3119
        rdf = self.raw_data_frames[0]

        # pick up copy of data frame in case we need to convert type on export
        # keep whatever RDF dtype to preserve quality
        img_nd_arr = rdf.get_data_arr(is_return_reference=False)

        img_nd_arr = RawDataFrame.convert_data_arr(img_nd_arr, target_dtype=np.uint8)

        pimg = PillowImage.fromarray(img_nd_arr)
        pimg.save(path, format=target_format.name)

    @staticmethod
    def create_from_frame(
        raw_data_frame: RawDataFrame, target_format: SingleImageFormat = DEFAULT_FORMAT
    ) -> 'SingleImage':
        img = SingleImage()
        img._add_raw_data_frame(raw_data_frame)
        img.format = target_format
        return img

    @staticmethod
    def create_from_frame_batch(
        batch: FrameBatch, target_format: SingleImageFormat = DEFAULT_FORMAT
    ) -> 'SingleImage':
        if batch.is_empty():
            raise Exception("batch is empty")
        if batch.size() > 1:
            raise Exception(f"batch is too large [{batch.size()}]")

        return SingleImage.create_from_frame(batch.frames[0])
