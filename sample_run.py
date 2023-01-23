import os
from salt_shaker.image import Image
from salt_shaker.image_batch import ImageBatch
from salt_shaker.image_actions.swirl import (
    BasicSwirl,
    VariableSwirl,
    VaryingVariableSwirl,
)
from salt_shaker.image_actions.gif import Gifify

INPUT_DIR = "./sample_data/"
GIF_DATA_INPUT_DIR = os.path.join(INPUT_DIR, "gif_data")
OUTPUT_DIR = "./sample_output/"

VARYING_DEPTH = 25


def basic_rewrite(input_image):
    input_image.write_to_file(os.path.join(OUTPUT_DIR, "orange_simple_rewrite.png"))


def basic_swirl(input_image):
    bs = BasicSwirl()
    batch = ImageBatch()
    batch.add_image(input_image)

    output_batch = bs.process(batch)
    output_batch.images[0].write_to_file(
        os.path.join(OUTPUT_DIR, "orange_basic_swirl.png")
    )


def variable_swirl(input_image):
    vs = VariableSwirl()
    batch = ImageBatch()
    batch.add_image(input_image)

    depth_5_batch = vs.process(batch, 5)
    depth_5_batch.images[0].write_to_file(
        os.path.join(OUTPUT_DIR, "orange_variable_swirl_depth_5.png")
    )
    depth_10_batch = vs.process(batch, 10)
    depth_10_batch.images[0].write_to_file(
        os.path.join(OUTPUT_DIR, "orange_variable_swirl_depth_10.png")
    )


def varying_variable_swirl(input_image):
    # this will take a while
    vvs = VaryingVariableSwirl()
    batch = ImageBatch()
    batch.add_image(input_image)

    output_batch = vvs.process(batch, VARYING_DEPTH)
    for i, img in enumerate(output_batch.images):
        if i % 5 == 0:
            img.write_to_file(
                os.path.join(OUTPUT_DIR, f"orange_varying_variable_swirl_depth_{i}.png")
            )

        # write data to input dir for gif demo
        try:
            img.write_to_file(
                os.path.join(GIF_DATA_INPUT_DIR, f"swirl_depth_{i}.png"),
                overwrite=False,
            )
        except FileExistsError:
            pass


def gif():
    g = Gifify()
    batch = ImageBatch()
    for i in range(VARYING_DEPTH):
        batch.add_image(
            Image.create_from_file(
                os.path.join(GIF_DATA_INPUT_DIR, f"swirl_depth_{i}.png")
            )
        )
    output_gif = g.process(batch)

    with open(os.path.join(OUTPUT_DIR, "orange_swirl.gif"), "wb") as f:
        f.write(output_gif)


if __name__ == "__main__":
    orange = Image.create_from_file(os.path.join(INPUT_DIR, "orange.png"))

    basic_rewrite(orange)
    basic_swirl(orange)
    variable_swirl(orange)
    # varying_variable_swirl(orange)
    gif()
