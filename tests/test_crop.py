import os
import pytest

from giford.action import Crop
from giford.frame import FrameBatch

from tests.util import BASELINE_DIRECTORY, save_batch_and_compare


@pytest.mark.parametrize(
    "crop_px, is_horizontal, is_vertical",
    [
        (50, False, False),
        (50, False, True),
        (50, True, False),
        (50, True, True),
        (150, True, True),
    ],
)
def test_crop(
    temp_output_png,
    orange_image_batch: FrameBatch,
    crop_px: int,
    is_horizontal: bool,
    is_vertical: bool,
):
    baseline = os.path.join(
        BASELINE_DIRECTORY,
        f"test_crop/test_crop_{crop_px}_{is_horizontal}_{is_vertical}.png",
    )

    c = Crop()
    output_batch = c.process(
        orange_image_batch,
        crop_px=crop_px,
        is_horizontal=is_horizontal,
        is_vertical=is_vertical,
    )

    assert save_batch_and_compare(baseline, output_batch, temp_output_png)
