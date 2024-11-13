# simulation/fluid_flow.py

import numpy as np
from scipy.ndimage import convolve


class FluidFlowSimulator:
    """
    Simulates fluid flow on the canvas using simplified Navier-Stokes equations.
    """

    def __init__(
        self,
        canvas,
        viscosity: float = 0.1,
        diffusion: float = 0.0001,
        gravity: float = 0.0,
    ):
        """
        Initializes the fluid flow simulator.

        Parameters:
            canvas (Canvas): The virtual canvas.
            viscosity (float): Viscosity of the fluid.
            diffusion (float): Diffusion rate of velocity.
            gravity (float): Gravitational force applied to vertical velocity.
        """
        self.canvas = canvas
        self.viscosity = viscosity
        self.diffusion = diffusion
        self.gravity = gravity
        self.u = np.zeros(
            (canvas.height, canvas.width), dtype=np.float32
        )  # Horizontal velocity
        self.v = np.zeros(
            (canvas.height, canvas.width), dtype=np.float32
        )  # Vertical velocity
        # Define convolution kernel for Laplacian
        self.kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)

    def bilinear_interpolate(self, d, X, Y):
        x0 = np.floor(X).astype(int)
        x1 = x0 + 1
        y0 = np.floor(Y).astype(int)
        y1 = y0 + 1

        x1 = np.clip(x1, 0, d.shape[1] - 1)
        y1 = np.clip(y1, 0, d.shape[0] - 1)

        Ia = d[y0, x0]
        Ib = d[y1, x0]
        Ic = d[y0, x1]
        Id = d[y1, x1]

        wa = (x1 - X) * (y1 - Y)
        wb = (x1 - X) * (Y - y0)
        wc = (X - x0) * (y1 - Y)
        wd = (X - x0) * (Y - y0)

        return wa * Ia + wb * Ib + wc * Ic + wd * Id

    def advect(self, d, d_prev, u, v, dt):
        height, width = d.shape
        X, Y = np.meshgrid(np.arange(width), np.arange(height))
        X_prev = X - u * dt
        Y_prev = Y - v * dt

        # Clamp the positions to stay within the canvas
        X_prev = np.clip(X_prev, 0, width - 1)
        Y_prev = np.clip(Y_prev, 0, height - 1)

        # Perform bilinear interpolation
        d[:] = self.bilinear_interpolate(d_prev, X_prev, Y_prev)

    def step(self, dt=1.0):
        # Previous state
        u_prev = self.u.copy()
        v_prev = self.v.copy()

        # Compute Laplacian for diffusion
        u_lap = convolve(self.u, self.kernel, mode="reflect")
        v_lap = convolve(self.v, self.kernel, mode="reflect")

        # Update velocities with diffusion and viscosity
        self.u += self.diffusion * u_lap - self.viscosity * self.u
        self.v += self.diffusion * v_lap - self.viscosity * self.v

        # Apply gravity
        self.v += self.gravity

        # Apply barriers by setting velocity to zero at barrier locations
        barriers = self.canvas.barriers
        self.u *= 1 - barriers
        self.v *= 1 - barriers

        # Advect the color channels based on velocity
        red_prev = self.canvas.red.copy()
        green_prev = self.canvas.green.copy()
        blue_prev = self.canvas.blue.copy()

        self.advect(self.canvas.red, red_prev, self.u, self.v, dt)
        self.advect(self.canvas.green, green_prev, self.u, self.v, dt)
        self.advect(self.canvas.blue, blue_prev, self.u, self.v, dt)

        # Ensure color channels are within [0, 1]
        self.canvas.red = np.clip(self.canvas.red, 0, 1)
        self.canvas.green = np.clip(self.canvas.green, 0, 1)
        self.canvas.blue = np.clip(self.canvas.blue, 0, 1)
