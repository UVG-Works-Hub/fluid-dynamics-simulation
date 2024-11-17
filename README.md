
# 2D Interactive Fluid Dynamics Simulation Based on Simplified Navier-Stokes

The simulation visualizes the real-time behavior of fluid flow and color diffusion within a two-dimensional environment. Users can interactively add colors, adjust key parameters such as diffusion rate, viscosity, and gravity, and manipulate barriers to observe their effects on the fluid dynamics. The intuitive interface allows for dynamic exploration of fluid behaviors, enabling the creation of complex patterns and the study of fundamental fluid phenomena in an engaging and interactive manner.

## Features

- **Real-Time Simulation**: Visualize fluid flow and color diffusion in a 2D environment.
- **Interactive Controls**: Adjust parameters such as diffusion rate, viscosity, and gravity on-the-fly.
- **User Manipulation**: Add or remove colors and barriers directly on the canvas using intuitive tools.
- **Color Mixing and Decay**: Experience natural blending of colors and gradual fading over time.
- **Responsive Interface**: Smooth and responsive user interface built with Pygame and pygame_gui.

## Requirements

- **Python 3.7 or higher**
- **Libraries**:
  - [NumPy](https://numpy.org/)
  - [SciPy](https://www.scipy.org/)
  - [Pygame](https://www.pygame.org/)
  - [pygame_gui](https://pygame-gui.readthedocs.io/en/latest/)

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/UVG-Works-Hub/fluid-dynamics-simulation
   cd artistic-diffusion-sim
   ```

2. **Create a Virtual Environment (Optional but Recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Simulation

2. **Run the Main Script**
   ```bash
   python main.py
   ```

   This will launch the simulation window where you can interact with the fluid dynamics model.

## Controls

- **Brush Mode**
  - **Add Colors**: Click and drag the left mouse button to paint colors on the canvas.
  - **Select Color**: Use the "Pick Color" button to choose your desired brush color.
  - **Adjust Brush Size**: Use the brush size slider to change the radius of the brush.

- **Eraser Mode**
  - **Remove Colors**: Switch to eraser mode by pressing `2` or selecting the mode from the interface. Click and drag to erase colors.

- **Add Barrier Mode**
  - **Add Barriers**: Switch to add barrier mode by pressing `3`. Click and drag to place impermeable barriers that affect fluid flow.

- **Remove Barrier Mode**
  - **Remove Barriers**: Switch to remove barrier mode by pressing `4`. Click and drag to remove existing barriers.

- **Adjust Simulation Parameters**
  - **Diffusion Rate**: Use the diffusion rate slider to control how quickly colors spread.
  - **Viscosity**: Use the viscosity slider to adjust the fluid's internal resistance.
  - **Gravity**: Use the gravity slider to modify the gravitational force affecting the fluid.

- **Other Controls**
  - **Clear Canvas**: Press `c` to clear all colors from the canvas.
  - **Reset Brush Color**: Press `r`, `g`, `b` or `t` to reset the brush color to red, green, blue or lighT blue respectively.
  - **Toggle Stochastic Noise: Press `n` to toggle stochastic noise over the canvas.
  - **Exit Simulation**: Press `Escape` or close the window to exit.

## Gallery

![noise5](https://github.com/user-attachments/assets/d06aeaa4-04c7-4c90-be8d-0bd2a4d26de7)

![asd](https://github.com/user-attachments/assets/49bad4fe-5b1d-4633-84fe-82fcd144a22a)

![fluido_gravedad_mezcla](https://github.com/user-attachments/assets/881d10d8-9e63-45a8-bf0b-3fcdb052da3b)


## Documentation

For a comprehensive understanding of the theoretical background, implementation details, and experimental results, please refer to the [Project Report](docs/Informe___CC2017_MODELACIÓN_Y_SIMULACIÓN__PROYECTO_.pdf).

## License

This project is licensed under the GPL-3.0 license. See the [LICENSE](LICENSE) file for details.
