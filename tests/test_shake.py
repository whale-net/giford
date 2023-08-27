import os

import pytest

from giford.frame import FrameBatch
from giford.action import Shake
from tests.util import BASELINE_DIRECTORY, save_batch_and_compare


# may be failing because of the weird frame buffer issue fixed in later ffmpeg versions
# need a way to test the raw data
@pytest.mark.skipif(
    os.getenv("CI") == "true", reason="failing on github, need to revisit"
)
def test_shake_default(temp_output_gif: str, orange_image_batch: FrameBatch):
    baseline = os.path.join(BASELINE_DIRECTORY, f"test_shake_default.gif")

    s = Shake()
    output_batch = s.process(orange_image_batch, 30, seed=1234)

    assert save_batch_and_compare(baseline, output_batch, temp_output_gif)


def test_shake_params(orange_image_batch: FrameBatch):
    s = Shake()

    # need args
    with pytest.raises(Exception):
        s.process()

    # need at least 1 frame
    with pytest.raises(Exception):
        s.process(input_batch=orange_image_batch, frame_count=0)

    # need something
    with pytest.raises(Exception):
        s.process(
            input_batch=orange_image_batch,
            frame_count=1,
            max_horizontal_move=None,
            max_vertical_move=None,
        )

    # need to None out move
    with pytest.raises(Exception):
        s.process(
            input_batch=orange_image_batch,
            frame_count=1,
            max_horizontal_shift_px=1,
            max_vertical_shift_px=1,
        )
