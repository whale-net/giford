import abc
from typing import BinaryIO

from giford.frame.frame_batch import FrameBatch
from giford.frame.raw_data import RawDataFrame


class AbstractImage(abc.ABC):
    """
    container for raw data frames
    also acts as interface from dataframe <-> file on disk


    :param abc: this is an abstract base class
    """

    def __init__(self) -> None:
        self.raw_data_frames: list[RawDataFrame] = []

    @abc.abstractmethod
    def load(self, in_file: str | BinaryIO) -> None:
        pass

    @abc.abstractmethod
    def save(self, out_file: str | BinaryIO) -> None:
        """
        save image data to out_file

        :param out_file: file path or file pointer
        """
        pass

    @classmethod
    @abc.abstractmethod
    def create_from_frame_batch(cls, batch: FrameBatch) -> "AbstractImage":
        pass
