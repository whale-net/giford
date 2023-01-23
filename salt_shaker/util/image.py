from salt_shaker.image import Image


def is_all_img_same_shape(imgs: list[Image], is_check_depth: bool = False) -> bool:
    """
    returns true if all images are the same size
    """
    if len(imgs) == 1:
        return True

    base_img = imgs[0]
    for compare_img in imgs[1:]:
        if not base_img.image_data.is_same_shape(
            compare_img.image_data, is_check_depth
        ):
            return False

    return True
