from skimage import transform

from salt_shaker.image_actions.image_action import ChainImageAction
from salt_shaker.image_actions.translate import Translate
from salt_shaker.frame_batch import FrameBatch
from salt_shaker.raw_data import RawDataFrame


class Scroll(ChainImageAction):
    def __init__(self):
        super().__init__()

    def process(
        self,
        input_batch: FrameBatch,
        num_frames: int = 60,
        is_wrap_image: bool = False,
        scroll_count: int = 1,
        is_horizontal_scroll: bool = False,
        horizontal_scroll_multiplier: float = 1.0,
        is_horizontal_direction_negative: bool = False,
        is_vertical_scroll: bool = False,
        vertical_scroll_multiplier: float = 1.0,
        is_vertical_direction_negative: bool = False,

    ) -> FrameBatch:
        """
        produces series of images to imitate scrolling

        scroll: selling lobbies 250gp

        :param input_batch: FrameBatch
        :param num_frames: number of frames to produce for a single scroll through
        :param is_wrap_image: wrap image instead of clearing it out
        :param scroll_count: scaling factor for number of frames to produce, useful for multipliers < 1
        :param is_horizontal_scroll: do horizontal scroll
        :param horizontal_scroll_multiplier: amount the image should move horizontally during a single scroll
        :param is_horizontal_direction_negative: reverse horizontal scroll direction
        :param is_vertical_scroll: do vertical scroll
        :param vertical_scroll_multiplier: amount the image should move vertically during a single scroll
        :param is_vertical_direction_negative: reverse vertical scroll direction
        :return:
        """
        if not is_horizontal_scroll and not is_vertical_scroll:
            return input_batch.clone()

        if num_frames is None or num_frames <= 0:
            raise Exception(
                f"num_frames must be greater than 0. num_frames=[{num_frames}]"
            )

        if is_horizontal_scroll and horizontal_scroll_multiplier <= 0.0:
            raise Exception(
                f"horizontal_scroll_count must be greater than 0. horizontal_scroll_count=[{horizontal_scroll_multiplier}]"
            )

        if is_vertical_scroll and vertical_scroll_multiplier <= 0.0:
            raise Exception(
                f"vertical_scroll_count must be greater than 0. vertical_scroll_count=[{vertical_scroll_multiplier}]"
            )

        # handle is_wrap_image input, changes a bit
        if not is_wrap_image:
            if is_horizontal_scroll and horizontal_scroll_multiplier != 1.0:
                raise Exception('horizontal_scroll_multiplier must be 1.0 if wrap is false')
            if is_vertical_scroll and vertical_scroll_multiplier != 1.0:
                raise Exception('vertical_scroll_multiplier must be 1.0 if wrap is false')
            if scroll_count != 1:
                # if you need to scroll more than 1 time, duplicate the batch
                raise Exception('cannot scroll more than 1 time if wrap is false')


        # this is opposite what you'd think, but is correct
        if is_horizontal_direction_negative:
            h_direction_sign = 1
        else:
            h_direction_sign = -1

        # this is opposite what you'd think, but is correct
        if is_vertical_direction_negative:
            v_direction_sign = 1
        else:
            v_direction_sign = -1

        output_batch = FrameBatch()

        # todo - empty frames around beginning and end
        # todo - create empty frame util in rawdataframe
        t = Translate()
        for frame in input_batch.frames:
            # in order to completely scroll across the image
            # we need to travel 2x the distance of the image
            # let [X] represent our image
            # let {[X]} represent the image being displayed
            # we need to do this: [X]{[ ]}[ ] -> [ ]{[X]}[ ] -> [ ]{[ ]}[X]
            h_scroll_step_size_px = int(
                    2 * horizontal_scroll_multiplier * frame.width // num_frames
            )
            v_scroll_step_size_px = int(
                    2 * vertical_scroll_multiplier * frame.height // num_frames
            )

            # scale number of frames by number of times we want to scroll
            # useful when scroll multiplier < 1
            # but will be tricky to use
            num_frames_to_generate = num_frames * scroll_count
            for i in range(num_frames_to_generate):

                if is_horizontal_scroll:
                    if is_horizontal_direction_negative:
                        h_shift_px = h_direction_sign * frame.width - (
                                i * h_scroll_step_size_px
                        )
                    else:
                        h_shift_px = h_direction_sign * frame.width + (
                            i * h_scroll_step_size_px
                        )
                else:
                    h_shift_px = 0

                if is_vertical_scroll:
                    if is_vertical_direction_negative:
                        v_shift_px = v_direction_sign * frame.height - (
                                i * v_scroll_step_size_px
                        )
                    else:
                        v_shift_px = v_direction_sign * frame.height + (
                                 i * v_scroll_step_size_px
                             )
                else:
                    v_shift_px = 0

                output_batch.add_batch(
                    t.process(
                        input_batch,
                        horizontal_shift_px=h_shift_px,
                        vertical_shift_px=v_shift_px,
                        wrap_image=is_wrap_image,
                    )
                )

        return output_batch
