import abc

from giford.frame.frame_batch import FrameBatch
from giford.frame.raw_data import RawDataFrame


class AbstractImage(abc.ABC):
    """
    container for raw data frames
    also acts as interface from dataframe <-> file on disk


    :param abc: this is an abstract base class
    """

    def __init__(self):
        self.raw_data_frames: list[RawDataFrame] = []

    @abc.abstractmethod
    def load(self, path):
        pass

    @abc.abstractmethod
    def save(self, path):
        pass

    @abc.abstractstaticmethod
    def create_from_frame_batch(self, batch: FrameBatch) -> 'AbstractImage':  # one day 3.11 -> Self:
        pass
