from typing import Any, TYPE_CHECKING, Union

from giford.action import Action

# if TYPE_CHECKING:
from giford.frame_batch import FrameBatch


class ImageAction(Action):
    """
    really no reason for this class
    just kind of feels like a good idea for better inheritance tree shape
    """

    def __init__(self):
        pass

    def process(self, *args, **kwargs) -> FrameBatch:
        """
        takes in image(s), produces image(s)
        """
        pass


class ChainImageAction(ImageAction):
    def __init__(self):
        super().__init__()

    def process(self, input_batch: FrameBatch, *args, **kwargs) -> FrameBatch:
        """
        takes in image(s), produces image(s)
        """
        pass
