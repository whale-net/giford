from giford.frame.frame_batch import FrameBatch
from giford.frame.raw_data import RawDataFrame

from .abstract_frame_action import AbstractFrameAction


class Crop(AbstractFrameAction):
    def __init__(self) -> None:
        super().__init__()

    def process(
        self,
        input_batch: FrameBatch,
        crop_px: int = 1,
        is_horizontal: bool = True,
        is_vertical: bool = True,
    ) -> FrameBatch:
        """
        crop images

        :param input_batch: input batch
        :param crop_px: number of pixels to crop, defaults to 1
        :param is_horizontal: crop horizontally, defaults to True
        :param is_vertical: crop vertically, defaults to True
        :return: _description_
        """

        if crop_px < 0:
            raise Exception("crop_px is negative, use Reshape instead")

        if crop_px == 0:
            return input_batch.clone()

        output_batch = FrameBatch()
        for frame in input_batch.cloned_frames():
            np_arr = frame.get_data_arr(is_return_reference=True)

            # TODO - error handling, crop_px < len(np_arr)
            # TODO - error handling, too big of crop
            if is_vertical and is_horizontal:
                np_arr = np_arr[crop_px:-crop_px, crop_px:-crop_px]
            elif is_vertical:
                np_arr = np_arr[crop_px:-crop_px]
            elif is_horizontal:
                np_arr = np_arr[0 : len(np_arr), crop_px:-crop_px]

            output_batch.add_frame(RawDataFrame(np_arr))

        return output_batch
