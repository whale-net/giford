# only needed for pypi
import os.path

from setuptools import setup

def get_version():
    from setuptools_scm.version import get_local_dirty_tag
    def clean_scheme(version):
        return get_local_dirty_tag(version) if version.dirty else '+clean'

    return {'local_scheme': clean_scheme}

if __name__ == '__main__':

    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_path, encoding="utf-8") as f:
        # todo use md comments to make pypi friendly description
        readme = f.read()


    setup(
        long_description=readme,
        long_description_content_type='text/markdown',
        use_scm_version=get_version,
    )