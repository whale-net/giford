from skimage import transform

from salt_shaker.image import Image
from salt_shaker.image_actions.image_action import ImageAction


class BasicSwirl(ImageAction):
    def __init__(self):
        super().__init__()

    def process(self, image_input: Image | list[Image]) -> Image | list[Image]:
        image_input = ImageAction._listify_input(image_input)

        processed_images: list[Image] = []
        for img in image_input:
            img.image_data = transform.swirl(img.image_data)
            processed_images.append(img)

        return processed_images[0] if len(processed_images) == 1 else processed_images
