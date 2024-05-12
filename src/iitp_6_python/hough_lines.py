"""Hough algorithm for detecting lines."""

from matplotlib import pyplot as plt
import numpy as np
import cv2
import imageio
import math


def hough_line(
    img: np.ndarray,
    angle_step: int = 1,
    lines_are_white: bool = True,
    value_threshold: int = 5,
) -> tuple:
    """Hough transform for lines.

    Args:
        img (np.ndarray): 2D binary image with nonzeros representing edges.
        angle_step (int): Spacing between angles to use every n-th angle
                          between -90 and 90 degrees. Default step is 1.
        lines_are_white (bool): Boolean indicating whether lines to be detected are white.
                                Defaults to True.
        value_threshold (int): Pixel values above or below the value_threshold are edges.
                               Defaults to 5.

    Returns:
        tuple: A tuple containing:
            accumulator (np.ndarray): 2D array of the hough transform accumulator.
            theta (np.ndarray): Array of angles used in computation, in radians.
            rhos (np.ndarray): Array of rho values. Max size is 2 times the diagonal
                               distance of the input image.

    Examples:
        >>> from iitp_6_python import hough_lines
        >>> img = np.zeros((100, 100), dtype=np.uint8)
        >>> img[25:75, 40:60] = 255
        >>> accumulator, thetas, rhos = hough_lines.hough_line(img)
    """
    # Rho and Theta ranges
    thetas = np.deg2rad(np.arange(-90.0, 90.0, angle_step))
    width, height = img.shape[:2]
    diag_len = int(round(math.sqrt(width * width + height * height)))
    rhos = np.linspace(-diag_len, diag_len, diag_len * 2)

    # Cache some reusable values
    cos_t = np.cos(thetas)
    sin_t = np.sin(thetas)
    num_thetas = len(thetas)

    # Hough accumulator array of theta vs rho
    accumulator = np.zeros((2 * diag_len, num_thetas), dtype=np.uint8)
    # (row, col) indexes to edges
    are_edges = img > value_threshold if lines_are_white else img < value_threshold
    y_idxs, x_idxs = np.nonzero(are_edges)

    # Vote in the hough accumulator
    for i in range(len(x_idxs)):
        x = x_idxs[i]
        y = y_idxs[i]

        for t_idx in range(num_thetas):
            # Calculate rho. diag_len is added for a positive index
            rho = diag_len + int(round(x * cos_t[t_idx] + y * sin_t[t_idx]))
            accumulator[rho, t_idx] += 1

    return accumulator, thetas, rhos


def show_hough_line(
    img: np.ndarray,
    accumulator: np.ndarray,
    thetas: np.ndarray,
    rhos: np.ndarray,
    save_path: str = "./",
) -> None:
    """Display the original image and its Hough transform.

    Args:
        img (np.ndarray): Input image.
        accumulator (np.ndarray): Hough transform accumulator.
        thetas (np.ndarray): Array of angles used in computation, in radians.
        rhos (np.ndarray): Array of rho values. Max size is 2 times the diagonal
                           distance of the input image.
        save_path (str): Path to save the figure. Defaults to None.

    Examples:
        >>> img = np.zeros((100, 100), dtype=np.uint8)
        >>> img[25:75, 40:60] = 255
        >>> accumulator, thetas, rhos = hough_line(img)
        >>> show_hough_line(img, accumulator, thetas, rhos)
    """
    fig, ax = plt.subplots(1, 2, figsize=(10, 10))

    ax[0].imshow(img, cmap=plt.cm.gray)
    ax[0].set_title("Input image")
    ax[0].axis("image")

    ax[1].imshow(
        accumulator,
        extent=[np.rad2deg(thetas[-1]), np.rad2deg(thetas[0]), rhos[-1], rhos[0]],
    )
    ax[1].set_aspect("equal", adjustable="box")
    ax[1].set_title("Hough transform")
    ax[1].set_xlabel("Angles (degrees)")
    ax[1].set_ylabel("Distance (pixels)")
    ax[1].axis("image")

    if save_path is not None:
        plt.savefig(save_path, bbox_inches="tight")
    plt.show()


def detect_and_draw_lines(
    image: np.ndarray,
    angle_step: int = 1,
    lines_are_white: bool = True,
    value_threshold: int = 5,
) -> np.ndarray:
    """Detect lines in an image using Hough transform and draw them on the original image.

    Args:
        image (np.ndarray): The input image.
        angle_step (int): Spacing between angles to use every n-th angle
                          between -90 and 90 degrees. Default step is 1.
        lines_are_white (bool): Boolean indicating whether lines to be detected are white.
                                Defaults to True.
        value_threshold (int): Pixel values above or below the value_threshold are edges.
                               Defaults to 5.

    Returns:
        np.ndarray: The original image with detected lines drawn on it.

    Examples:
        >>> img = imageio.imread("./src/iitp_6_python/images/road.jpeg")
        >>> result_image = detect_and_draw_lines(img)
        >>> plt.imshow(result_image, cmap='gray')
        >>> plt.axis('off')
        >>> plt.show()
    """
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise and improve edge detection
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Perform Canny edge detection
    edges = cv2.Canny(blurred_image, 50, 150)

    # Perform Hough transform to detect lines
    accumulator, thetas, rhos = hough_line(
        edges, angle_step, lines_are_white, value_threshold
    )

    # Find peaks in the Hough accumulator
    threshold = 0.5 * np.max(accumulator)
    rho_indices, theta_indices = np.where(accumulator >= threshold)

    # Draw detected lines on the original image
    image_with_lines = np.copy(image)
    for rho_idx, theta_idx in zip(rho_indices, theta_indices):
        rho = rhos[rho_idx]
        theta = thetas[theta_idx]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(image_with_lines, (x1, y1), (x2, y2), (0, 0, 255), 2)

    return image_with_lines


if __name__ == "__main__":
    img = imageio.imread("src/iitp_6_python/images/road.jpeg")
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Binary image
    _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
    accumulator, thetas, rhos = hough_line(binary_image)
    show_hough_line(img, accumulator, thetas, rhos, save_path="./images")
    result_image = detect_and_draw_lines(img)
    cv2.imwrite("result_image_with_lines.png", result_image)
