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
