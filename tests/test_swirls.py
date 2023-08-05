import os
import pytest

from giford.image import Image
from giford.frame_batch import FrameBatch
from giford.image_actions.swirl import BasicSwirl, VariableSwirl, VaryingVariableSwirl
from tests.util import BASELINE_DIRECTORY, TEST_INPUT_ORANGE_IMAGE_FILEPATH, compare_file_hash 

def test_basic_swirl(temp_output_png: str, orange_image: Image):
    baseline = os.path.join(BASELINE_DIRECTORY, 'test_basic_swirl.png')

    bs = BasicSwirl()
    batch = FrameBatch()
    batch.add_image(orange_image)

    output_batch = bs.process(batch)
    Image.create_from_frame_batch(output_batch).write_to_file(temp_output_png)

    assert compare_file_hash(baseline, temp_output_png)


@pytest.mark.parametrize(
        'swirl_depth',
        [0, 5, 10]
)
def test_variable_swirl(temp_output_png: str, orange_image: Image, swirl_depth: int):
    # test variable swirl
    if swirl_depth == 0:
        baseline = TEST_INPUT_ORANGE_IMAGE_FILEPATH
    else:
        baseline = os.path.join(BASELINE_DIRECTORY, f'test_variable_swirl_depth_{swirl_depth}.png')

    vs = VariableSwirl()
    batch = FrameBatch()
    batch.add_image(orange_image)

    batch = vs.process(batch, swirl_depth)
    Image.create_from_frame_batch(batch).write_to_file(temp_output_png)
    assert compare_file_hash(baseline, temp_output_png)

def test_varying_variable_swirl(temp_output_png: str, orange_image: Image):
    # produce a bunch of swirls
    # this will take a while because the code is SLOWOWOW
    
    vvs = VaryingVariableSwirl()
    batch = FrameBatch()
    batch.add_image(orange_image)

    output_batch = vvs.process(batch, 25)
    for i, frame in enumerate(output_batch.frames):
        img = Image.create_from_raw_data_frame(frame)
        if i % 5 == 0:
            # TODO - don't overwrite same image
            img.write_to_file(temp_output_png)
            baseline = os.path.join(BASELINE_DIRECTORY, f'test_varying_variable_swirl_depth_{i}.png')
            assert compare_file_hash(baseline, temp_output_png)
