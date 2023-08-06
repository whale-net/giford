import os
import hashlib

from giford.image import Image
from giford.frame_batch import FrameBatch
from giford.frame_wrapper import SingleImage, SingleImageFormat
from giford.image_actions.gif import Gifify

DEFAULT_TEST_SINGLE_IMAGE_FORMAT = SingleImageFormat.PNG

TEST_INPUT_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "input_data")
TEST_INPUT_ORANGE_IMAGE_FILEPATH = os.path.join(TEST_INPUT_DATA_FOLDER, "orange.png")
TEST_INPUT_ORANGE_IMAGE_SWIRL_FILEPATH = os.path.join(TEST_INPUT_DATA_FOLDER, "orange_swirl.gif")

BASELINE_DIRECTORY = os.path.join(os.path.dirname(__file__), "baseline_data")


def hash_file(filename):
    """ "This function returns the SHA-1 hash
    of the file passed into it

    ripped from https://www.programiz.com/python-programming/examples/hash-file
    """

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(filename, "rb") as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b"":
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


def create_gif(batch: FrameBatch, framerate: int = 15) -> Image:
    # todo create util test file
    g = Gifify()
    return g.process(batch, framerate=framerate)


def compare_file_hash(baseline_filepath: str, test_filepath: str) -> bool:
    assert baseline_filepath
    assert os.path.exists(baseline_filepath), "baseline_filepath does not exist"
    assert test_filepath
    assert os.path.exists(test_filepath), "test_filepath does not exist"

    baseline_hash = hash_file(baseline_filepath)
    test_hash = hash_file(test_filepath)

    return baseline_hash == test_hash, "file hashs do not match"

def save_batch_and_compare(baseline_filepath: str, batch: FrameBatch, test_filepath: str, 
                           is_force_multi_image: bool = False, 
                           target_format: SingleImageFormat = DEFAULT_TEST_SINGLE_IMAGE_FORMAT
                           ) -> bool:
    assert not batch.is_empty()
    
    if batch.size() > 1 or is_force_multi_image:
        raise NotImplementedError()
    else:
        wrapper = SingleImage.create_from_frame_batch(batch, target_format=target_format)

    wrapper.save(test_filepath)

    return compare_file_hash(baseline_filepath, test_filepath)