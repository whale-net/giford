# only needed for pypi
import os.path

from setuptools import setup


if __name__ == "__main__":
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    with open(readme_path, encoding="utf-8") as f:
        # todo use md comments to make pypi friendly description
        readme = f.read()

    setup(
        long_description=readme,
        long_description_content_type="text/markdown",
    )
