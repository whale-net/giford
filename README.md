# giford

## about
modify images and create gifs with unified toolkit


## manifesto:
lowercase because it's friendly

newlines at end of files because it's nice

## setup
todo - package config
packages - scikit-image (skimage), ffmpeg
python sample_run.py

python >=3.7
needed because:
```
from __future__ import annotations
```

install required modules
```
pip install -e .

# if running development locally do this:
pip install -e .[dev]
```

## building

```
pip install build
pip install setuptools-scm
python -m build
```