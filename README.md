# solar_system_motion
# Solar System Simulation

A realistic solar system simulation built with Python and Pygame, featuring accurate orbital mechanics and gravitational physics.

## Features

- **Realistic Physics**: Implements Newton's law of universal gravitation with accurate planetary masses and orbital velocities
- **Interactive Controls**: Zoom, pause, reset, and trail management
- **Visual Trails**: See the orbital paths of planets over time
- **All Planets**: Includes all planets from Mercury to Pluto (plus the Sun)
- **Optimized Performance**: Efficient force calculations and rendering

## Screenshots

The simulation shows planets orbiting the Sun with realistic relative sizes, distances, and orbital velocities. Each planet leaves a trail showing its orbital path.

## Requirements

- Python 3.7+
- Pygame 2.0+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yantim/solar-system-simulation.git
cd solar-system-simulation
```

2. Install dependencies:
```bash
pip install pygame
```

3. Run the simulation:
```bash
python planet_simulation.py
```

## Controls

| Key | Action |
|-----|--------|
| `Z` | Toggle zoom (switch between solar system view and inner planet view) |
| `SPACE` | Pause/Resume simulation |
| `R` | Reset simulation to initial state |
| `C` | Clear all planet trails |
| `ESC` | Exit simulation |

## Physics Model

The simulation uses Newton's law of universal gravitation:

```
F = G × (m₁ × m₂) / r²
```

Where:
- `F` is the gravitational force
- `G` is the gravitational constant (6.67430 × 10⁻¹¹ m³/kg⋅s²)
- `m₁` and `m₂` are the masses of the two objects
- `r` is the distance between the centers of the objects

### Planetary Data

The simulation includes realistic:
- **Orbital distances** (semi-major axes)
- **Orbital velocities** (average speeds)
- **Planetary masses** (actual values in kg)
- **Relative sizes** (scaled for visibility)

## Code Structure

```
├── planet_simulation.py          # Main simulation file
├── README.md                     # This file
└── requirements.txt              # Python dependencies
```

### Key Classes

- **`SimulationConfig`**: Configuration settings and constants
- **`CelestialBody`**: Represents a planet or star with physics properties
- **`PlanetSimulation`**: Main simulation engine and game loop
- **`SimulationState`**: Enum for simulation states (running/paused)

## Customization

### Adding New Bodies

To add a new celestial body, modify the `planet_data` list in `_create_solar_system()`:

```python
# [distance_from_sun(m), orbital_velocity(m/s), mass(kg), radius(pixels), color, name]
[distance, velocity, mass, radius, (r, g, b), "Name"]
```

### Adjusting Simulation Parameters

Modify the `SimulationConfig` class to change:
- **Time step** (`DT`): How fast time progresses
- **Scale factors** (`SCALE`, `ZOOM_SCALE`): Zoom levels
- **Trail length** (`TRAIL_LENGTH`): How long orbital trails persist
- **Frame rate** (`FPS`): Simulation smoothness

### Color Schemes

Planet colors are defined in the `planet_data` list. Colors are RGB tuples:
- Sun: `(255, 255, 0)` - Yellow
- Earth: `(0, 100, 255)` - Blue
- Mars: `(255, 100, 0)` - Red
- Jupiter: `(200, 150, 100)` - Brown

## Performance Notes

- The simulation runs at 60 FPS by default
- Each frame calculates gravitational forces between all planet pairs
- Time step is set to 1 day (86400 seconds) for realistic orbital periods
- Trails are limited to 200 points to maintain performance

## Educational Value

This simulation demonstrates:
- **Orbital mechanics** and Kepler's laws
- **Gravitational physics** and Newton's laws
- **Numerical integration** methods
- **Real-time simulation** techniques
- **Object-oriented programming** in Python

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## Acknowledgments

- Planetary data sourced from NASA
- Physics equations based on Newton's law of universal gravitation
- Built with Python and Pygame

## Future Enhancements

- [ ] Add moons for planets
- [ ] Implement elliptical orbits
- [ ] Add asteroid belt
- [ ] Include comet trajectories
- [ ] Add gravitational slingshot effects
- [ ] Implement time acceleration controls
- [ ] Add planet information display
- [ ] Include sound effects
- [ ] Add save/load simulation states
