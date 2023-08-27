# giford
[![Pytest](https://github.com/whale-net/giford/actions/workflows/pytest.yml/badge.svg)](https://github.com/whale-net/giford/actions/workflows/pytest.yml)
[![codecov](https://codecov.io/gh/whale-net/giford/graph/badge.svg?token=QX182ZYMHN)](https://codecov.io/gh/whale-net/giford)

## about
modify images and create gifs with unified toolkit

### concepts

![giford_concepts](./diagrams/giford_concepts.drawio.svg)

### class diagram (very crude)

![giford_class_diagram](./diagrams/giford_architecture.drawio.svg)

## manifesto:
lowercase because it's friendly

newlines at end of files because it's nice

if you understand why an image manipulation library needs a manifesto, then you arent thinking little enough

## setup
todo - package config
packages - scikit-image (skimage), ffmpeg
python sample_run.py

python >=3.11
needed because:
```
from typing import Self
```

install required for developmet
will install linters, pytest and all supporting modules for those
```
pip install -e .[dev]
```

## building

```
pip install build
pip install setuptools-scm
python -m build
```

## coverage wheel
[![coveragegraph](https://codecov.io/gh/whale-net/giford/graphs/sunburst.svg?token=QX182ZYMHN)](https://codecov.io/gh/whale-net/giford)

## sometimes things don't go right
![whoops](./whoops_example.gif)
![whoops](./whoops_example2.gif)
