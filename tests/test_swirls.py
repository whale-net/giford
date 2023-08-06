import os
import pytest

from giford.frame_batch import FrameBatch
from giford.frame_wrapper import SingleImage
from giford.image_actions.swirl import BasicSwirl, VariableSwirl, VaryingVariableSwirl
from tests.util import (
    BASELINE_DIRECTORY,
    TEST_INPUT_ORANGE_IMAGE_FILEPATH,
    save_batch_and_compare,
)

def test_basic_swirl(temp_output_png: str, orange_image_batch: FrameBatch):
    baseline = os.path.join(BASELINE_DIRECTORY, "test_basic_swirl.png")

    bs = BasicSwirl()
    output_batch = bs.process(orange_image_batch)

    assert save_batch_and_compare(baseline, output_batch, temp_output_png)

@pytest.mark.parametrize("swirl_depth", [0, 5, 10])
def test_variable_swirl(temp_output_png: str, orange_image_batch: FrameBatch, swirl_depth: int):
    # test variable swirl
    if swirl_depth == 0:
        baseline = TEST_INPUT_ORANGE_IMAGE_FILEPATH
    else:
        baseline = os.path.join(
            BASELINE_DIRECTORY, f"test_variable_swirl_depth_{swirl_depth}.png"
        )

    vs = VariableSwirl()
    output_batch = vs.process(orange_image_batch, swirl_depth)

    assert save_batch_and_compare(baseline, output_batch, temp_output_png)

def test_varying_variable_swirl(temp_output_png: str, orange_image_batch: FrameBatch):
    # produce a bunch of swirls
    # this will take a while because the code is SLOWOWOW

    vvs = VaryingVariableSwirl()
    output_batch = vvs.process(orange_image_batch, 25)
    for i, frame in enumerate(output_batch.frames):
        simg = SingleImage.create_from_frame(frame)
        simg.save(temp_output_png)
        if i % 5 == 0:
            # TODO - don't overwrite same image
            simg.save(temp_output_png)
            baseline = os.path.join(
                BASELINE_DIRECTORY, f"test_varying_variable_swirl_depth_{i}.png"
            )

            assert save_batch_and_compare(baseline, output_batch[i], temp_output_png)