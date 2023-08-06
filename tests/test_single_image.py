from giford.frame_wrapper.single_image import SingleImage

from tests.util import compare_file_hash, TEST_INPUT_ORANGE_IMAGE_FILEPATH

def test_single_image_load():
    img = SingleImage()
    img.load(TEST_INPUT_ORANGE_IMAGE_FILEPATH)

    assert len(img.raw_data_frames) == 1

def test_single_image_save(temp_output_png):
    # todo use fixture
    img = SingleImage()
    img.load(TEST_INPUT_ORANGE_IMAGE_FILEPATH)
    img.save(temp_output_png)
    assert compare_file_hash(TEST_INPUT_ORANGE_IMAGE_FILEPATH, temp_output_png)