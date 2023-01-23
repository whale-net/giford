from typing import Any

from salt_shaker.action import Action
from salt_shaker.image_batch import ImageBatch


class ImageAction(Action):
    """
    really no reason for this class
    just kind of feels like a good idea for better inheritance tree shape
    """

    def __init__(self):
        pass

    def process(self, *args, **kwargs) -> Any:
        """
        takes in image(s), produces image(s)
        """
        pass


class ChainImageAction(ImageAction):
    def __init__(self):
        pass

    def process(self, input_batch: ImageBatch) -> ImageBatch:
        """
        takes in image(s), produces image(s)
        """
        pass


class ExportImageAction(ImageAction):
    def __init__(self):
        pass

    def process(self, input_batch: ImageBatch) -> Any:
        """
        takes in image(s), produces anything
        """


class ImportImageAction(ImageAction):
    def __init__(self):
        pass

    def process(self, *args, **kwargs) -> ImageBatch:
        """
        takes in anything, produces image(s)
        """
        pass
