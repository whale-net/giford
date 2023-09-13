import os

import pytest

from giford.frame import FrameBatch
from giford.action import Reshape, ReshapeMethod
from tests.util import BASELINE_DIRECTORY, save_batch_and_compare


# TODO ReshapeMethod.DOWNSCALE
# TODO parametrize scale
@pytest.mark.parametrize(
    "reshape_method", [None, ReshapeMethod.RESCALE, ReshapeMethod.RESIZE]
)
def test_reshape(
    temp_output_png, orange_image_batch: FrameBatch, reshape_method: ReshapeMethod
):
    baseline = os.path.join(
        BASELINE_DIRECTORY,
        f"test_reshape/test_reshape_method_{reshape_method.name if reshape_method is not None else None}.png",
    )

    r = Reshape()
    output_batch = r.process(
        orange_image_batch, scale_factor=0.25, reshape_method=reshape_method
    )

    assert save_batch_and_compare(baseline, output_batch, temp_output_png)


@pytest.mark.parametrize(
    "v_px, h_px",
    [
        (50, 100),
        (100, 50),
        (100, 100),
        (500, 25),
        (25, 500),
    ],
)
def test_reshape_resize(
    temp_output_png, orange_image_batch: FrameBatch, v_px: int, h_px: int
):
    baseline = os.path.join(
        BASELINE_DIRECTORY, f"test_reshape/test_reshape_resize_{v_px}_{h_px}.png"
    )

    r = Reshape()
    output_batch = r.process(
        orange_image_batch,
        reshape_method=ReshapeMethod.RESIZE,
        veritcal_resize_px=v_px,
        horiztonal_resize_px=h_px,
    )

    assert save_batch_and_compare(baseline, output_batch, temp_output_png)
