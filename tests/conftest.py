import os
import tempfile

import pytest

from giford.image import Image
from giford.frame_batch import FrameBatch

TEST_INPUT_DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'input_data')
ORANGE_IMAGE_FILEPATH = os.path.join(TEST_INPUT_DATA_FOLDER, 'orange.png')

@pytest.fixture
def temp_output_png(tmp_path):
    return os.path.join(tmp_path, 'output.png')

@pytest.fixture
def orange_image() -> Image:
    img = Image.create_from_file(ORANGE_IMAGE_FILEPATH)
    return img

@pytest.fixture
def orange_swirl_batch() -> FrameBatch:
    batch = FrameBatch()
    for idx in range(25):
        img_path = os.path.join(TEST_INPUT_DATA_FOLDER, 'gif_data', f'swirl_depth_{idx}.png')
        img = Image.create_from_file(img_path)
        batch.add_image(img)
    return batch

