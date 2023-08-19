import os

import pytest

from giford.image import SingleImage
from giford.frame import FrameBatch
from giford.util import Point, Movement, VirtualPath

from tests.util import (
    TEST_INPUT_DATA_FOLDER,
    TEST_INPUT_ORANGE_IMAGE_FILEPATH,
    MAX_IMAGES_PER_TEST,
)


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
def temp_out_png_generator(tmp_path):
    return (
        create_test_image(tmp_path, f"output{i}.png")
        for i in range(MAX_IMAGES_PER_TEST)
    )


@pytest.fixture
def temp_output_gif(tmp_path):
    # create path of temporary gif for tests to use
    return create_test_image(tmp_path, "output.gif")


@pytest.fixture
def single_orange_image() -> SingleImage:
    img = SingleImage()
    img.load(TEST_INPUT_ORANGE_IMAGE_FILEPATH)
    return img


@pytest.fixture()
def orange_image_batch(single_orange_image) -> FrameBatch:
    return FrameBatch.create_from_image(single_orange_image)


@pytest.fixture
def orange_swirl_batch() -> FrameBatch:
    batch = FrameBatch()
    for idx in range(25):
        img_path = os.path.join(
            TEST_INPUT_DATA_FOLDER, "gif_data", f"swirl_depth_{idx}.png"
        )
        img = SingleImage()
        img.load(img_path)
        batch.add_frame(img.raw_data_frame)
    return batch


@pytest.fixture
def basic_movement_matrix() -> list[Movement]:
    # cover all 9 quadrants
    neg_x = -0.25
    pos_x = 0.25
    neg_y = -0.25
    pos_y = 0.25
    vp = VirtualPath()
    vp.add_point(Point(neg_x, neg_y))
    vp.add_point(Point(0, neg_y))
    vp.add_point(Point(pos_x, neg_y))
    vp.add_point(Point(neg_x, 0))
    vp.add_point(Point(0, 0))
    vp.add_point(Point(pos_x, 0))
    vp.add_point(Point(neg_x, pos_y))
    vp.add_point(Point(0, pos_y))
    vp.add_point(Point(pos_x, pos_y))

    return vp.calculate_movements(is_from_true_origin=True)
