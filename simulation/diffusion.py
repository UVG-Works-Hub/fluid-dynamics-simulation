# simulation/diffusion.py

import numpy as np
from scipy.ndimage import convolve


class DiffusionSimulator:
    """
    Simulates color diffusion on the canvas using the heat equation.
    Supports per-channel diffusion rates, color mixing, and color decay.
    """

    def __init__(
        self,
        canvas,
        diffusion_rates: dict = None,
        color_decay: float = 0.01,
        mixing_strength: float = 0.02,
    ):
        """
        Initializes the diffusion simulator.

        Parameters:
            canvas (Canvas): The virtual canvas.
            diffusion_rates (dict): Dictionary specifying diffusion rates for each color channel.
                                    Example: {'red': 0.1, 'green': 0.05, 'blue': 0.07}
            color_decay (float): Rate at which colors decay (fade) over time. Range: [0, 1]
            mixing_strength (float): Strength of color mixing between channels.
        """
        self.canvas = canvas

        # Set default diffusion rates if not provided
        if diffusion_rates is None:
            self.diffusion_rates = {"red": 0.1, "green": 0.1, "blue": 0.1}
        else:
            self.diffusion_rates = diffusion_rates

        self.color_decay = color_decay
        self.mixing_strength = mixing_strength

        # Define convolution kernel for Laplacian (standard for diffusion)
        self.laplacian_kernel = np.array(
            [[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32
        )

        # Define convolution kernel for simple color mixing (blending neighboring pixels)
        self.mixing_kernel = np.array(
            [[0.0, 0.05, 0.0], [0.05, 0.8, 0.05], [0.0, 0.05, 0.0]], dtype=np.float32
        )

    def step(self):
        """
        Performs one diffusion step on the canvas with essential color enhancements.
        """
        for channel in ["red", "green", "blue"]:
            # Retrieve the current color channel data
            data = getattr(self.canvas, channel)

            # Compute Laplacian for diffusion
            laplacian = convolve(data, self.laplacian_kernel, mode="reflect")

            # Apply per-channel diffusion rate
            diffusion = self.diffusion_rates[channel] * laplacian

            # Update the color channel with diffusion
            new_data = data + diffusion

            # Apply color mixing to promote natural blending
            mixed_data = convolve(new_data, self.mixing_kernel, mode="reflect")

            # Apply color decay to gradually fade colors over time
            decayed_data = mixed_data * (1 - self.color_decay)

            # Update the canvas with the new color data
            setattr(self.canvas, channel, decayed_data)

            # Ensure color channels remain within [0, 1]
            setattr(self.canvas, channel, np.clip(getattr(self.canvas, channel), 0, 1))

    def set_diffusion_rates(self, diffusion_rates: dict):
        """
        Updates the diffusion rates for each color channel.

        Parameters:
            diffusion_rates (dict): Dictionary specifying diffusion rates for each color channel.
        """
        for channel in ["red", "green", "blue"]:
            if channel in diffusion_rates:
                self.diffusion_rates[channel] = diffusion_rates[channel]

    def set_color_decay(self, decay: float):
        """
        Updates the color decay rate.

        Parameters:
            decay (float): New color decay rate. Range: [0, 1]
        """
        self.color_decay = decay

    def set_mixing_strength(self, strength: float):
        """
        Updates the color mixing strength.

        Parameters:
            strength (float): New mixing strength. Higher values increase blending between channels.
        """
        self.mixing_strength = strength
        # Update the mixing kernel based on the new strength
        self.mixing_kernel = np.array(
            [
                [0.0, self.mixing_strength, 0.0],
                [
                    self.mixing_strength,
                    1 - 4 * self.mixing_strength,
                    self.mixing_strength,
                ],
                [0.0, self.mixing_strength, 0.0],
            ],
            dtype=np.float32,
        )
