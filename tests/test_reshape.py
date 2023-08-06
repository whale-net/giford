import os

import pytest

from giford.image import Image
from giford.frame_batch import FrameBatch
from giford.image_actions.reshape import Reshape, ReshapeMethod
from tests.util import BASELINE_DIRECTORY, compare_file_hash


# TODO ReshapeMethod.DOWNSCALE
# TODO parametrize scale
@pytest.mark.skip('rewrite')
@pytest.mark.parametrize(
    "reshape_method", [ReshapeMethod.RESCALE, ReshapeMethod.RESIZE]
)
def test_reshape(temp_output_png, single_orange_image, reshape_method: ReshapeMethod):
    baseline = os.path.join(
        BASELINE_DIRECTORY, f"test_reshape_method_{reshape_method.name}.png"
    )

    batch = FrameBatch()
    batch.add_image(single_orange_image)
    r = Reshape()

    batch = r.process(batch, reshape_method, 0.25)
    Image.create_from_frame_batch(batch).write_to_file(temp_output_png)

    assert compare_file_hash(baseline, temp_output_png)
