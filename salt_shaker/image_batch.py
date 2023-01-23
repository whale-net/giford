from __future__ import annotations  # py>=3.7
from salt_shaker.image import Image


class ImageBatch:
    """
    class for sending and receiving data to ImageActions
    """

    @property
    def images(self):
        return self._images

    def __init__(self):
        self._images: list[Image] = []
        pass

    def add_image(self, img: Image):
        # TODO - cloning here is safe but expensive, can this be improved?
        self.images.append(img.clone())

    def add_batch(self, batch: ImageBatch):
        #self.images += batch.images
        # need to add_img, so we clone properly
        for img in batch.images:
            self.add_image(img)
