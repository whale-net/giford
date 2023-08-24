import os

import numpy as np
from PIL import Image as PillowImage

from giford.frame.frame_batch import FrameBatch
from giford.image import (
    SingleImage,
    SingleImageFormat,
    MultiImage,
    MultiImageFormat,
)

DEFAULT_TEST_SINGLE_IMAGE_FORMAT = SingleImageFormat.PNG

TEST_INPUT_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "input_data")
TEST_INPUT_ORANGE_IMAGE_FILEPATH = os.path.join(TEST_INPUT_DATA_FOLDER, "orange.png")
TEST_INPUT_ORANGE_IMAGE_SWIRL_FILEPATH = os.path.join(
    TEST_INPUT_DATA_FOLDER, "orange_swirl.gif"
)

BASELINE_DIRECTORY = os.path.join(os.path.dirname(__file__), "baseline_data")

MAX_IMAGES_PER_TEST = 30


def compare_image_files(baseline_filepath: str, test_filepath: str) -> bool:
    assert baseline_filepath
    assert os.path.exists(baseline_filepath), "baseline_filepath does not exist"
    assert test_filepath
    assert os.path.exists(test_filepath), "test_filepath does not exist"

    # Using PIL/Pillow to open images since that is indepdent of this project
    # Calculate MSE of each file
    # TODO - what is max dfference? don't really know much about this tbh
    # TODO explore SSIM https://pypi.org/project/SSIM-PIL/
    baseline_pimg = PillowImage.open(baseline_filepath)
    test_pimg = PillowImage.open(test_filepath)

    baseline_frame_count = baseline_pimg.n_frames
    test_frame_count = test_pimg.n_frames
    assert (
        baseline_frame_count == test_frame_count
    ), f"different frame count {baseline_frame_count} <> {test_frame_count}"

    for frame_idx in range(0, baseline_pimg.n_frames):
        baseline_pimg.seek(frame_idx)
        test_pimg.seek(frame_idx)

        # Mean Square Error
        # basically what is the max difference between the two pictures
        # not a perfect comparison, but should handle PIL discrepancies
        mse = np.square(
            np.subtract(np.asarray(baseline_pimg), np.asarray(test_pimg))
        ).mean()

        # 1.00 was experimentally found to be ok
        assert mse < 1.00, f"frame_idx={frame_idx} is different"

    # returning true since I initially set this function up stupidly
    return True


def save_batch_and_compare(
    baseline_filepath: str,
    batch: FrameBatch,
    test_filepath: str,
    is_force_multi_image: bool = False,
    target_format: SingleImageFormat = DEFAULT_TEST_SINGLE_IMAGE_FORMAT,
    is_overwrite_existing: bool = False,
) -> bool:
    assert not batch.is_empty()

    if not is_overwrite_existing and os.path.exists(test_filepath):
        raise FileExistsError("cannot overwrite test file")

    if batch.size() > 1 or is_force_multi_image:
        wrapper = MultiImage.create_from_frame_batch(
            batch, target_format=MultiImageFormat.GIF
        )
    else:
        wrapper = SingleImage.create_from_frame_batch(
            batch, target_format=target_format
        )

    wrapper.save(test_filepath, overwrite_existing=is_overwrite_existing)

    return compare_image_files(baseline_filepath, test_filepath)
