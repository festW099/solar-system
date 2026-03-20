from ursina import *
from ursina.prefabs.editor_camera import EditorCamera
import math

app = Ursina()

window.title = "Solar System"
window.borderless = False

Sky(texture='textures/space.jpg')

sun = Entity(
    model='sphere',
    texture='textures/sun.jpg',
    scale=2.5
)

DirectionalLight(parent=sun, y=2, z=3, shadows=True)
AmbientLight(color=color.rgba(100, 100, 100, 255))

show_trails = False

class Planet(Entity):
    def __init__(self, distance, scale, speed, texture, name, color_trail=color.white, has_rings=False):
        super().__init__(
            model='sphere',
            texture=texture,
            scale=scale,
            smooth_shading=True
        )

        self.distance = distance
        self.angle = random.uniform(0, math.pi*2)
        self.speed = speed
        self.name = name
        self.has_rings = has_rings

        self.orbit_center = sun

        self.trail_points = []
        self.trail = Entity(
            model=Mesh(mode='line', vertices=[], thickness=3),
            color=color_trail,
            unlit=True
        )

        if has_rings:
            self.ring = Entity(
                parent=self,
                model='torus',
                scale=(scale*2.5, 0.05, scale*2.5),
                color=color.rgba(210, 180, 140, 180)
            )

        orbit_points = []
        for i in range(100):
            angle = (i / 100) * math.pi * 3
            x = math.cos(angle) * distance
            z = math.sin(angle) * distance
            orbit_points.append(Vec3(x, 0, z))

        self.orbit = Entity(
            model=Mesh(vertices=orbit_points, mode='line', thickness=2),
            color=color.rgba(255, 255, 255, 80),
            unlit=True
        )

    def update(self):
        self.angle += self.speed * time.dt
        x = math.cos(self.angle) * self.distance
        z = math.sin(self.angle) * self.distance
        self.position = self.orbit_center.position + Vec3(x, 0, z)

        self.rotation_y += 20 * time.dt

        if show_trails:
            self.trail_points.append(self.position)
            if len(self.trail_points) > 150:
                self.trail_points.pop(0)

            if len(self.trail_points) > 1:
                vertices = []
                colors = []
                for i, p in enumerate(self.trail_points):
                    fade = i / len(self.trail_points)
                    vertices.append(p)
                    colors.append(color.rgba(
                        self.trail.color.r,
                        self.trail.color.g,
                        self.trail.color.b,
                        int(255 * fade)
                    ))
                self.trail.model.vertices = vertices
                self.trail.model.colors = colors
                self.trail.model.generate()
        else:
            self.trail_points = []
            self.trail.model.vertices = []

mercury = Planet(4, 0.25, 0.6, 'textures/mercury.jpg', "Mercury", color.orange)
venus   = Planet(6, 0.35, 0.45, 'textures/venus.jpg', "Venus", color.yellow)
earth   = Planet(8, 0.4, 0.35, 'textures/earth.jpg', "Earth", color.azure)
mars    = Planet(10, 0.3, 0.25, 'textures/mars.jpg', "Mars", color.red)
saturn  = Planet(14, 0.7, 0.15, 'textures/saturn.jpg', "Saturn", color.rgb(210,180,140), has_rings=True)

planets = [mercury, venus, earth, mars, saturn]

moon = Entity(
    model='sphere',
    texture='textures/moon.jpg',
    scale=0.12
)
moon.angle = random.uniform(0, math.pi*2)

EditorCamera()

def update():
    for p in planets:
        p.update()

    moon.angle += 0.8 * time.dt
    moon.position = earth.position + Vec3(
        math.cos(moon.angle) * 1.2,
        0,
        math.sin(moon.angle) * 1.2
    )

app.run()