# visualization/visualizer.py

import pygame
import numpy as np

class Visualizer:
    """
    Visualizes the simulation in real-time using Pygame.
    """

    def __init__(self, canvas, width: int = 800, height: int = 600, scale: int = 1):
        """
        Initializes the visualizer.

        Parameters:
            canvas (Canvas): The virtual canvas to visualize.
            width (int): Width of the window.
            height (int): Height of the window.
            scale (int): Scaling factor for display.
        """
        pygame.init()
        self.canvas = canvas
        self.width = width
        self.height = height
        self.scale = scale
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Color Diffusion Simulation")
        self.clock = pygame.time.Clock()
        self.running = True

    def render(self):
        """
        Renders the current state of the canvas to the screen.
        """
        image = self.canvas.get_color_image()
        # Resize image according to scale
        if self.scale != 1:
            image = pygame.transform.scale(pygame.surfarray.make_surface(image), (self.width, self.height))
        else:
            image = pygame.surfarray.make_surface(image)
        self.screen.blit(image, (0, 0))
        pygame.display.flip()

    def handle_events(self):
        """
        Handles user input events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Add a color source on click
                self.canvas.add_color_source(x, y, color=(1.0, 0.0, 0.0), intensity=1.0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def run(self, simulation_step_callback):
        """
        Runs the visualization loop.

        Parameters:
            simulation_step_callback (function): Function to advance the simulation.
        """
        while self.running:
            self.handle_events()
            simulation_step_callback()
            self.render()
            self.clock.tick(60)  # Limit to 60 FPS
        pygame.quit()
