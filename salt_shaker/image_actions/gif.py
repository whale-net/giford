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

        #ffmpeg -f image2 -framerate 1 -i ./local_test_output/gif_test/gnomechild_varying_variable_swirl_depth_%02d.png -loop -1 local_test_output/test_gnome.gif -y
        (
            ffmpeg
            .input('./local_test_output/gif_test/gnomechild_varying_variable_swirl_depth_%02d.png', framerate=4, format='image2')
            # loop -1=>no loop, 1=> loop 1 time, 2=> loop 2 times, nothing->what you want
            .output(f'./local_test_output/gifify_{temp_str}.gif')#, loop=-1)
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
