import os

import pytest

from giford.frame import FrameBatch
from giford.action import Reshape, ReshapeMethod
from tests.util import BASELINE_DIRECTORY, save_batch_and_compare


# TODO ReshapeMethod.DOWNSCALE
# TODO parametrize scale
@pytest.mark.parametrize(
    "reshape_method", [ReshapeMethod.RESCALE, ReshapeMethod.RESIZE]
)
def test_reshape(
    temp_output_png, orange_image_batch: FrameBatch, reshape_method: ReshapeMethod
):
    baseline = os.path.join(
        BASELINE_DIRECTORY, f"test_reshape_method_{reshape_method.name}.png"
    )

    r = Reshape()
    output_batch = r.process(orange_image_batch, reshape_method, 0.25)

    assert save_batch_and_compare(baseline, output_batch, temp_output_png)
