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
    parser = argparse.ArgumentParser(description="Color Diffusion and Propagation Simulation")
    parser.add_argument('--width', type=int, default=400, help='Width of the canvas')
    parser.add_argument('--height', type=int, default=300, help='Height of the canvas')
    parser.add_argument('--scale', type=int, default=2, help='Scale factor for visualization')
    args = parser.parse_args()

    # Initialize canvas
    canvas = Canvas(width=args.width, height=args.height)

    # Initialize simulators
    diffusion_sim = DiffusionSimulator(canvas, diffusion_rate=0.1, anisotropy=1.0)
    fluid_flow_sim = FluidFlowSimulator(canvas, viscosity=0.1, diffusion=0.0001)

    # Initialize visualizer
    visualizer = Visualizer(canvas, width=args.width*args.scale, height=args.height*args.scale, scale=args.scale)

    def simulation_step():
        """
        Advances the simulation by one step.
        """
        # Perform diffusion
        diffusion_sim.step()
        # Perform fluid flow
        fluid_flow_sim.step()
        # # Perform reaction-diffusion
        # reaction_diffusion_sim.step()
        # Add stochastic noise
        add_random_noise(canvas, intensity=0.01)

    # Run the visualization loop
    visualizer.run(simulation_step)

if __name__ == "__main__":
    main()
