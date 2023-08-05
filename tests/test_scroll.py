import os

import pytest

from giford.image import Image
from giford.frame_batch import FrameBatch
from tests.util import BASELINE_DIRECTORY, compare_file_hash

from giford.image_actions.gif import Gifify
from giford.image_actions.scroll import Scroll
from giford.image_actions.reshape import Reshape, ReshapeMethod


# TODO - test_scroll various step sizes/scroll_multipliers
# TODO - test various scroll scroll combinations
@pytest.mark.parametrize(
    "is_wrap, is_reverse", [(False, False), (False, True), (True, False), (True, True)]
)
def test_scroll(
    temp_output_gif: str, orange_image: Image, is_wrap: bool, is_reverse: bool
):
    # test scroll combinations
    baseline = os.path.join(
        BASELINE_DIRECTORY, f"test_scroll_wrap_{is_wrap}_reverse_{is_reverse}.gif"
    )

    batch = FrameBatch()
    batch.add_image(orange_image)

    # shrink image so test is faster
    r = Reshape()
    batch = r.process(batch, reshape_method=ReshapeMethod.RESIZE)  # idk why resize

    s = Scroll()
    batch = s.process(
        batch,
        is_wrap_image=is_wrap,
        is_horizontal_direction_negative=is_reverse,
        is_vertical_direction_negative=is_reverse,
        num_frames=15,
        is_horizontal_scroll=True,
        is_vertical_scroll=True,
    )

    g = Gifify(default_framerate=10)
    g.process(batch).write_to_file(temp_output_gif)

    assert compare_file_hash(baseline, temp_output_gif)
