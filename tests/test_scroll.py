import os

import pytest

from giford.image import MultiImage
from giford.frame import FrameBatch
from giford.action import Scroll, Reshape, ReshapeMethod

from tests.util import BASELINE_DIRECTORY, compare_image_files


# TODO - test_scroll various step sizes/scroll_multipliers
# TODO - test various scroll scroll combinations
@pytest.mark.parametrize(
    "is_wrap, is_reverse", [(False, False), (False, True), (True, False), (True, True)]
)
def test_scroll(
    temp_output_gif: str,
    orange_image_batch: FrameBatch,
    is_wrap: bool,
    is_reverse: bool,
):
    # test scroll combinations
    baseline = os.path.join(
        BASELINE_DIRECTORY, f"test_scroll_wrap_{is_wrap}_reverse_{is_reverse}.gif"
    )

    # shrink image so test is faster
    r = Reshape()
    orange_image_batch = r.process(
        orange_image_batch, reshape_method=ReshapeMethod.RESIZE
    )  # idk why resize

    s = Scroll()
    output_batch = s.process(
        orange_image_batch,
        is_wrap_image=is_wrap,
        is_horizontal_direction_negative=is_reverse,
        is_vertical_direction_negative=is_reverse,
        num_frames=15,
        is_horizontal_scroll=True,
        is_vertical_scroll=True,
    )

    mimg = MultiImage.create_from_frame_batch(output_batch)
    mimg.save(temp_output_gif)

    assert compare_image_files(baseline, temp_output_gif)
