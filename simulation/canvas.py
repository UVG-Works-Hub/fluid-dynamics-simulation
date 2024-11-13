# simulation/canvas.py

import numpy as np


class Canvas:
    """
    Represents the virtual canvas where color diffusion and propagation occur.
    """

    def __init__(self, width: int, height: int):
        """
        Initializes the canvas with given dimensions.

        Parameters:
            width (int): Width of the canvas.
            height (int): Height of the canvas.
        """
        self.width = width
        self.height = height
        # Initialize RGB channels
        self.red = np.zeros((height, width), dtype=np.float32)
        self.green = np.zeros((height, width), dtype=np.float32)
        self.blue = np.zeros((height, width), dtype=np.float32)
        # Initialize barriers (1: barrier, 0: free space)
        self.barriers = np.zeros((height, width), dtype=np.float32)

    def clear(self):
        """
        Clears the canvas by resetting all color channels.
        """
        self.red.fill(0)
        self.green.fill(0)
        self.blue.fill(0)

    def add_color_source(self, x: int, y: int, color: tuple, intensity: float = 1.0):
        """
        Adds a color source at the specified position.

        Parameters:
            x (int): X-coordinate.
            y (int): Y-coordinate.
            color (tuple): RGB color as a tuple of floats (0-1).
            intensity (float): Intensity of the color source.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.red[y, x] += color[0] * intensity
            self.green[y, x] += color[1] * intensity
            self.blue[y, x] += color[2] * intensity

    def add_barrier(self, x: int, y: int):
        """
        Adds a barrier at the specified position.

        Parameters:
            x (int): X-coordinate.
            y (int): Y-coordinate.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.barriers[y, x] = 1.0

    def get_color_image(self) -> np.ndarray:
        """
        Combines RGB channels into a single image array.

        Returns:
            np.ndarray: Combined RGB image.
        """
        image = np.stack((self.red, self.green, self.blue), axis=-1)
        # Normalize to [0, 255] for visualization
        image = np.clip(image * 255, 0, 255).astype(np.uint8)
        return image
