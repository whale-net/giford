import os

import pytest

from giford.frame import FrameBatch
from giford.action import Zoom, ZoomMany
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


@pytest.mark.parametrize("zoom_step_px, num_steps", [(0, 1), (20, 3), (50, 5)])
def test_zoom_many(
    temp_out_png_generator,
    orange_image_batch: FrameBatch,
    zoom_step_px: int,
    num_steps: int,
):
    zm = ZoomMany()
    output_batch = zm.process(
        orange_image_batch, zoom_step_size_px=zoom_step_px, num_steps=num_steps
    )

    for step_idx, frame in enumerate(output_batch.frames):
        temp_batch = output_batch.create_from_frame(frame)
        baseline = os.path.join(
            BASELINE_DIRECTORY,
            "test_zoom",
            f"test_zoom_many_{zoom_step_px}_{step_idx}.png",
        )
        temp_output_png = next(temp_out_png_generator)

        assert save_batch_and_compare(baseline, temp_batch, temp_output_png)
