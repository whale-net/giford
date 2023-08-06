import os

import pytest

from giford.image import Image
from giford.frame_batch import FrameBatch
from tests.util import BASELINE_DIRECTORY, compare_file_hash

from giford.image_actions.translate import Translate

@pytest.mark.skip('rewrite')
@pytest.mark.parametrize(
    "horizontal_px, vertical_px",
    [
        (-100, 0),
        (100, 0),
        (0, -100),
        (0, 100),
    ],
)
def test_translate_basic(
    temp_output_png: str, orange_image: Image, horizontal_px: int, vertical_px: int
):
    baseline = os.path.join(
        BASELINE_DIRECTORY,
        f"test_translate_basic_h_{horizontal_px}_v_{vertical_px}.png",
    )

    t = Translate()
    batch = FrameBatch()
    batch.add_image(orange_image)

    batch = t.process(
        batch, horizontal_shift_px=horizontal_px, vertical_shift_px=vertical_px
    )
    Image.create_from_frame_batch(batch).write_to_file(temp_output_png)

    assert compare_file_hash(baseline, temp_output_png)

@pytest.mark.skip('rewrite')
@pytest.mark.parametrize(
    "horizontal_px, vertical_px",
    [
        (-100, -100),
        (100, -100),
        (-100, 100),
        (100, 100),
    ],
)
def test_translate_complex(
    temp_output_png: str, orange_image: Image, horizontal_px: int, vertical_px: int
):
    baseline = os.path.join(
        BASELINE_DIRECTORY,
        f"test_translate_complex_h_{horizontal_px}_v_{vertical_px}.png",
    )

    t = Translate()
    batch = FrameBatch()
    batch.add_image(orange_image)

    batch = t.process(
        batch, horizontal_shift_px=horizontal_px, vertical_shift_px=vertical_px
    )
    Image.create_from_frame_batch(batch).write_to_file(temp_output_png)

    assert compare_file_hash(baseline, temp_output_png)
