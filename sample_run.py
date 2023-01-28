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
from salt_shaker.image_actions.reshape import Reshape, ReshapeMethod
from salt_shaker.image_actions.scroll import Scroll

INPUT_DIR = "./sample_data/"
GIF_DATA_INPUT_DIR = os.path.join(INPUT_DIR, "gif_data")
OUTPUT_DIR = "./sample_output/"

VARYING_DEPTH = 25


def create_gif(batch: FrameBatch, framerate: int = 15) -> Image:
    # todo create util test file
    g = Gifify()
    return g.process(batch, framerate=framerate)


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
    batch = FrameBatch()
    for i in range(VARYING_DEPTH):
        batch.add_image(
            Image.create_from_file(
                os.path.join(GIF_DATA_INPUT_DIR, f"swirl_depth_{i}.png")
            )
        )
    output_gif = create_gif(batch)

    # with open(os.path.join(OUTPUT_DIR, "orange_swirl.gif"), "wb") as f:
    #     f.write(output_gif)
    output_gif.write_to_file(os.path.join(OUTPUT_DIR, "orange_swirl.gif"))


def translate_basic(input_image):
    t = Translate()
    batch = FrameBatch()
    batch.add_image(input_image)
    output_batch = (
        t.process(batch, horizontal_shift_px=100)
        .add_batch(t.process(batch, horizontal_shift_px=-100))
        .add_batch(t.process(batch, vertical_shift_px=100))
        .add_batch(t.process(batch, vertical_shift_px=-100))
    )

    img_hp = Image.create_from_raw_data_frame(output_batch.frames[0])
    img_hp.write_to_file(os.path.join(OUTPUT_DIR, "orange_translate_h+100.png"))

    img_hn = Image.create_from_raw_data_frame(output_batch.frames[1])
    img_hn.write_to_file(os.path.join(OUTPUT_DIR, "orange_translate_h-100.png"))

    img_vp = Image.create_from_raw_data_frame(output_batch.frames[2])
    img_vp.write_to_file(os.path.join(OUTPUT_DIR, "orange_translate_v+100.png"))

    img_vn = Image.create_from_raw_data_frame(output_batch.frames[3])
    img_vn.write_to_file(os.path.join(OUTPUT_DIR, "orange_translate_v-100.png"))


def translate_complex(input_image):
    t = Translate()
    batch = FrameBatch()
    batch.add_image(input_image)
    output_batch = (
        t.process(batch, horizontal_shift_px=100, vertical_shift_px=100)
        .add_batch(t.process(batch, horizontal_shift_px=-100, vertical_shift_px=100))
        .add_batch(t.process(batch, horizontal_shift_px=100, vertical_shift_px=-100))
        .add_batch(t.process(batch, horizontal_shift_px=-100, vertical_shift_px=-100))
    )

    img_hp_vp = Image.create_from_raw_data_frame(output_batch.frames[0])
    img_hp_vp.write_to_file(
        os.path.join(OUTPUT_DIR, "orange_translate_h+100_v+100.png")
    )

    img_hn_vp = Image.create_from_raw_data_frame(output_batch.frames[1])
    img_hn_vp.write_to_file(
        os.path.join(OUTPUT_DIR, "orange_translate_h-100_v+100.png")
    )

    img_hp_vn = Image.create_from_raw_data_frame(output_batch.frames[2])
    img_hp_vn.write_to_file(
        os.path.join(OUTPUT_DIR, "orange_translate_h+100_v-100.png")
    )

    img_hn_vn = Image.create_from_raw_data_frame(output_batch.frames[3])
    img_hn_vn.write_to_file(
        os.path.join(OUTPUT_DIR, "orange_translate_h-100_v-100.png")
    )


def reshape(test_image):
    # reshape test
    batch = FrameBatch()
    batch.add_image(test_image)

    r = Reshape()

    def local_reshape(reshape_method: ReshapeMethod):
        out_batch = r.process(batch, reshape_method, 0.25)
        img = Image.create_from_raw_data_frame(out_batch.frames[0])
        img.write_to_file(os.path.join(OUTPUT_DIR, f"reshape_{reshape_method}.png"))

    local_reshape(ReshapeMethod.RESCALE)
    local_reshape(ReshapeMethod.RESIZE)
    # local_reshape(ReshapeMethod.DOWNSCALE)


def scroll(test_image: Image):
    batch = FrameBatch()
    batch.add_image(test_image)

    # rescale so the images aren't so big
    r = Reshape()
    batch = r.process(batch, reshape_method=ReshapeMethod.RESIZE, scale_factor=0.25)

    b = Scroll()
    out_batch = b.process(
        batch,
        num_frames=30,
        is_wrap_image=True,
        scroll_count=2,
        is_horizontal_scroll=True,
        is_horizontal_direction_negative=True,
        is_vertical_scroll=True,
        is_vertical_direction_negative=False,
        vertical_scroll_multiplier=0.25,
    )

    gif_no_wrap = create_gif(
        b.process(
            batch,
            num_frames=30,
            is_wrap_image=False,
            is_horizontal_scroll=True,
            is_vertical_scroll=True,
        )
    )
    gif_no_wrap.write_to_file(os.path.join(OUTPUT_DIR, "scroll_gif_no_wrap.gif"))

    gif_no_wrap_reverse = create_gif(
        b.process(
            batch,
            num_frames=30,
            is_wrap_image=False,
            is_horizontal_scroll=True,
            is_horizontal_direction_negative=True,
            is_vertical_scroll=True,
            is_vertical_direction_negative=True,
        )
    )
    gif_no_wrap_reverse.write_to_file(
        os.path.join(OUTPUT_DIR, "scroll_gif_no_wrap_reverse.gif")
    )

    gif_wrap = create_gif(
        b.process(
            batch,
            num_frames=30,
            is_wrap_image=True,
            scroll_count=2,
            is_horizontal_scroll=True,
            is_horizontal_direction_negative=True,
            is_vertical_scroll=True,
            is_vertical_direction_negative=False,
            vertical_scroll_multiplier=0.25,
        )
    )
    gif_wrap.write_to_file(os.path.join(OUTPUT_DIR, "scroll_gif_wrap.gif"))


if __name__ == "__main__":
    orange = Image.create_from_file(os.path.join(INPUT_DIR, "orange.png"))

    # basic_rewrite(orange)
    # basic_swirl(orange)
    # variable_swirl(orange)
    # varying_variable_swirl(orange)
    # gif()
    # translate_basic(orange)
    # translate_complex(orange)
    # reshape(orange)
    scroll(orange)
