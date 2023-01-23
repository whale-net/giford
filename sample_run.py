from datetime import datetime
from salt_shaker.image import Image
from salt_shaker.image_actions.swirl import (
    BasicSwirl,
    VariableSwirl,
    VaryingVariableSwirl,
)

orange_image = Image.create_from_file("./sample_data/orange.png")
orange_image.write_to_file("./sample_output/orange_simple_rewrite.png")

basic_swirl = BasicSwirl()
output_image = basic_swirl.process(orange_image)

# filetime = datetime.now().strftime("%Y%m%d-%H%M%S")
output_image.write_to_file(f"./sample_output/orange_basic_swirl.png")


variable_swirl = VariableSwirl()
output_image_depth_5 = variable_swirl.process(orange_image, 5)
output_image_depth_5.write_to_file(f"./sample_output/orange_variable_swirl_depth_5.png")
output_image_depth_10 = variable_swirl.process(orange_image, 10)
output_image_depth_10.write_to_file(
    f"./sample_output/orange_variable_swirl_depth_10.png"
)

# this will take a while
varying_variable_swirl = VaryingVariableSwirl()
output_varying_25 = varying_variable_swirl.process(orange_image, 25)
for i, img in enumerate(output_varying_25):
    if not (i % 5 == 0):
        continue
    img.write_to_file(f"./sample_output/orange_varying_variable_swirl_depth_{i}.png")
