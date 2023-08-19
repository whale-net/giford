import os
import pytest

from giford.frame import FrameBatch
from giford.image import SingleImage
from giford.action import BasicSwirl, VariableSwirl, VaryingVariableSwirl
from tests.util import (
    BASELINE_DIRECTORY,
    TEST_INPUT_ORANGE_IMAGE_FILEPATH,
    save_batch_and_compare,
    compare_image_files,
)


def test_basic_swirl(temp_output_png: str, orange_image_batch: FrameBatch):
    baseline = os.path.join(BASELINE_DIRECTORY, "test_basic_swirl.png")

    bs = BasicSwirl()
    output_batch = bs.process(orange_image_batch)

    assert save_batch_and_compare(baseline, output_batch, temp_output_png)


@pytest.mark.parametrize("swirl_depth", [0, 5, 10])
def test_variable_swirl(
    temp_output_png: str, orange_image_batch: FrameBatch, swirl_depth: int
):
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


def test_varying_variable_swirl_increasing_depth(
    temp_out_png_generator, orange_image_batch: FrameBatch
):
    # produce a bunch of swirls
    # this will take a while

    vvs = VaryingVariableSwirl()
    # can support 25, but limiting to 11 (idx 10) for speed
    # output_batch = vvs.process(orange_image_batch, 25)
    output_batch = vvs.process(orange_image_batch, 11, is_increasing_swirl_depth=True)
    comparisons: list[tuple[str, str]] = []
    for i, frame in enumerate(output_batch.frames):
        if i % 5 == 0:
            baseline = os.path.join(
                BASELINE_DIRECTORY,
                f"test_varying_variable_swirl_increasing_depth_{i}.png",
            )
            temp_output_png = next(temp_out_png_generator)
            simg = SingleImage.create_from_frame(frame)
            simg.save(temp_output_png)
            comparisons.append((baseline, temp_output_png))

    for baseline, test in comparisons:
        assert compare_image_files(baseline, test)


def test_varying_variable_swirl_default_depth(
    temp_out_png_generator, orange_image_batch: FrameBatch
):
    vvs = VaryingVariableSwirl()

    output_batch = vvs.process(orange_image_batch, 10)
    comparisons: list[tuple[str, str]] = []
    for i, frame in enumerate(output_batch.frames):
        baseline = os.path.join(
            BASELINE_DIRECTORY, f"test_varying_variable_swirl_default_depth_{i}.png"
        )
        temp_output_png = next(temp_out_png_generator)
        simg = SingleImage.create_from_frame(frame)
        simg.save(temp_output_png)
        comparisons.append((baseline, temp_output_png))

    for baseline, test in comparisons:
        assert compare_image_files(baseline, test)


# TODO varying increment > 1
