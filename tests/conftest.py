import os
import tempfile

import pytest

from giford.frame_wrapper.single_image import SingleImage
from giford.image import Image
from giford.frame_batch import FrameBatch
from tests.util import TEST_INPUT_DATA_FOLDER, TEST_INPUT_ORANGE_IMAGE_FILEPATH

def create_test_image(directory, filename, is_delete_existing: bool = True):
    tmp_img_filepath = os.path.join(directory, filename)
    # sometimes pytest tmp_path appears to be re-used
    # so try and delete file if it exists to avoid accidental cross-pollination
    if is_delete_existing and os.path.exists(tmp_img_filepath):
        os.remove(tmp_img_filepath)
    return tmp_img_filepath


@pytest.fixture
def temp_output_png(tmp_path):
    # create path of temporary png for tests to use
    return create_test_image(tmp_path, "output.png")


@pytest.fixture
def temp_output_gif(tmp_path):
    # create path of temporary gif for tests to use
    return create_test_image(tmp_path, "output.gif")


@pytest.fixture
def single_orange_image() -> Image:
    img = SingleImage()
    img.load(TEST_INPUT_ORANGE_IMAGE_FILEPATH)
    return img

@pytest.fixture()
def orange_image_batch(single_orange_image) -> FrameBatch:
    return FrameBatch.create_from_single_image(single_orange_image)

@pytest.fixture
def orange_swirl_batch() -> FrameBatch:
    batch = FrameBatch()
    for idx in range(25):
        img_path = os.path.join(
            TEST_INPUT_DATA_FOLDER, "gif_data", f"swirl_depth_{idx}.png"
        )
        img = Image.create_from_file(img_path)
        batch.add_image(img)
    return batch
