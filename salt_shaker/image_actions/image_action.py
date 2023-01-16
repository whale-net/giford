from abc import ABC, abstractmethod

from salt_shaker.image import Image


class ImageAction(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def process(image_input: Image | list[Image]) -> Image | list[Image]:
        """
        takes in image(s), produces image(s)
        """
        pass

    @staticmethod
    def _listify_input(image_input: Image | list[Image]) -> list[Image]:
        if not isinstance(image_input, list):
            image_input = [image_input]
        return image_input
