from __future__ import annotations  # py>=3.7

import copy

# this prevents circular imports, going to bandaid whenever needed because this is dumb
from typing import TYPE_CHECKING, Self, Iterable

if TYPE_CHECKING:
    from giford.image import AbstractImage, SingleImage
    from giford.frame.raw_data import RawDataFrame


class FrameBatch:
    """
    class for sending and receiving data to ImageActions
    """

    @property
    def frames(self) -> list[RawDataFrame]:
        return self._frames

    def __init__(self) -> None:
        self._frames: list[RawDataFrame] = []
        pass

    def reverse_batch(self) -> None:
        self._frames.reverse()

    def add_frame(self, frame: RawDataFrame) -> Self:
        self.frames.append(frame.clone())

        # allow chaining these functions together
        return self

    def add_batch(self, batch: FrameBatch) -> Self:
        # self.images += batch.images
        # need to add_img, so we is_clone properly
        for frame in batch.frames:
            self.add_frame(frame)

        # allow chaining these functions together
        return self

    def is_all_frame_same_shape(self, is_check_depth: bool = False) -> bool:
        """
        returns true if all images are the same size
        """
        if self.size() == 1:
            return True

        base_frame = self.frames[0]
        for compare_frame in self.frames[1:]:
            if not base_frame.is_same_shape(compare_frame, is_check_depth):
                return False

        return True

    def clone(self) -> "FrameBatch":
        return copy.deepcopy(self)

    def cloned_frames(self) -> Iterable[RawDataFrame]:
        """
        returns cloned copy of all frames in batch

        useful for implementing image actions
        TODO - self.readonly flag and clone on get_copy
        """
        for frame in self.frames:
            yield frame.clone()

    def size(self) -> int:
        return len(self.frames)

    def is_empty(self) -> bool:
        return self.size() == 0

    @classmethod
    def create_from_image(cls, img: AbstractImage) -> "FrameBatch":
        batch = cls()
        for rdf in img.raw_data_frames:
            batch.add_frame(rdf)
        return batch
