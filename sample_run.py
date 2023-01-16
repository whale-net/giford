from datetime import datetime
from salt_shaker.image import Image
from salt_shaker.image_actions.swirl import BasicSwirl

gnome_image = Image.create_from_file("./sample_data/orange.png")

swirl_basic = BasicSwirl()
output_image = swirl_basic.process(gnome_image)

#filetime = datetime.now().strftime("%Y%m%d-%H%M%S")
output_image.write_to_file(f'./sample_output/orange_basic_swirl.png')
