# Hough Algorithm for Detecting Lines

This project implements the Hough transform algorithm for detecting lines in images. The Hough transform is a popular technique in computer vision for detecting geometric shapes, particularly lines in images.

## Features

- **Hough Transform**: Detect lines in images using the Hough transform algorithm.
- **Visualization**: Display the original image and its Hough transform to visualize detected lines.

## Installation

1. Clone the repository:

    ```bash
    git clone git@github.com:cucumparty/iitp_6_python.git
    cd iitp_6_python
    ```

## Usage

The main functionality is provided through the `hough_line` and `detect_and_draw_lines` functions in the `hough_lines.py` module.

```python
from iitp_6_python import hough_lines
import numpy as np
import imageio

# Load an image
img = imageio.imread("path/to/your/image.jpg")

# Detect lines in the image
accumulator, thetas, rhos = hough_lines.hough_line(img)

# Display the original image and its Hough transform
hough_lines.show_hough_line(img, accumulator, thetas, rhos)
```


```python
from iitp_6_python import hough_lines
import numpy as np
import imageio
import matplotlib.pyplot as plt

# Load an image
img = imageio.imread("path/to/your/image.jpg")

# Detect and draw lines on the image
result_image = hough_lines.detect_and_draw_lines(img)

# Display the result image
plt.imshow(result_image, cmap='gray')
plt.axis('off')
plt.show()
```

## Documentation

The documentation for this project can be found in the `docs/_build/index.html` file. You can open this file in your web browser to view the detailed documentation, including usage instructions, API references, and examples.

## Nox Sessions

This project includes several [Nox](https://nox.thea.codes/en/stable/) sessions for automation tasks. You can use these sessions to perform various tasks such as linting, testing, type-checking, and building documentation.

To run Nox sessions, make sure you have [Nox](https://nox.thea.codes/en/stable/) installed. Then, execute the desired session by running the following command in your terminal:

```bash
nox -s session_name
```

### Available Sessions

- `typeguard`: Runtime type checking using Typeguard.
- `mypy`: Type-check using mypy.
- `tests`: Run the test suite.
- `lint`: Lint using flake8.
- `black`: Run black code formatter.
- `safety`: Scan dependencies for insecure packages.
- `pytype`: Type-check using pytype.
- `xdoctest`: Run examples with xdoctest.
- `docs`: Build the documentation.

For example, to run linting, execute:

```bash
nox -s lint
