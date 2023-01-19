import os

import ffmpeg
import numpy as np
import uuid
from skimage import transform

from salt_shaker.image import Image
from salt_shaker.image_actions.image_action import ImageAction


class Gifify(ImageAction):
    def __init__(self):
        super().__init__()

    def process(self, image_input: Image | list[Image]) -> Image | list[Image]:
        image_input = ImageAction._listify_input(image_input)

        #processed_images: list[Image] = []
        # for img in image_input:
        #for i in range(0, 24):
        # c string style (i think) -> fill 0 5depth
        #img_path = os.path.abspath(f'./local_test_data/gif_test/gnomechild_varying_variable_swirl_depth_%02d.png')
        #img_path = os.path.abspath(f'./local_test_data/gif_test/*.png')

        # make it unique
        temp_str = str(uuid.uuid4())[0:8]

        #ffmpeg -f image2 -framerate 1 -i local_test_data/gnomechild.png -loop -1 local_test_output/test_gnome.gif
        # this gif command works:
        #ffmpeg -f image2 -framerate 1 -i ./local_test_output/gif_test/gnomechild_varying_variable_swirl_depth_%02d.png -loop -1 local_test_output/test_gnome.gif -y
        out, _  = (
            ffmpeg
            # todo, cstring pattern?
            .input('./local_test_output/gif_test/gnomechild_varying_variable_swirl_depth_%02d.png', framerate=12)
            #.output(f'./local_test_output/test_mp4_{temp_str}.mp4')
            # vframes
            .output(f'./local_test_output/gifify_{temp_str}.gif', format='image2', loop=-1, frames=24, vframes=1)
            .overwrite_output()
            .run()
            # read video to local variable
            #.run(capture_stdout=True)
        )

            # todo later
            # video = (
            #         np
            #         .frombuffer(out, np.uint8)
            #         .reshape([-1, height, width, 3])
            #     )

        #processed_images.append(img.clone())

        return
        #return ImageAction._unlistify_output(processed_images)

