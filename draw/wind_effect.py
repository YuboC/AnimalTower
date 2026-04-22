import random
import pygame
from constants import WIDTH, HEIGHT

''' Wind Effect System
Simulates moving particles to visually represent wind 
Consists of: 
- WindParticle - individual streaks 
- WindEffect - manager for all particles '''

# individual wind particle 
class WindParticle:
    # represents a single wind streak particle 
    
    def __init__(self):
        # intialize particle with random properties 
        self.reset()

    def reset(self):
        # resets particle to a new random position and properties 
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(0.5, 2.0)
        self.length = random.randint(5, 12)

    def update(self, wind):
        # updates particle position based on wind and slight downward drift
        
        # horizontal movement influenced by wind strength 
        self.x += wind * self.speed * 3
        
        # slight vertical drift - adds natural motion 
        self.y += 0.2 + random.uniform(-0.05, 0.05)

        # reset particle if it goes off-screen 
        if self.x < -20 or self.x > WIDTH + 20 or self.y > HEIGHT:
            self.reset()

    def draw(self, surface, wind):
        # draws the particle as a small horizontal streak 
        
        end_x = self.x + (wind * 6)

        thickness = 2  # controls visibility of paritcle 

        pygame.draw.line(
            surface,
            (180, 180, 180),
            (int(self.x), int(self.y)),
            (int(end_x), int(self.y)),
            thickness
        )

# wind effect manager 
class WindEffect:
    # manages and renders a collection of wind particles 
    
    def __init__(self, count=40):
        # create a list of particles 
        self.particles = [WindParticle() for _ in range(count)]

    def update(self, wind):
        # updates all particles each frame
        for p in self.particles:
            p.update(wind)

    def draw(self, surface, wind):
        # draws all particles to the screen 
        for p in self.particles:
            p.draw(surface, wind)