import ffmpeg
import skimage
import datetime

# TODO input directory and such needs to be more standard and relative
image = skimage.io.imread("./1639-gnomechild.png")
print(type(image))
print(image.shape)


image = skimage.transform.swirl(image)
image = skimage.transform.swirl(image)
image = skimage.transform.swirl(image)
image = skimage.transform.swirl(image)
image = skimage.transform.swirl(image)

filetime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
print(filetime)
skimage.io.imsave(f"./output/gnome_test_{filetime}.png", image)

"""
# TODO intermediate? build pipeline?
try to see if we can make this into an airflow project. operators for each transformation? 
would only be worth it if the operator makes file handling easy otherwise not really worth it imo
am I going too far with the steps? I think having the gif thing separate would be beneficial, especially if files shared
then I can just feed list of images and have it automanaged

need gif step

need to think about how to process gifs too, but maybe not too much of an issue now
maybe video gif too? unsure about limits

https://airflow.apache.org/docs/apache-airflow/stable/concepts/overview.html
https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html#using-official-airflow-helm-chart

https://scikit-image.org/docs/stable/api/skimage.transform.html
https://scikit-image.org/docs/stable/api/skimage.io.html#skimage.io.imsave
https://scikit-image.org/docs/stable/auto_examples/index.html
https://scikit-image.org/docs/stable/auto_examples/transform/plot_geometric.html#sphx-glr-auto-examples-transform-plot-geometric-py
https://kkroening.github.io/ffmpeg-python/
"""
