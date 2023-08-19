from giford.image import AbstractImage, SingleImage
from giford.frame_batch import FrameBatch
from tests.util import compare_image_files, TEST_INPUT_ORANGE_IMAGE_FILEPATH


def test_single_image_load():
    img = SingleImage()
    img.load(TEST_INPUT_ORANGE_IMAGE_FILEPATH)

    assert len(img.raw_data_frames) == 1


def test_single_image_save(temp_output_png, single_orange_image):
    single_orange_image.save(temp_output_png)
    assert compare_image_files(TEST_INPUT_ORANGE_IMAGE_FILEPATH, temp_output_png)


def test_single_image_create_from_batch(temp_output_png, orange_image_batch):
    img = SingleImage.create_from_frame_batch(orange_image_batch)
    # TODO equality instead of write???? maybe one day
    img.save(temp_output_png)
    assert compare_image_files(TEST_INPUT_ORANGE_IMAGE_FILEPATH, temp_output_png)
