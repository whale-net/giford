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

def test_crop_negative(
    orange_image_batch: FrameBatch,
):
    c = Crop()
    with pytest.raises(Exception):
        output_batch = c.process(
            orange_image_batch,
            crop_px=-100
        )

def test_crop_zero_px(
    temp_output_png,
    orange_image_batch: FrameBatch,
):
    
    baseline = os.path.join(
        BASELINE_DIRECTORY,
        f"test_crop/test_crop_zero_px.png",
    )

    c = Crop()
    output_batch = c.process(
        orange_image_batch,
        crop_px=0
    )

    assert save_batch_and_compare(baseline, output_batch, temp_output_png)
