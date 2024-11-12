# utils/helpers.py

import numpy as np

def add_random_noise(canvas, intensity: float = 0.1):
    """
    Adds random noise to the canvas to simulate stochastic propagation.

    Parameters:
        canvas (Canvas): The virtual canvas.
        intensity (float): Intensity of the noise.
    """
    noise_r = np.random.randn(canvas.height, canvas.width) * intensity
    noise_g = np.random.randn(canvas.height, canvas.width) * intensity
    noise_b = np.random.randn(canvas.height, canvas.width) * intensity
    canvas.red += noise_r
    canvas.green += noise_g
    canvas.blue += noise_b
    # Ensure color channels are within [0, 1]
    canvas.red = np.clip(canvas.red, 0, 1)
    canvas.green = np.clip(canvas.green, 0, 1)
    canvas.blue = np.clip(canvas.blue, 0, 1)
