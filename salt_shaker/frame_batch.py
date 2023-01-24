from __future__ import annotations  # py>=3.7

# this prevents circular imports, going to bandaid whenever needed because this is dumb
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from salt_shaker.image import Image
    from salt_shaker.raw_data import RawDataFrame


class FrameBatch:
    """
    class for sending and receiving data to ImageActions
    """

    @property
    def frames(self):
        return self._frames

    def __init__(self):
        self._frames: list[RawDataFrame] = []
        pass

    def add_frame(self, frame: RawDataFrame):
        self.frames.append(frame.clone())

    def add_image(self, img: Image):
        # TODO - cloning here is safe but expensive, can this be improved?
        self.add_frame(img.raw_frame)

    def add_batch(self, batch: FrameBatch):
        # self.images += batch.images
        # need to add_img, so we clone properly
        for frame in batch.frames:
            self.add_frame(frame)

    def is_all_frame_same_shape(self, is_check_depth: bool = False) -> bool:
        """
        returns true if all images are the same size
        """
        if len(self.frames) == 1:
            return True

        base_frame = self.frames[0]
        for compare_frame in self.frames[1:]:
            if not base_frame.is_same_shape(compare_frame, is_check_depth):
                return False

        return True