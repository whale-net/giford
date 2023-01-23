from datetime import datetime
from salt_shaker.image import Image
from salt_shaker.image_batch import ImageBatch
from salt_shaker.image_actions.swirl import (
    BasicSwirl,
    VariableSwirl,
    VaryingVariableSwirl,
)


def basic_rewrite(orange_image):
    orange_image.write_to_file("./sample_output/orange_simple_rewrite.png")


def basic_swirl(orange_image):
    basic_swirl = BasicSwirl()
    batch = ImageBatch()
    batch.add_image(orange_image)

    output_batch = basic_swirl.process(batch)

    # filetime = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_batch.images[0].write_to_file(f"./sample_output/orange_basic_swirl.png")


def variable_swirl(orange_image):
    variable_swirl = VariableSwirl()
    batch = ImageBatch()
    batch.add_image(orange_image)

    depth_5_batch = variable_swirl.process(batch, 5)
    depth_5_batch.images[0].write_to_file(
        f"./sample_output/orange_variable_swirl_depth_5.png"
    )
    depth_10_batch = variable_swirl.process(batch, 10)
    depth_10_batch.images[0].write_to_file(
        f"./sample_output/orange_variable_swirl_depth_10.png"
    )


def varying_variable_swirl(orange_image):
    # this will take a while
    varying_variable_swirl = VaryingVariableSwirl()
    batch = ImageBatch()
    batch.add_image(orange_image)

    output_batch = varying_variable_swirl.process(batch, 25)
    for i, img in enumerate(output_batch.images):
        if not (i % 5 == 0):
            continue
        img.write_to_file(
            f"./sample_output/orange_varying_variable_swirl_depth_{i}.png"
        )


if __name__ == "__main__":
    orange_image = Image.create_from_file("./sample_data/orange.png")

    basic_rewrite(orange_image)
    basic_swirl(orange_image)
    variable_swirl(orange_image)
    varying_variable_swirl(orange_image)
