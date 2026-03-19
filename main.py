import pygame
import math
import datetime

pygame.init()
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Solar System")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
GRAY = (200, 200, 200)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
LIGHT_YELLOW = (255, 255, 200)

class Planet:
    def __init__(self, orbit_center, orbit_radius, radius, color, speed, name, has_rings=False):
        self.center = orbit_center
        self.orbit_radius = orbit_radius
        self.radius = radius
        self.color = color
        self.speed = speed
        self.angle = 0
        self.name = name
        self.has_rings = has_rings
        self.moons = []
        self.destroyed = False

    def update(self):
        if self.destroyed:
            return
        self.angle += self.speed

    def get_position(self):
        cx, cy = self.center
        x = cx + self.orbit_radius * math.cos(self.angle)
        y = cy + self.orbit_radius * math.sin(self.angle)
        return x, y

sun_pos = (WIDTH//2, HEIGHT//2)

mercury = Planet(sun_pos, 80, 5, GRAY, 0.04, "Mercury")
venus = Planet(sun_pos, 120, 7, ORANGE, 0.03, "Venus")
earth = Planet(sun_pos, 170, 8, BLUE, 0.025, "Earth")
mars = Planet(sun_pos, 220, 6, RED, 0.02, "Mars")
saturn = Planet(sun_pos, 320, 12, LIGHT_YELLOW, 0.015, "Saturn", has_rings=True)

moon = Planet((0,0), 20, 3, WHITE, 0.08, "Moon")
earth.moons.append(moon)

planets = [mercury, venus, earth, mars, saturn]

running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.circle(screen, YELLOW, sun_pos, 25)
    screen.blit(font.render("Sun", True, WHITE), (sun_pos[0] - 15, sun_pos[1] + 30))

    for planet in planets:
        planet.update()

    for i in range(len(planets)):
        for j in range(i+1, len(planets)):
            p1 = planets[i]
            p2 = planets[j]
            if p1.destroyed or p2.destroyed:
                continue
            x1, y1 = p1.get_position()
            x2, y2 = p2.get_position()
            dist = math.hypot(x1 - x2, y1 - y2)
            if dist < p1.radius + p2.radius:
                p1.destroyed = True
                p2.destroyed = True

    for planet in planets:
        if planet.destroyed:
            continue
        x, y = planet.get_position()

        if planet.has_rings:
            pygame.draw.ellipse(screen, GRAY, (x - planet.radius*2, y - planet.radius//2, planet.radius*4, planet.radius))

        pygame.draw.circle(screen, planet.color, (int(x), int(y)), planet.radius)

        label = font.render(planet.name, True, WHITE)
        screen.blit(label, (int(x) - label.get_width()//2, int(y) + planet.radius + 5))

        for moon in planet.moons:
            moon.center = (x, y)
            moon.update()
            mx, my = moon.get_position()
            pygame.draw.circle(screen, moon.color, (int(mx), int(my)), moon.radius)
            moon_label = font.render(moon.name, True, WHITE)
            screen.blit(moon_label, (int(mx) - moon_label.get_width()//2, int(my) + moon.radius + 3))

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    screen.blit(font.render(f"Date: {now}", True, WHITE), (10, 10))

    pygame.display.flip()

pygame.quit()