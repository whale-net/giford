import os
import hashlib

from PIL import Image as PillowImage

from giford.frame_batch import FrameBatch
from giford.frame_wrapper import SingleImage, SingleImageFormat

DEFAULT_TEST_SINGLE_IMAGE_FORMAT = SingleImageFormat.PNG

TEST_INPUT_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "input_data")
TEST_INPUT_ORANGE_IMAGE_FILEPATH = os.path.join(TEST_INPUT_DATA_FOLDER, "orange.png")
TEST_INPUT_ORANGE_IMAGE_SWIRL_FILEPATH = os.path.join(
    TEST_INPUT_DATA_FOLDER, "orange_swirl.gif"
)

BASELINE_DIRECTORY = os.path.join(os.path.dirname(__file__), "baseline_data")


def compare_image_files(baseline_filepath: str, test_filepath: str) -> bool:
    assert baseline_filepath
    assert os.path.exists(baseline_filepath), "baseline_filepath does not exist"
    assert test_filepath
    assert os.path.exists(test_filepath), "test_filepath does not exist"

    # Using PIL/Pillow to compare
    # Ran into issue using file hash since pillow will somtimes compress images when saving
    # which makes the hashes different
    # Hopefully PIL/Pillow is tested enough that this is a reasonable operation
    # NOTE: deleting info dict removes icc_profile, unsure if that matters
    baseline_pimg = PillowImage.open(baseline_filepath)
    baseline_pimg.info = {}
    test_pimg = PillowImage.open(test_filepath)
    test_pimg.info = {}

    return baseline_pimg == test_pimg


def save_batch_and_compare(
    baseline_filepath: str,
    batch: FrameBatch,
    test_filepath: str,
    is_force_multi_image: bool = False,
    target_format: SingleImageFormat = DEFAULT_TEST_SINGLE_IMAGE_FORMAT,
) -> bool:
    assert not batch.is_empty()

    if batch.size() > 1 or is_force_multi_image:
        raise NotImplementedError()
    else:
        wrapper = SingleImage.create_from_frame_batch(
            batch, target_format=target_format
        )

    if os.path.exists(test_filepath):
        raise FileExistsError("cannot overwrite test file")

    wrapper.save(test_filepath, overwrite_existing=False)

    return compare_image_files(baseline_filepath, test_filepath)
