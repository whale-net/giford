import os

import pytest

from giford.image import Image
from giford.frame_batch import FrameBatch
from giford.image_actions.gif import Gifify
from tests.util import BASELINE_DIRECTORY, compare_file_hash


@pytest.mark.parametrize("framerate", [5, 15, 60])
def test_create_gif(
    temp_output_gif: str, orange_swirl_batch: FrameBatch, framerate: int
) -> Image:
    baseline = os.path.join(
        BASELINE_DIRECTORY, f"test_create_gif_framerate_{framerate}.gif"
    )

    g = Gifify()
    g.process(orange_swirl_batch, framerate=framerate).write_to_file(temp_output_gif)

    assert compare_file_hash(baseline, temp_output_gif)
