import os

import pytest


from giford.frame import FrameBatch
from giford.action import Translate
from giford.util import Movement
from tests.util import BASELINE_DIRECTORY, save_batch_and_compare


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
    temp_output_png: str,
    orange_image_batch: FrameBatch,
    horizontal_px: int,
    vertical_px: int,
):
    baseline = os.path.join(
        BASELINE_DIRECTORY,
        f"test_translate_basic_h_{horizontal_px}_v_{vertical_px}.png",
    )

    t = Translate()

    output_batch = t.process(
        orange_image_batch,
        horizontal_shift_px=horizontal_px,
        vertical_shift_px=vertical_px,
    )

    assert save_batch_and_compare(baseline, output_batch, temp_output_png)


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
    temp_output_png: str,
    orange_image_batch: FrameBatch,
    horizontal_px: int,
    vertical_px: int,
):
    baseline = os.path.join(
        BASELINE_DIRECTORY,
        f"test_translate_complex_h_{horizontal_px}_v_{vertical_px}.png",
    )

    t = Translate()

    output_batch = t.process(
        orange_image_batch,
        horizontal_shift_px=horizontal_px,
        vertical_shift_px=vertical_px,
    )

    assert save_batch_and_compare(baseline, output_batch, temp_output_png)


# TODO use output generator once #60 is merged and remove overwrite
def test_translate_movement_basic_matrix(
    temp_output_png,
    basic_movement_matrix: list[Movement],
    orange_image_batch: FrameBatch,
):
    # uses matrix movement list
    t = Translate()

    for movement in basic_movement_matrix:
        output_batch = t.process(orange_image_batch, movement=movement)

        baseline = os.path.join(
            BASELINE_DIRECTORY,
            f"test_translate_movement_basic_matrix_{movement.x_distance}h_{movement.y_distance}v.png",
        )

        assert save_batch_and_compare(
            baseline, output_batch, temp_output_png, is_overwrite_existing=True
        )
