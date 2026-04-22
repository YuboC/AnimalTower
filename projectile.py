import math
import pygame

from constants import (
    WIDTH, HEIGHT, BLACK, GRAY,
    GRAVITY, VELOCITY_SCALE, WIND_FACTOR,
)

''' Projectile System Module - Defines the Projectile class, 
which represents a thrown object that moves through the air 
using basic 2d physics. 

Key behaviors: 
- Moves using intitial velocity derived from angle and pwoer 
- Affected by gravity (pulls downward)
- Can detect hits and go out of bounds 
- Includes helper functions for AI prediction and trajectory simulation  '''


# represents a projectile (thrown object)
class Projectile:
    ''' The projectile foollows a parabolic arc influenced by: 
    - intial launch angle and power 
    - gravity 
    - wind '''

    # intialie a new projectile 
    ''' Args:
    - x (float): Starting x-position 
    - y (float): Starting y-position 
    - angle (float): Launch angle in radians
    - power (float): Launch power (controls speed)
    - wind (floar): Current wind value affection motion '''
    def __init__(self, x, y, angle, power, wind):
       
        # stores starting position 
        self.x = float(x)
        self.y = float(y)

        # convert angle and power into velocity component 
        self.vx = math.cos(angle) * power * VELOCITY_SCALE
        self.vy = math.sin(angle) * power * VELOCITY_SCALE

        # environmental effects 
        self.wind = wind
        
        # activate state (False = projectile is removed from game)
        self.alive = True


    # game loop update 
    # updates projectile position using physics 
    def update(self):
        ''' Applies: 
        - Wind acceleration (horizontal)
        - Gravity acceleration (vertical)
        - Position update 
        - Boundary check (removes projectile if out of bounds) '''
        
        if not self.alive:
            return

        # apply wind force 
        self.vx += self.wind * WIND_FACTOR
        
        # apply gravity 
        self.vy += GRAVITY

        # update position 
        self.x += self.vx
        self.y += self.vy

        # remove projectile if it leaves the playable area
        if self.x < -50 or self.x > WIDTH + 50 or self.y > HEIGHT + 50:
            self.alive = False


    # rendering 
    # draws the projectile on screen 
    # args: surface - pygame surface to draw on 
    def draw(self, surface):
        
        if self.alive:
            pygame.draw.circle(
                surface, 
                BLACK, 
                (int(self.x), int(self.y)), 
                5
            )

    # collision detection 
    # checks if projectile hits a target 
    ''' args: 
    - target_x(float): Target X position 
    - target_y(float): Target Y position 
    - radius (float): Hit detection radius '''
    def check_hit(self, target_x, target_y, radius):
        
        dx = self.x - target_x
        dy = self.y - target_y
        
        distance = math.sqrt(dx * dx + dy * dy)
        
        # returns a bool: True is hit deteceted, otherwise False 
        return distance < radius


    # static helpers (used by trajectory preview and AI)
    @staticmethod
    def simulate_trajectory(ox, oy, angle, power, wind, steps=200):
        """Simulate a throw and return a list of (x, y) positions.

        This uses the same physics as update(), but without actually
        creating a Projectile. Used for the dotted preview line and
        for the AI to figure out where a throw would land.
        """
        vx = math.cos(angle) * power * VELOCITY_SCALE
        vy = math.sin(angle) * power * VELOCITY_SCALE
        px, py = float(ox), float(oy)
        points = []
        for _ in range(steps):
            vx += wind * WIND_FACTOR
            vy += GRAVITY
            px += vx
            py += vy
            points.append((px, py))
            if py > HEIGHT + 50 or px < -50 or px > WIDTH + 50:
                break
        return points

    @staticmethod
    def solve_launch_angle(ox, oy, tx, ty, power, wind):
        """Find the best angle to hit target (tx, ty) at given power.

        Tries many angles and picks the one whose simulated path
        passes closest to the target. Returns (best_angle, distance).
        """
        best_angle = -math.pi * 3 / 4  # default: aim up-left
        best_dist = float("inf")

        # search angles that aim left-and-up (for the dog)
        for i in range(60):
            angle = -math.pi + 0.05 + (-math.pi / 2 + 0.3 - (-math.pi + 0.05)) * i / 59
            points = Projectile.simulate_trajectory(ox, oy, angle, power, wind, 300)
            for px, py in points:
                d = math.sqrt((px - tx) ** 2 + (py - ty) ** 2)
                if d < best_dist:
                    best_dist = d
                    best_angle = angle
        return best_angle, best_dist
