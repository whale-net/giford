from __future__ import annotations  # py>=3.7

import copy

# this prevents circular imports, going to bandaid whenever needed because this is dumb
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from giford.frame_wrapper import AbstractFrameWrapper, SingleImage
    from giford.raw_data import RawDataFrame


class FrameBatch:
    """
    class for sending and receiving data to ImageActions
    """

    @property
    def frames(self) -> list[RawDataFrame]:
        return self._frames

    def __init__(self):
        self._frames: list[RawDataFrame] = []
        pass

    def add_frame(self, frame: RawDataFrame):
        self.frames.append(frame.clone())

        # allow chaining these functions together
        return self

    def add_batch(self, batch: FrameBatch):
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

    def clone(self):
        return copy.deepcopy(self)

    def cloned_frames(self):
        """
        returns cloned copy of all frames in batch

        useful for implementing image actions
        TODO - self.readonly flag and clone on get_copy
        """
        for frame in self.frames:
            yield frame.clone()

    def size(self):
        return len(self.frames)

    def is_empty(self):
        return self.size() == 0

    def create_from_frame_wrapper(wrapper: AbstractFrameWrapper):
        batch = FrameBatch()
        for rdf in wrapper.raw_data_frames:
            batch.add_frame(rdf)
        return batch

    def create_from_single_image(simg: SingleImage):
        """
        same as create_from_frame_wrapper, but here for convenience

        :param simg: single image
        """
        return FrameBatch.create_from_frame_wrapper(simg)
