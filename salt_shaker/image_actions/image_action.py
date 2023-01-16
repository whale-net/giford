from abc import ABC, abstractmethod

from salt_shaker.image import Image


class ImageAction(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def process(self, image_input: Image | list[Image]) -> Image | list[Image]:
        """
        takes in image(s), produces image(s)
        """
        pass

    @staticmethod
    def _listify_input(image_input: Image | list[Image]) -> list[Image]:
        # convert variable input into list for ez process
        if not isinstance(image_input, list):
            image_input = [image_input]
        return image_input

    @staticmethod
    def _unlistify_output(image_input: list[Image]) -> Image | list[Image]:
        # unconvert list into variable output for ez process
        return image_input[0] if len(image_input) == 1 else image_input
