from skimage import transform

from salt_shaker.image import Image
from salt_shaker.image_actions.image_action import ImageAction
from salt_shaker.image_batch import ImageBatch


class BasicSwirl(ImageAction):
    def __init__(self):
        super().__init__()

    def process(self, input_batch: ImageBatch) -> ImageBatch:
        output_batch = ImageBatch()
        for img in input_batch.images:
            img_nd_arr = transform.swirl(img.image_data.as_3d_ndarray())
            output_batch.add_image(Image.create_from_ndarray(img_nd_arr))

        return output_batch


class VariableSwirl(ImageAction):
    def __init__(self):
        super().__init__()

    def process(self, input_batch: ImageBatch, depth: int) -> ImageBatch:
        if not isinstance(depth, int):
            raise Exception(f"depth is not valid int [{depth}]")
        if depth < 0:
            # todo - make fun thing with negatives
            raise Exception(f"depth cannot be negative [{depth}]")

        output_batch = ImageBatch()
        basic_swirl = BasicSwirl()
        for img in input_batch.images:
            # turn each image in input_batch into its own batch so we can feed it into another action
            batch = ImageBatch()
            batch.add_image(img)
            for i in range(0, depth):
                batch = basic_swirl.process(batch)
            # TODO - do we need to clone?
            output_batch.add_batch(batch)

        return output_batch


class VaryingVariableSwirl(ImageAction):
    def __init__(self):
        super().__init__()

    def process(self, input_batch: ImageBatch, depth: int) -> ImageBatch:
        """
        if multiple images are passed in, array with size len(image_input)*depth return
        index with [image_idx * depth + depth_idx]
        """
        if not isinstance(depth, int):
            raise Exception(f"depth is not valid int [{depth}]")
        if depth < 0:
            # todo - make fun thing with negatives
            raise Exception(f"depth cannot be negative [{depth}]")

        output_batch = ImageBatch()
        variable_swirl = VariableSwirl()
        for img in input_batch.images:
            # turn each image in input_batch into its own batch so we can feed it into another action
            batch = ImageBatch()
            batch.add_image(img)
            for i in range(0, depth):
                batch = variable_swirl.process(batch, i)
                output_batch.add_batch(batch)

        return output_batch
