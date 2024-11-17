# main.py

import sys
import argparse
from simulation.canvas import Canvas
from simulation.diffusion import DiffusionSimulator
from simulation.fluid_flow import FluidFlowSimulator
from visualization.visualizer import Visualizer
from __utils.helpers import add_random_noise
import numpy as np


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Color Diffusion and Propagation Simulation"
    )
    parser.add_argument("--width", type=int, default=400, help="Width of the canvas")
    parser.add_argument("--height", type=int, default=400, help="Height of the canvas")
    parser.add_argument(
        "--scale", type=int, default=2, help="Scale factor for visualization"
    )
    args = parser.parse_args()

    # Initialize canvas
    canvas = Canvas(width=args.width, height=args.height)

    # Initialize simulators
    diffusion_sim = DiffusionSimulator(
        canvas=canvas,
        diffusion_rate=0.1,
        color_decay=0.001,
        mixing_strength=0.4,
    )
    fluid_flow_sim = FluidFlowSimulator(
        canvas, viscosity=0.15, diffusion=0.0005, gravity=0.02
    )

    # Initialize visualizer
    visualizer = Visualizer(
        canvas,
        width=args.width * args.scale,
        height=args.height * args.scale,
        scale=args.scale,
    )

    def simulation_step():
        """
        Advances the simulation by one step.
        """
        # Update simulation parameters based on sliders
        diffusion_sim.diffusion_rate = visualizer.diffusion_slider.get_current_value()
        fluid_flow_sim.gravity = visualizer.gravity_slider.get_current_value()
        fluid_flow_sim.viscosity = visualizer.viscosity_slider.get_current_value()

        # print("Diffusion Rate: ", diffusion_sim.diffusion_rate)
        # print("Gravity: ", fluid_flow_sim.gravity)
        # print("Viscosity: ", fluid_flow_sim.viscosity)

        # Perform simulation steps
        diffusion_sim.step()
        fluid_flow_sim.step()

        # Add stochastic noise
        # add_random_noise(canvas, intensity=0.01)

    # Run the visualization loop
    visualizer.run(simulation_step)


if __name__ == "__main__":
    main()
