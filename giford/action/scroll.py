from giford.action.abstract_frame_action import AbstractFrameAction
from giford.action.translate import Translate
from giford.frame.frame_batch import FrameBatch


class Scroll(AbstractFrameAction):
    def __init__(self) -> None:
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
        is_skip_clean_frame: bool = False,
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
        :param is_skip_clean_frame: skip the last frame
        :return:
        """
        if not is_horizontal_scroll and not is_vertical_scroll:
            return input_batch.clone()

        if num_frames is None or num_frames <= 2:
            # num_frames must be >= 2 else it's just the image again
            raise Exception(f"num_frames must be >=2. num_frames=[{num_frames}]")

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
                raise Exception(
                    "horizontal_scroll_multiplier must be 1.0 if wrap is false"
                )
            if is_vertical_scroll and vertical_scroll_multiplier != 1.0:
                raise Exception(
                    "vertical_scroll_multiplier must be 1.0 if wrap is false"
                )
            if scroll_count != 1:
                # if you need to scroll more than 1 time, duplicate the batch
                raise Exception("cannot scroll more than 1 time if wrap is false")

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
            if is_skip_clean_frame:
                step_divisor = num_frames
            else:
                step_divisor = num_frames - 1

            h_scroll_step_size_px = int(
                2 * horizontal_scroll_multiplier * frame.width // step_divisor
            )
            v_scroll_step_size_px = int(
                2 * vertical_scroll_multiplier * frame.height // step_divisor
            )

            # scale number of frames by number of times we want to scroll
            # useful when scroll multiplier < 1
            # but will be tricky to use
            num_frames_to_generate = num_frames * scroll_count
            for i in range(num_frames_to_generate):
                if is_horizontal_scroll:
                    h_shift_px = Scroll._calculate_shift(
                        is_horizontal_direction_negative,
                        frame.width,
                        i,
                        h_scroll_step_size_px,
                    )
                else:
                    h_shift_px = 0

                if is_vertical_scroll:
                    v_shift_px = Scroll._calculate_shift(
                        is_vertical_direction_negative,
                        frame.height,
                        i,
                        v_scroll_step_size_px,
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

    @staticmethod
    def _calculate_shift(
        is_direction_negative: int, size: int, increment: int, step_size: int
    ) -> int:
        """
        produces shift amount

        :param sign:
        :param size:
        :param increment:
        :param step_size:
        :return:
        """
        if is_direction_negative:
            shift_px = size - (increment * step_size)
        else:
            shift_px = -size + (increment * step_size)

        return shift_px
