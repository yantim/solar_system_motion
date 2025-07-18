import pygame
import math
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum


class SimulationState(Enum):
    RUNNING = "running"
    PAUSED = "paused"


@dataclass
class SimulationConfig:
    """Configuration settings for the simulation."""
    WIDTH: int = 800
    HEIGHT: int = 600
    FPS: int = 60
    G: float = 6.67430e-11  # Gravitational constant (m³/kg⋅s²)
    SCALE: float = 6e-11  # Scale factor for normal view
    ZOOM_SCALE: float = 1e-9  # Scale factor for zoomed view
    DT: float = 86400  # Time step in seconds (1 day)
    TRAIL_LENGTH: int = 200
    TRAIL_COLOR: Tuple[int, int, int] = (50, 50, 50)
    BACKGROUND_COLOR: Tuple[int, int, int] = (0, 0, 0)


class CelestialBody:
    """Represents a celestial body in the simulation."""

    def __init__(self, x: float, y: float, vx: float, vy: float,
                 mass: float, radius: int, color: Tuple[int, int, int], name: str = ""):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.radius = radius
        self.color = color
        self.name = name
        self.trail: List[Tuple[int, int]] = []
        self.force_x = 0.0
        self.force_y = 0.0

    def reset_forces(self) -> None:
        """Reset accumulated forces."""
        self.force_x = 0.0
        self.force_y = 0.0

    def add_gravitational_force(self, other: 'CelestialBody', G: float) -> None:
        """Calculate and add gravitational force from another body."""
        dx = other.x - self.x
        dy = other.y - self.y
        distance_squared = dx * dx + dy * dy

        if distance_squared > 0:
            distance = math.sqrt(distance_squared)
            # F = G * m1 * m2 / r²
            force_magnitude = G * self.mass * other.mass / distance_squared

            # Normalize and apply force components
            force_x = force_magnitude * dx / distance
            force_y = force_magnitude * dy / distance

            self.force_x += force_x
            self.force_y += force_y

    def update_position(self, dt: float) -> None:
        """Update position and velocity based on accumulated forces."""
        # Calculate acceleration: a = F / m
        ax = self.force_x / self.mass
        ay = self.force_y / self.mass

        # Update velocity: v = v₀ + a * dt
        self.vx += ax * dt
        self.vy += ay * dt

        # Update position: x = x₀ + v * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def update_trail(self, config: SimulationConfig, zoomed: bool) -> None:
        """Update the trail of the body."""
        current_scale = config.ZOOM_SCALE if zoomed else config.SCALE
        screen_x = int(self.x * current_scale + config.WIDTH // 2)
        screen_y = int(self.y * current_scale + config.HEIGHT // 2)

        self.trail.append((screen_x, screen_y))

        if len(self.trail) > config.TRAIL_LENGTH:
            self.trail.pop(0)

    def clear_trail(self) -> None:
        """Clear the trail."""
        self.trail.clear()

    def draw(self, screen: pygame.Surface, config: SimulationConfig, zoomed: bool) -> None:
        """Draw the body and its trail."""
        # Draw trail
        if len(self.trail) > 1:
            pygame.draw.lines(screen, config.TRAIL_COLOR, False, self.trail, 1)

        # Draw body
        current_scale = config.ZOOM_SCALE if zoomed else config.SCALE
        screen_x = int(self.x * current_scale + config.WIDTH // 2)
        screen_y = int(self.y * current_scale + config.HEIGHT // 2)

        # Only draw if on screen (with margin)
        margin = 50
        if (-margin <= screen_x <= config.WIDTH + margin and
                -margin <= screen_y <= config.HEIGHT + margin):
            pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)


class PlanetSimulation:
    """Main simulation class."""

    def __init__(self, config: SimulationConfig = None):
        self.config = config or SimulationConfig()
        self.bodies: List[CelestialBody] = []
        self.zoomed = False
        self.state = SimulationState.RUNNING

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.config.WIDTH, self.config.HEIGHT))
        pygame.display.set_caption("Solar System Simulation")
        self.clock = pygame.time.Clock()

        # Create solar system
        self._create_solar_system()

    def _create_solar_system(self) -> None:
        """Create the solar system with realistic orbital parameters."""
        # Data: [distance_from_sun(m), orbital_velocity(m/s), mass(kg), radius(pixels), color, name]
        planet_data = [
            [0, 0, 1.989e30, 8, (255, 255, 0), "Sun"],
            [5.79e10, 47360, 3.301e23, 2, (169, 169, 169), "Mercury"],
            [1.082e11, 35020, 4.867e24, 3, (255, 165, 0), "Venus"],
            [1.496e11, 29780, 5.972e24, 4, (0, 100, 255), "Earth"],
            [2.279e11, 24077, 6.39e23, 3, (255, 100, 0), "Mars"],
            [7.786e11, 13070, 1.898e27, 6, (200, 150, 100), "Jupiter"],
            [1.432e12, 9680, 5.683e26, 5, (250, 200, 100), "Saturn"],
            [2.867e12, 6810, 8.681e25, 4, (100, 200, 255), "Uranus"],
            [4.515e12, 5430, 1.024e26, 4, (0, 0, 255), "Neptune"],
            [5.906e12, 4670, 1.309e22, 2, (150, 100, 50), "Pluto"]
        ]

        for distance, velocity, mass, radius, color, name in planet_data:
            body = CelestialBody(
                x=distance, y=0, vx=0, vy=velocity,
                mass=mass, radius=radius, color=color, name=name
            )
            self.bodies.append(body)

    def handle_events(self) -> bool:
        """Handle pygame events. Returns False if quit event is received."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    self.toggle_zoom()
                elif event.key == pygame.K_SPACE:
                    self.toggle_pause()
                elif event.key == pygame.K_r:
                    self.reset_simulation()
                elif event.key == pygame.K_c:
                    self.clear_trails()

        return True

    def toggle_zoom(self) -> None:
        """Toggle between normal and zoomed view."""
        self.zoomed = not self.zoomed
        self.clear_trails()

    def toggle_pause(self) -> None:
        """Toggle simulation pause state."""
        self.state = (SimulationState.PAUSED if self.state == SimulationState.RUNNING
                      else SimulationState.RUNNING)

    def reset_simulation(self) -> None:
        """Reset the simulation to initial state."""
        self.bodies.clear()
        self._create_solar_system()
        self.zoomed = False
        self.state = SimulationState.RUNNING

    def clear_trails(self) -> None:
        """Clear all body trails."""
        for body in self.bodies:
            body.clear_trail()

    def update_physics(self) -> None:
        """Update physics simulation."""
        if self.state == SimulationState.PAUSED:
            return

        # Reset forces for all bodies
        for body in self.bodies:
            body.reset_forces()

        # Calculate gravitational forces between all pairs
        for i, body1 in enumerate(self.bodies):
            for j, body2 in enumerate(self.bodies[i + 1:], i + 1):
                body1.add_gravitational_force(body2, self.config.G)
                body2.add_gravitational_force(body1, self.config.G)

        # Update positions and trails
        for body in self.bodies:
            body.update_position(self.config.DT)
            body.update_trail(self.config, self.zoomed)

    def draw(self) -> None:
        """Draw the simulation."""
        self.screen.fill(self.config.BACKGROUND_COLOR)

        # Draw all bodies
        for body in self.bodies:
            body.draw(self.screen, self.config, self.zoomed)

        # Draw UI information
        self._draw_ui()

        pygame.display.flip()

    def _draw_ui(self) -> None:
        """Draw UI elements."""
        font = pygame.font.Font(None, 24)

        # Status text
        status_text = f"{'PAUSED' if self.state == SimulationState.PAUSED else 'RUNNING'}"
        zoom_text = f"Zoom: {'ON' if self.zoomed else 'OFF'}"

        # Controls text
        controls = [
            "Controls:",
            "Z - Toggle Zoom",
            "SPACE - Pause/Resume",
            "R - Reset",
            "C - Clear Trails"
        ]

        y_offset = 10
        for i, text in enumerate([status_text, zoom_text, ""] + controls):
            if text:
                surface = font.render(text, True, (255, 255, 255))
                self.screen.blit(surface, (10, y_offset))
            y_offset += 25

    def run(self) -> None:
        """Main simulation loop."""
        running = True

        while running:
            running = self.handle_events()
            self.update_physics()
            self.draw()
            self.clock.tick(self.config.FPS)

        pygame.quit()


def main():
    """Main function to run the simulation."""
    simulation = PlanetSimulation()
    simulation.run()


if __name__ == "__main__":
    main()