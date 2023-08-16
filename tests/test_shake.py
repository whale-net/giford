import os

import pytest

from giford.frame_batch import FrameBatch
from giford.image_actions.shake import Shake
from giford.frame_wrapper import MultiImage
from tests.util import BASELINE_DIRECTORY, save_batch_and_compare


def test_shake(
    temp_output_gif, orange_image_batch: FrameBatch
):
    baseline = os.path.join(
        BASELINE_DIRECTORY, f"test_shake.gif"
    )

    s = Shake()
    output_batch = s.process(orange_image_batch, 30, seed=1234)

    assert save_batch_and_compare(baseline, output_batch, temp_output_gif)
