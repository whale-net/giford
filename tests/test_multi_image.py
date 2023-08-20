import os
from tempfile import TemporaryFile

import pytest

from giford.image import MultiImage, SingleImage
from giford.frame import FrameBatch
from tests.util import (
    compare_image_files,
    BASELINE_DIRECTORY,
    TEST_INPUT_ORANGE_IMAGE_SWIRL_FILEPATH,
    TEST_INPUT_DATA_FOLDER,
)


def test_multi_image_load_bad():
    with pytest.raises(ValueError):
        mimg = MultiImage().load(in_file=None)

def test_multi_image_load_path(temp_output_gif, temp_output_png):
    mimg = MultiImage()
    # with pytest.raises(NotImplementedError):
    #     mimg.load(TEST_INPUT_ORANGE_IMAGE_SWIRL_FILEPATH)
    base_img_path = os.path.join(TEST_INPUT_DATA_FOLDER, "orange_swirl.gif")
    mimg.load(base_img_path)

    # simg = SingleImage.create_from_frame(mimg.raw_data_frames[0])
    # simg.save(temp_output_png)
    mimg.save(temp_output_gif)
    # print(temp_output_png)
    # print(temp_output_gif)
    assert compare_image_files(base_img_path, temp_output_gif)


def test_multi_image_save_path(temp_output_gif: str, orange_swirl_batch: FrameBatch):
    baseline = os.path.join(BASELINE_DIRECTORY, "test_multi_image_save.gif")

    mimg = MultiImage.create_from_frame_batch(orange_swirl_batch)
    mimg.save(temp_output_gif)

    assert compare_image_files(baseline, temp_output_gif)


def test_multi_image_save_fp(temp_output_gif: str, orange_swirl_batch: FrameBatch):
    mimg = MultiImage.create_from_frame_batch(orange_swirl_batch)

    with TemporaryFile() as fp:
        mimg.save(fp)

        fp.seek(0)
        BUFFER_SIZE = 4096
        with open(temp_output_gif, "wb") as final_out:
            buf: bytes = fp.read(BUFFER_SIZE)
            while len(buf) > 0:
                final_out.write(buf)
                buf = fp.read(BUFFER_SIZE)

    baseline = os.path.join(BASELINE_DIRECTORY, "test_multi_image_save.gif")
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
