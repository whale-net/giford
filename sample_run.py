import os
from salt_shaker.image import Image
from salt_shaker.frame_batch import FrameBatch
from salt_shaker.image_actions.swirl import (
    BasicSwirl,
    VariableSwirl,
    VaryingVariableSwirl,
)
from salt_shaker.image_actions.gif import Gifify
from salt_shaker.image_actions.translate import Translate

INPUT_DIR = "./sample_data/"
GIF_DATA_INPUT_DIR = os.path.join(INPUT_DIR, "gif_data")
OUTPUT_DIR = "./sample_output/"

VARYING_DEPTH = 25


def basic_rewrite(input_image):
    input_image.write_to_file(os.path.join(OUTPUT_DIR, "orange_simple_rewrite.png"))


def basic_swirl(input_image):
    bs = BasicSwirl()
    batch = FrameBatch()
    batch.add_image(input_image)

    output_batch = bs.process(batch)
    Image.create_from_raw_data_frame(output_batch.frames[0]).write_to_file(
        os.path.join(OUTPUT_DIR, "orange_basic_swirl.png")
    )


def variable_swirl(input_image):
    vs = VariableSwirl()
    batch = FrameBatch()
    batch.add_image(input_image)

    depth_5_batch = vs.process(batch, 5)
    Image.create_from_raw_data_frame(depth_5_batch.frames[0]).write_to_file(
        os.path.join(OUTPUT_DIR, "orange_variable_swirl_depth_5.png")
    )
    depth_10_batch = vs.process(batch, 10)
    Image.create_from_raw_data_frame(depth_10_batch.frames[0]).write_to_file(
        os.path.join(OUTPUT_DIR, "orange_variable_swirl_depth_10.png")
    )


def varying_variable_swirl(input_image):
    # this will take a while
    vvs = VaryingVariableSwirl()
    batch = FrameBatch()
    batch.add_image(input_image)

    output_batch = vvs.process(batch, VARYING_DEPTH)
    for i, frame in enumerate(output_batch.frames):
        img = Image.create_from_raw_data_frame(frame)
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
    batch = FrameBatch()
    for i in range(VARYING_DEPTH):
        batch.add_image(
            Image.create_from_file(
                os.path.join(GIF_DATA_INPUT_DIR, f"swirl_depth_{i}.png")
            )
        )
    output_gif = g.process(batch)

    # with open(os.path.join(OUTPUT_DIR, "orange_swirl.gif"), "wb") as f:
    #     f.write(output_gif)
    output_gif.write_to_file(os.path.join(OUTPUT_DIR, "orange_swirl.gif"))

def translate_basic(input_image):
    t = Translate()
    batch = FrameBatch()
    batch.add_image(input_image)
    output_batch = \
        t.process(batch, horizontal_shift_px=100)\
        .add_batch(t.process(batch, horizontal_shift_px=-100))\
        .add_batch(t.process(batch, vertical_shift_px=100))\
        .add_batch(t.process(batch, vertical_shift_px=-100))

    img_hp = Image.create_from_raw_data_frame(output_batch.frames[0])
    img_hp.write_to_file(os.path.join(OUTPUT_DIR, 'orange_translate_h+100.png'))

    img_hn = Image.create_from_raw_data_frame(output_batch.frames[1])
    img_hn.write_to_file(os.path.join(OUTPUT_DIR, 'orange_translate_h-100.png'))

    img_vp = Image.create_from_raw_data_frame(output_batch.frames[2])
    img_vp.write_to_file(os.path.join(OUTPUT_DIR, 'orange_translate_v+100.png'))

    img_vn = Image.create_from_raw_data_frame(output_batch.frames[3])
    img_vn.write_to_file(os.path.join(OUTPUT_DIR, 'orange_translate_v-100.png'))

def translate_complex(input_image):
    t = Translate()
    batch = FrameBatch()
    batch.add_image(input_image)
    output_batch = \
        t.process(batch, horizontal_shift_px=100, vertical_shift_px=100)\
        .add_batch(t.process(batch, horizontal_shift_px=-100, vertical_shift_px=100))\
        .add_batch(t.process(batch, horizontal_shift_px=100, vertical_shift_px=-100))\
        .add_batch(t.process(batch, horizontal_shift_px=-100, vertical_shift_px=-100))

    img_hp_vp = Image.create_from_raw_data_frame(output_batch.frames[0])
    img_hp_vp.write_to_file(os.path.join(OUTPUT_DIR, 'orange_translate_h+100_v+100.png'))

    img_hn_vp = Image.create_from_raw_data_frame(output_batch.frames[1])
    img_hn_vp.write_to_file(os.path.join(OUTPUT_DIR, 'orange_translate_h-100_v+100.png'))

    img_hp_vn = Image.create_from_raw_data_frame(output_batch.frames[2])
    img_hp_vn.write_to_file(os.path.join(OUTPUT_DIR, 'orange_translate_h+100_v-100.png'))

    img_hn_vn = Image.create_from_raw_data_frame(output_batch.frames[3])
    img_hn_vn.write_to_file(os.path.join(OUTPUT_DIR, 'orange_translate_h-100_v-100.png'))



if __name__ == "__main__":
    orange = Image.create_from_file(os.path.join(INPUT_DIR, "orange.png"))

    basic_rewrite(orange)
    basic_swirl(orange)
    variable_swirl(orange)
    varying_variable_swirl(orange)
    gif()
    translate_basic(orange)
    translate_complex(orange)
