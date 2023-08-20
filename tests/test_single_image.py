from tempfile import TemporaryFile

from giford.image import SingleImage
from giford.frame import FrameBatch
from tests.util import compare_image_files, TEST_INPUT_ORANGE_IMAGE_FILEPATH


def test_single_image_load():
    img = SingleImage()
    img.load(TEST_INPUT_ORANGE_IMAGE_FILEPATH)

    assert len(img.raw_data_frames) == 1


def test_single_image_save_path(temp_output_png, single_orange_image: SingleImage):
    single_orange_image.save(temp_output_png)
    assert compare_image_files(TEST_INPUT_ORANGE_IMAGE_FILEPATH, temp_output_png)

def test_single_image_save_fp(temp_output_png, single_orange_image: SingleImage):
    with TemporaryFile() as fp:
        single_orange_image.save(fp)

        fp.seek(0)
        BUFFER_SIZE = 4096
        with open(temp_output_png, 'wb') as final_out:
            buf: bytes = fp.read(BUFFER_SIZE)
            while len(buf) > 0:
                final_out.write(buf)
                buf = fp.read(BUFFER_SIZE)

    assert compare_image_files(TEST_INPUT_ORANGE_IMAGE_FILEPATH, temp_output_png)


def test_single_image_create_from_batch(
    temp_output_png, orange_image_batch: FrameBatch
):
    img = SingleImage.create_from_frame_batch(orange_image_batch)
    # TODO equality instead of write???? maybe one day
    img.save(temp_output_png)
    assert compare_image_files(TEST_INPUT_ORANGE_IMAGE_FILEPATH, temp_output_png)
