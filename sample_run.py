from datetime import datetime
from salt_shaker.image import Image
from salt_shaker.image_actions.swirl import BasicSwirl, VariableSwirl

orange_image = Image.create_from_file("./sample_data/orange.png")

basic_swirl = BasicSwirl()
output_image = basic_swirl.process(orange_image)

# filetime = datetime.now().strftime("%Y%m%d-%H%M%S")
output_image.write_to_file(f"./sample_output/orange_basic_swirl.png")


variable_swirl = VariableSwirl()
output_image_depth_5 = variable_swirl.process(orange_image, 5)
output_image_depth_5.write_to_file(f"./sample_output/orange_variable_swirl_depth_5.png")
