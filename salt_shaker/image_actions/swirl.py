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

        return ImageAction._unlistify_output(processed_images)


class VariableSwirl(ImageAction):
    def __init__(self):
        super().__init__()

    def process(
        self, image_input: Image | list[Image], depth: int
    ) -> Image | list[Image]:
        if not isinstance(depth, int):
            raise Exception(f"depth is not valid int [{depth}]")
        if depth < 0:
            # todo - make fun thing with negatives
            raise Exception(f"depth cannot be negative [{depth}]")

        image_input = ImageAction._listify_input(image_input)

        processed_images: list[Image] = []
        basic_swirl = BasicSwirl()
        for img in image_input:
            for i in range(0, depth):
                img = basic_swirl.process(img)
            processed_images.append(img)

        return ImageAction._unlistify_output(processed_images)
