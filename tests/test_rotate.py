import os
import pytest

from giford.action import Rotate, RotateMany
from giford.frame import FrameBatch

from tests.util import BASELINE_DIRECTORY, save_batch_and_compare


@pytest.mark.parametrize(
    "is_clockwise, rotate_degrees",
    [
        (False, 30),
        (False, 220),
        (True, 30),
        (True, 220),
    ],
)
def test_rotate(
    temp_output_png,
    orange_image_batch: FrameBatch,
    is_clockwise: bool,
    rotate_degrees: int,
):
    baseline = os.path.join(
        BASELINE_DIRECTORY, f"test_rotate_{is_clockwise}_{rotate_degrees}.png"
    )

    r = Rotate()
    output_batch = r.process(orange_image_batch, rotate_degrees, is_clockwise)

    assert save_batch_and_compare(baseline, output_batch, temp_output_png)
