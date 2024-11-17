# visualization/visualizer.py

import pygame
import numpy as np
from __utils.helpers import interpolate_points
import pygame_gui
from enum import Enum, auto

class Mode(Enum):
    BRUSH = auto()
    ERASER = auto()
    ADD_BARRIER = auto()
    REMOVE_BARRIER = auto()

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
        self.screen = pygame.display.set_mode(
            (width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE
        )
        pygame.display.set_caption("Color Diffusion Simulation")
        self.clock = pygame.time.Clock()
        self.running = True
        self.drawing = False
        self.last_pos = None
        # Brush parameters
        self.brush_color = (1.0, 0.0, 0.0)  # Red
        self.brush_intensity = 1.0
        self.brush_size = 5  # Radius in canvas units

        self.mode = Mode.BRUSH  # Initial mode

        self.ui_manager = pygame_gui.UIManager((self.width, self.height))
        self.create_ui_elements()

    def create_ui_elements(self):
        # Label for brush size slider
        self.brush_size_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, -10), (200, 30)),
            text=f"Brush Size: {self.brush_size}",
            manager=self.ui_manager,
        )
        # Slider for brush size
        self.brush_size_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 10), (200, 30)),
            start_value=self.brush_size,
            value_range=(1, 50),
            manager=self.ui_manager,
        )

        # Label for diffusion slider
        self.diffusion_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 30), (200, 30)),
            text=f"Diffusion Rate: {0.1}",
            manager=self.ui_manager,
        )
        # Sliders for simulation parameters
        self.diffusion_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 50), (200, 30)),
            start_value=0.1,  # Initial diffusion rate
            value_range=(0.01, 1.0),
            manager=self.ui_manager,
        )

        # Label for gravity slider
        self.gravity_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 70), (200, 30)),
            text=f"Gravity: {0.02}",
            manager=self.ui_manager,
        )
        self.gravity_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 90), (200, 30)),
            start_value=0.02,  # Initial gravity
            value_range=(0.001, 10.0),
            manager=self.ui_manager,
        )

        # Label for viscosity slider
        self.viscosity_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 110), (200, 30)),
            text=f"Viscosity: {0.15}",
            manager=self.ui_manager,
        )
        self.viscosity_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 130), (200, 30)),
            start_value=0.15,  # Initial viscosity
            value_range=(0.01, 1.0),
            manager=self.ui_manager,
        )

        # Label for color picker button
        self.color_picker_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((220, -10), (100, 30)),
            text="Color Picker",
            manager=self.ui_manager,
        )

        # Button to open color picker
        self.color_picker_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((220, 10), (100, 30)),
            text="Pick Color",
            manager=self.ui_manager,
        )

        # Label for current mode
        self.mode_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((220, 40), (100, 30)),
            text=f"Mode: {self.mode.name}",
            manager=self.ui_manager,
        )

    def update_labels(self):
        self.brush_size_label.set_text(
            f"Brush Size: {self.brush_size_slider.get_current_value()}"
        )
        self.diffusion_label.set_text(
            f"Diffusion Rate: {self.diffusion_slider.get_current_value()}"
        )
        self.gravity_label.set_text(
            f"Gravity: {self.gravity_slider.get_current_value()}"
        )
        self.viscosity_label.set_text(
            f"Viscosity: {self.viscosity_slider.get_current_value()}"
        )
        self.mode_label.set_text(f"Mode: {self.mode.name}")

    def open_color_picker(self):
        pygame_gui.windows.UIColourPickerDialog(
            rect=pygame.Rect((300, 100), (400, 400)),
            manager=self.ui_manager,
            window_title="Select Brush Color",
            initial_colour=pygame.Color(*[int(c * 255) for c in self.brush_color]),
        )

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

        # Render GUI elements on top
        self.ui_manager.draw_ui(self.screen)
        pygame.display.flip()

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
                        self.canvas.red[py, px] += (
                            current_color[0] * self.brush_intensity
                        )
                        self.canvas.green[py, px] += (
                            current_color[1] * self.brush_intensity
                        )
                        self.canvas.blue[py, px] += (
                            current_color[2] * self.brush_intensity
                        )
        # Ensure color channels are within [0, 1]
        self.canvas.red = np.clip(self.canvas.red, 0, 1)
        self.canvas.green = np.clip(self.canvas.green, 0, 1)
        self.canvas.blue = np.clip(self.canvas.blue, 0, 1)

    def erase_brush_stroke(self, x: int, y: int):
        """
        Erases color at the specified canvas coordinates.

        Parameters:
            x (int): X-coordinate on the canvas.
            y (int): Y-coordinate on the canvas.
        """
        for dx in range(-self.brush_size, self.brush_size + 1):
            for dy in range(-self.brush_size, self.brush_size + 1):
                if dx**2 + dy**2 <= self.brush_size**2:
                    px = x + dx
                    py = y + dy
                    if 0 <= px < self.canvas.width and 0 <= py < self.canvas.height:
                        # Erase colors
                        self.canvas.red[py, px] = 0.0
                        self.canvas.green[py, px] = 0.0
                        self.canvas.blue[py, px] = 0.0

    def add_barrier_stroke(self, x: int, y: int):
        """
        Adds barriers in a stroke-like manner at the specified canvas coordinates.

        Parameters:
            x (int): X-coordinate on the canvas.
            y (int): Y-coordinate on the canvas.
        """
        for dx in range(-self.brush_size, self.brush_size + 1):
            for dy in range(-self.brush_size, self.brush_size + 1):
                if dx**2 + dy**2 <= self.brush_size**2:
                    px = x + dx
                    py = y + dy
                    if 0 <= px < self.canvas.width and 0 <= py < self.canvas.height:
                        self.canvas.add_barrier(px, py)

    def remove_barrier_stroke(self, x: int, y: int):
        """
        Removes barriers in a stroke-like manner at the specified canvas coordinates.

        Parameters:
            x (int): X-coordinate on the canvas.
            y (int): Y-coordinate on the canvas.
        """
        for dx in range(-self.brush_size, self.brush_size + 1):
            for dy in range(-self.brush_size, self.brush_size + 1):
                if dx**2 + dy**2 <= self.brush_size**2:
                    px = x + dx
                    py = y + dy
                    if 0 <= px < self.canvas.width and 0 <= py < self.canvas.height:
                        self.canvas.remove_barrier(px, py)

    def handle_events(self):
        """
        Handles user input events.
        """
        time_delta = self.clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Handle UI events
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    self.update_labels()

                    if event.ui_element == self.brush_size_slider:
                        self.brush_size = int(event.value)
                    elif event.ui_element == self.diffusion_slider:
                        self.canvas.diffusion_rate = (
                            event.value
                        )  # Update diffusion rate
                    elif event.ui_element == self.gravity_slider:
                        self.canvas.gravity = event.value  # Update gravity
                    elif event.ui_element == self.viscosity_slider:
                        self.canvas.viscosity = event.value  # Update viscosity
                elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.color_picker_button:
                        self.open_color_picker()
                elif event.user_type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                    self.brush_color = (
                        event.colour.r / 255,
                        event.colour.g / 255,
                        event.colour.b / 255,
                    )

            # Process your brush-related events
            elif event.type == pygame.KEYDOWN:
                # Clear the canvas when 'c' key is pressed
                if event.key == pygame.K_c:
                    self.canvas.clear()
                elif event.key == pygame.K_r:
                    self.brush_color = (1.0, 0.0, 0.0)  # Red
                elif event.key == pygame.K_b:
                    self.brush_color = (0.0, 0.0, 1.0)
                elif event.key == pygame.K_g:
                    self.brush_color = (0.0, 1.0, 0.0)
                elif event.key == pygame.K_2:
                    self.mode = Mode.ERASER
                    self.update_labels()
                    print("Mode switched to Eraser.")
                elif event.key == pygame.K_3:
                    self.mode = Mode.ADD_BARRIER
                    self.update_labels()
                    print("Mode switched to Add Barrier.")
                elif event.key == pygame.K_4:
                    self.mode = Mode.REMOVE_BARRIER
                    self.update_labels()
                    print("Mode switched to Remove Barrier.")
                elif event.key == pygame.K_1:
                    self.mode = Mode.BRUSH
                    self.update_labels()
                    print("Mode switched to Brush.")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.drawing = True
                    x, y = pygame.mouse.get_pos()
                    canvas_x = int(x / self.scale)
                    canvas_y = int(y / self.scale)
                    if self.mode == Mode.BRUSH:
                        self.add_brush_stroke(canvas_x, canvas_y)
                    elif self.mode == Mode.ERASER:
                        self.erase_brush_stroke(canvas_x, canvas_y)
                    elif self.mode == Mode.ADD_BARRIER:
                        self.add_barrier_stroke(canvas_x, canvas_y)
                    elif self.mode == Mode.REMOVE_BARRIER:
                        self.remove_barrier_stroke(canvas_x, canvas_y)
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
                        interpolated_points = interpolate_points(
                            self.last_pos, (canvas_x, canvas_y), self.brush_size
                        )
                        for point in interpolated_points:
                            if self.mode == Mode.BRUSH:
                                self.add_brush_stroke(point[0], point[1])
                            elif self.mode == Mode.ERASER:
                                self.erase_brush_stroke(point[0], point[1])
                            elif self.mode == Mode.ADD_BARRIER:
                                self.add_barrier_stroke(point[0], point[1])
                            elif self.mode == Mode.REMOVE_BARRIER:
                                self.remove_barrier_stroke(point[0], point[1])
                    self.last_pos = (canvas_x, canvas_y)

            # Exit when Escape key is pressed
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

            # Let pygame_gui handle its own events
            self.ui_manager.process_events(event)

        # Update the UI manager
        self.ui_manager.update(time_delta)

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
