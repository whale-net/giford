import os

import pytest

from giford.frame_wrapper import MultiImage
from giford.frame_batch import FrameBatch
from tests.util import (
    compare_image_files,
    BASELINE_DIRECTORY,
    TEST_INPUT_ORANGE_IMAGE_SWIRL_FILEPATH,
)


def test_multi_image_load(orange_swirl_batch: FrameBatch):
    mimg = MultiImage()
    try:
        mimg.load(TEST_INPUT_ORANGE_IMAGE_SWIRL_FILEPATH)
    except NotImplementedError:
        pass
    except:
        assert False, "unexpected exception thrown"


def test_multi_image_save(temp_output_gif: str, orange_swirl_batch: FrameBatch):
    baseline = os.path.join(BASELINE_DIRECTORY, "test_multi_image_save.gif")

    mimg = MultiImage.create_from_frame_batch(orange_swirl_batch)
    mimg.save(temp_output_gif)

    assert compare_image_files(baseline, temp_output_gif)


def test_multi_image_create_from_batch(
    temp_output_gif: str, orange_swirl_batch: FrameBatch
):
    # yep this is the same test as above, hard to decouple these two right now
    # TODO decouple
    baseline = os.path.join(
        BASELINE_DIRECTORY, "test_multi_image_create_from_batch.gif"
    )

    mimg = MultiImage.create_from_frame_batch(orange_swirl_batch)
    mimg.save(temp_output_gif)

    assert compare_image_files(baseline, temp_output_gif)


@pytest.mark.parametrize("framerate", [5, 15, 60])
def test_multi_image_gif_framerate(
    temp_output_gif: str, orange_swirl_batch: FrameBatch, framerate: int
):
    # TODO - something other than 15 for once lol
    baseline = os.path.join(
        BASELINE_DIRECTORY, f"test_multi_image_gif_framerate_{framerate}.gif"
    )

    mimg = MultiImage.create_from_frame_batch(orange_swirl_batch)
    mimg.save(temp_output_gif)

    assert compare_image_files(baseline, temp_output_gif)
