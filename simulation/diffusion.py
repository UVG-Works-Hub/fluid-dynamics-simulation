# simulation/diffusion.py

import numpy as np
from scipy.ndimage import convolve

class DiffusionSimulator:
    """
    Simulates color diffusion on the canvas using the heat equation.
    Supports isotropic and anisotropic diffusion.
    """

    def __init__(self, canvas, diffusion_rate: float = 0.1, anisotropy: float = 1.0):
        """
        Initializes the diffusion simulator.

        Parameters:
            canvas (Canvas): The virtual canvas.
            diffusion_rate (float): Rate of diffusion.
            anisotropy (float): Degree of anisotropy in diffusion.
        """
        self.canvas = canvas
        self.diffusion_rate = diffusion_rate
        self.anisotropy = anisotropy # @ref: https://www.nde-ed.org/Physics/Materials/Structure/anisotropy.xhtml

        # Define convolution kernel for Laplacian
        self.kernel_iso = np.array([[0, 1, 0],
                                    [1, -4, 1],
                                    [0, 1, 0]], dtype=np.float32) # @ref: https://homepages.inf.ed.ac.uk/rbf/HIPR2/log.htm
