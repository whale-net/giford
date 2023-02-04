from typing import Any, TYPE_CHECKING, Union

from giford.action import Action

# if TYPE_CHECKING:
from giford.frame_batch import FrameBatch
from giford.image import Image


class ImageAction(Action):
    """
    really no reason for this class
    just kind of feels like a good idea for better inheritance tree shape
    """

    def __init__(self):
        pass

    def process(self, *args, **kwargs) -> Union[Image, FrameBatch]:
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


class ExportImageAction(ImageAction):
    def __init__(self):
        super().__init__()

    def process(self, input_batch: FrameBatch, *args, **kwargs) -> Image:
        """
        takes in image(s), produces anything
        """


class ImportImageAction(ImageAction):
    def __init__(self):
        super().__init__()

    def process(self, input_image: Image, *args, **kwargs) -> FrameBatch:
        """
        takes in anything, produces image(s)
        """
        pass
