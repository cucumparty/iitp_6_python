# Hough Algorithm for Detecting Lines

This project implements the Hough transform algorithm for detecting lines in images. The Hough transform is a popular technique in computer vision for detecting geometric shapes, particularly lines and circles, in images.

## Features

- **Hough Transform**: Detect lines in images using the Hough transform algorithm.
- **Visualization**: Display the original image and its Hough transform to visualize detected lines.
- **Edge Detection**: Use Canny edge detection as a preprocessing step to detect edges in images.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/your_project.git
    cd your_project
    ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

The main functionality is provided through the `hough_line` function in the `hough_lines.py` module.

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
