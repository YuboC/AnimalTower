import pygame
import random
from constants import WIDTH, HEIGHT

''' Experience Orb Module - Defines the ExpOrb object
Features:
- Random spawn position 
- Wind-based drifting 
- Optional attraction toward players 
- Collection and pop-up feedback 
- Collision detection with players and projectiles 
'''

# Floating XP orb that players can collect 
class ExpOrb:
    '''Behavior: 
    - Spawns at random position 
    - Moves with wind influence 
    - Can be attracted to nearby players 
    - Disappears when collected '''

    def __init__(self):
        # initializes orb state 
        self.reset()
        self.active = True

    # spawn and reset logic 
    def reset(self):
        # resets orb to a new random position and value 
        self.active = True
        
        # random spawn position 
        self.x = random.choice([100, 300, 500, 700, 900])
        self.y = random.randint(120, HEIGHT - 180)
        
        # XP value determines size 
        self.value = random.randint(10, 50)
        self.radius = 6 + self.value // 10
        
        # popup feedback timer 
        self.pop_timer = 0
        self.pop_text = ""


    # collection logic 
    def collect(self):
        # marks orb as collected and triggers popup timer 
        self.active = False
        self.pop_timer = 60


    # update logic 
    # updates orb movement
    def update(self, wind):
        
        ''' Active orb: moves with wind 
        Inactive orb: counts down popup timer '''
        
        if not self.active:
            self.pop_timer -= 1
            return

        # wind-based horizontal drift
        self.x += wind * (0.3 + self.radius * 0.05)

        # screen wrap-around behavior 
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
            
    
    # player attraction system 
    def attract(self, player):
        # slowly pulls orb toward player if within range 
        
        dx = player.x - self.x
        dy = player.y - self.y
        
        dist = max(1, (dx*dx + dy*dy) ** 0.5)

        # attraction radius check 
        if dist < 120:  
            self.x += dx / dist * 1.5
            self.y += dy / dist * 1.5
            

    # rendering 
    def draw(self, surface):
        # draws orb or popup text depending on state 
        
        # active orb rendering 
        if self.active:
            pygame.draw.circle(surface, (255, 230, 100), (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(surface, (255, 215, 0), (int(self.x), int(self.y)), self.radius, 2)
            return

        # popup text after collection 
        if self.pop_timer > 0:
            font = pygame.font.SysFont("Courier New", 16, bold=True)
            text = font.render(self.pop_text, True, (0, 200, 255))
            surface.blit(text, (self.x, self.y - 20))


    # colision detection (player) 
    def collides_with(self, player):
        # checks collision between orb and player 
        if not self.active:
            return False

        dx = self.x - player.x
        dy = self.y - player.y

        return (dx * dx + dy * dy) ** 0.5 < self.radius + 20


    # collision detected (projectile)
    def collides_with_projectile(self, projectile):
        # checks collision between orb and projectile 
        if not self.active or not projectile:
            return False

        dx = self.x - projectile.x
        dy = self.y - projectile.y

        return (dx * dx + dy * dy) ** 0.5 < self.radius + 8