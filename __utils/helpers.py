# __utils/helpers.py

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

def interpolate_points(start, end, brush_size):
    """
    Interpolates points between start and end positions based on brush size.

    Parameters:
        start (tuple): Starting (x, y) coordinates.
        end (tuple): Ending (x, y) coordinates.
        brush_size (int): Radius of the brush.

    Returns:
        list: List of interpolated (x, y) coordinates.
    """
    points = []
    dist = max(abs(end[0] - start[0]), abs(end[1] - start[1]))
    if dist == 0:
        return [start]
    for i in range(dist):
        t = i / dist
        x = int(start[0] + (end[0] - start[0]) * t)
        y = int(start[1] + (end[1] - start[1]) * t)
        points.append((x, y))
    points.append(end)
    return points
