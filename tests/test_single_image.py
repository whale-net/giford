from tempfile import TemporaryFile

from giford.image import SingleImage
from giford.frame import FrameBatch
from giford.util import buffered_stream_copy
from tests.util import compare_image_files, TEST_INPUT_ORANGE_IMAGE_FILEPATH


def test_single_image_load_path():
    img = SingleImage()
    img.load(TEST_INPUT_ORANGE_IMAGE_FILEPATH)

    assert len(img.raw_data_frames) == 1


def test_single_image_load_fp(temp_output_png):
    img = SingleImage()
    with open(TEST_INPUT_ORANGE_IMAGE_FILEPATH, "r+b") as fp:
        img.load(fp)

    assert len(img.raw_data_frames) == 1
    # although it's not quite an isolated test
    # want to make sure we're still reading/writing the correct stuff
    img.save(temp_output_png)
    assert compare_image_files(TEST_INPUT_ORANGE_IMAGE_FILEPATH, temp_output_png)


def test_single_image_save_path(temp_output_png, single_orange_image: SingleImage):
    single_orange_image.save(temp_output_png)
    assert compare_image_files(TEST_INPUT_ORANGE_IMAGE_FILEPATH, temp_output_png)


def test_single_image_save_fp(temp_output_png, single_orange_image: SingleImage):
    with TemporaryFile() as fp:
        single_orange_image.save(fp)

        fp.seek(0)
        with open(temp_output_png, "wb") as final_out:
            buffered_stream_copy(fp, final_out)

    assert compare_image_files(TEST_INPUT_ORANGE_IMAGE_FILEPATH, temp_output_png)


def test_single_image_create_from_batch(
    temp_output_png, orange_image_batch: FrameBatch
):
    img = SingleImage.create_from_frame_batch(orange_image_batch)
    # TODO equality instead of write???? maybe one day
    img.save(temp_output_png)
    assert compare_image_files(TEST_INPUT_ORANGE_IMAGE_FILEPATH, temp_output_png)
