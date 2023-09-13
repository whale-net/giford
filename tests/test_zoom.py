import os

import pytest

from giford.frame import FrameBatch
from giford.action import Zoom
from tests.util import BASELINE_DIRECTORY, save_batch_and_compare


@pytest.mark.parametrize(
    "zoom_px",
    [(0), (50), (100), (200)],
)
def test_zoom_basic(temp_output_png: str, orange_image_batch: FrameBatch, zoom_px: int):
    baseline = os.path.join(
        BASELINE_DIRECTORY,
        "test_zoom",
        f"test_zoom_basic_{zoom_px}.png",
    )

    z = Zoom()

    output_batch = z.process(orange_image_batch, zoom_step_size_px=zoom_px)

    assert save_batch_and_compare(baseline, output_batch, temp_output_png)
