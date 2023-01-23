import os
import tempfile
import ffmpeg
import numpy as np
import uuid
from skimage import transform

from salt_shaker.image import Image
from salt_shaker.image_actions.image_action import ImageAction
from salt_shaker.raw_data import RawDataVideo
from salt_shaker.image_batch import ImageBatch


class Gifify(ImageAction):
    def __init__(self):
        super().__init__()

    def process(self, input_batch: ImageBatch) -> ImageBatch:
        """
        takes list of images and returns a gif
        """
        # c string style (i think) -> fill 0 5depth
        # img_path = os.path.abspath(f'./local_test_data/gif_test/gnomechild_varying_variable_swirl_depth_%02d.png')
        # img_path = os.path.abspath(f'./local_test_data/gif_test/*.png')

        # validate shape and create raw_video
        if not input_batch.is_all_img_same_shape():
            raise Exception("not all images are same size in input")
        rdv = RawDataVideo()
        for img in input_batch.images:
            rdv.add_frame(img.image_data)

        # python scoping allows me to get away with this
        height = img.image_data.height
        width = img.image_data.width

        vid_ndarr = rdv.as_ndarray()

        # TODO - look at https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md#tensorflow-streaming
            # and make this buffered

        # working video output
        # out, _ = (
        #     ffmpeg.input(
        #         "pipe:",
        #         video_size='120x120',
        #         format='rawvideo',
        #         pix_fmt='rgba'
        #     )
        #     .output(
        #         # rgb8 is correct, rgba is 4x more data so need to store differently
        #         # rgb8 is not correct, that's monochrome. rgba is 32 bit + alpha
        #         "pipe:", format="rawvideo", pix_fmt="rgba"#pix_fmt="rgba"
        #     ).overwrite_output()  # outputs 25 frames of 120x120x120x4
        #     .run(capture_stdout=True, input=vid_ndarr.astype(np.uint8).tobytes())
        # )

        out, _ = (
            ffmpeg.input(
                "pipe:",
                s=f'{height},{width}',
                format='rawvideo',
                pix_fmt='rgba',
                framerate=5
            )
            # .filter(
            #
            # )
            .output(
                'pipe:', format='gif'
            )
            .run(capture_stdout=True, input=vid_ndarr.astype(np.uint8).tobytes())
        )


        #output_batch = ImageBatch()
        #output_batch.add_image(Image.create_from_bytes(out, height=120, width=120))


        return out #output_batch


        # ffmpeg -f image2 -framerate 1 -i ./local_test_output/gif_test/gnomechild_varying_variable_swirl_depth_%02d.png -loop -1 local_test_output/test_gnome.gif -y
        # tf = tempfile.NamedTemporaryFile()
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = f"{temp_dir}/temp_gif.gif"
            out, _ = (
                ffmpeg.input(
                    "./local_test_output/gif_test/gnomechild_varying_variable_swirl_depth_%02d.png",
                    framerate=4,
                    format="image2",
                )
                # loop -1=>no loop, 1=> loop 1 time, 2=> loop 2 times, nothing->what you want
                # .output(f'./local_test_output/gifify_{temp_str}.gif')#, loop=-1)
                # .output(file_path)
                # .run()
                # do I need rawvideo format? pixfmt? just copying it for now
                # .output('pipe:', format='rawvideo', pix_fmt='rgb24')
                # rgb8 works, but is big array, rgb24 does not work
                # .output('pipe:', format='gif', pix_fmt='rgb8')#, pix_fmt='rgb24')
                .output(
                    "pipe:", format="rawvideo", pix_fmt="rgba"
                ).overwrite_output()  # outputs 25 frames of 120x120x120x4
                # read video to local variable
                .run(capture_stdout=True)
            )

            # TODO - writing to temp path right now, likely not ideal.
            # need to learn more about what the scikit image structure is and see how to build something that is compatible between the two
            import shutil

            shutil.copyfile(file_path, "./local_test_output/gif_pre_wrapper.gif")

            img = Image.create_from_file(file_path)

        # invalid pixel format or something
        # height = 120
        # width = 120
        # video = (
        #     np
        #     .frombuffer(out, np.uint8)
        #     .reshape([-1, height, width, 3])
        # )
        # img = Image.create_from_ndarray(video)

        # todo later
        # video = (
        #         np
        #         .frombuffer(out, np.uint8)
        #         .reshape([-1, height, width, 3])
        #     )

        # processed_images.append(img.clone())

        return img
        # return ImageAction._unlistify_output(processed_images)
