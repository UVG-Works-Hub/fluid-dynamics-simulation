# visualization/visualizer.py

import pygame
import numpy as np
from __utils.helpers import interpolate_points

class Visualizer:
    """
    Visualizes the simulation in real-time using Pygame.
    """

    def __init__(self, canvas, width: int = 800, height: int = 600, scale: int = 2):
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
        self.scale = scale
        self.canvas_width = width // scale
        self.canvas_height = height // scale
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Color Diffusion Simulation")
        self.clock = pygame.time.Clock()
        self.running = True
        self.drawing = False
        self.last_pos = None
        # Brush parameters
        self.brush_color = (1.0, 0.0, 0.0)  # Red
        self.brush_intensity = 1.0
        self.brush_size = 5  # Radius in canvas units

    def render(self):
        """
        Renders the current state of the canvas to the screen.
        """
        image = self.canvas.get_color_image()
        # Create a Pygame surface from the NumPy array
        surface = pygame.surfarray.make_surface(image.swapaxes(0, 1))
        # Resize image according to scale
        if self.scale != 1:
            surface = pygame.transform.scale(surface, (self.width, self.height))
        self.screen.blit(surface, (0, 0))
        pygame.display.flip()

    def handle_events(self):
        """
        Handles user input events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.drawing = True
                    x, y = pygame.mouse.get_pos()
                    canvas_x = int(x / self.scale)
                    canvas_y = int(y / self.scale)
                    self.add_brush_stroke(canvas_x, canvas_y)
                    self.last_pos = (canvas_x, canvas_y)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    self.drawing = False
                    self.last_pos = None
            elif event.type == pygame.MOUSEMOTION:
                if self.drawing:
                    x, y = pygame.mouse.get_pos()
                    canvas_x = int(x / self.scale)
                    canvas_y = int(y / self.scale)
                    if self.last_pos is not None:
                        # Interpolate points between last_pos and current_pos for smooth drawing
                        interpolated_points = interpolate_points(self.last_pos, (canvas_x, canvas_y), self.brush_size)
                        for point in interpolated_points:
                            self.add_brush_stroke(point[0], point[1])
                    else:
                        self.add_brush_stroke(canvas_x, canvas_y)
                    self.last_pos = (canvas_x, canvas_y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def add_brush_stroke(self, x: int, y: int):
        """
        Adds a brush stroke at the specified canvas coordinates.

        Parameters:
            x (int): X-coordinate on the canvas.
            y (int): Y-coordinate on the canvas.
        """
        # Draw a circle of brush_size radius
        for dx in range(-self.brush_size, self.brush_size + 1):
            for dy in range(-self.brush_size, self.brush_size + 1):
                if dx**2 + dy**2 <= self.brush_size**2:
                    px = x + dx
                    py = y + dy
                    if 0 <= px < self.canvas.width and 0 <= py < self.canvas.height:
                        # Add color source with specified intensity
                        current_color = self.brush_color
                        self.canvas.red[py, px] += current_color[0] * self.brush_intensity
                        self.canvas.green[py, px] += current_color[1] * self.brush_intensity
                        self.canvas.blue[py, px] += current_color[2] * self.brush_intensity
        # Ensure color channels are within [0, 1]
        self.canvas.red = np.clip(self.canvas.red, 0, 1)
        self.canvas.green = np.clip(self.canvas.green, 0, 1)
        self.canvas.blue = np.clip(self.canvas.blue, 0, 1)

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
