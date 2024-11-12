# simulation/fluid_flow.py

import numpy as np
from scipy.ndimage import convolve

class FluidFlowSimulator:
    """
    Simulates fluid flow on the canvas using simplified Navier-Stokes equations.
    """

    def __init__(self, canvas, viscosity: float = 0.1, diffusion: float = 0.0001):
        """
        Initializes the fluid flow simulator.

        Parameters:
            canvas (Canvas): The virtual canvas.
            viscosity (float): Viscosity of the fluid.
            diffusion (float): Diffusion rate of velocity.
        """
        self.canvas = canvas
        self.viscosity = viscosity
        self.diffusion = diffusion
        self.u = np.zeros((canvas.height, canvas.width), dtype=np.float32)  # Horizontal velocity
        self.v = np.zeros((canvas.height, canvas.width), dtype=np.float32)  # Vertical velocity
        # Define convolution kernel for Laplacian
        self.kernel = np.array([[0, 1, 0],
                                [1, -4, 1],
                                [0, 1, 0]], dtype=np.float32)

    def step(self):
        """
        Performs one fluid flow simulation step.
        """
        # Compute Laplacian for diffusion
        u_lap = convolve(self.u, self.kernel, mode='reflect')
        v_lap = convolve(self.v, self.kernel, mode='reflect')

        # Update velocities
        self.u += self.diffusion * u_lap - self.viscosity * self.u
        self.v += self.diffusion * v_lap - self.viscosity * self.v

        # Apply barriers by setting velocity to zero at barrier locations
        barriers = self.canvas.barriers
        self.u *= (1 - barriers)
        self.v *= (1 - barriers)

        # Update canvas colors based on velocity
        self.canvas.red += self.u * 0.01
        self.canvas.green += self.v * 0.01
        # Ensure color channels are within [0, 1]
        self.canvas.red = np.clip(self.canvas.red, 0, 1)
        self.canvas.green = np.clip(self.canvas.green, 0, 1)
