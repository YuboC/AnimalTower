import pygame
import random
from constants import WIDTH, GROUND_Y, HIT_RADIUS

''' Shield Pickup Module - Defines the Shield Pickup 
system and shield activation logic 

Features: 
- Floating shield orb pickup 
- Wind movement and screen wrap 
- Collision detection with projectile 
- Temporary shield effect on player '''


class ShieldPickup:
    # shield orb that grants a temprary damage-reducing shield. 
    
    # initialization 
    def __init__(self):
        self.reset()

    # spawn / reset 
    def reset(self):
        # resets shield pickup to default position and state 
        self.x = random.randint(100, WIDTH - 100)
        self.y = GROUND_Y - 120
        self.radius = 15
        self.active = True


    # update logic 
    # updates shield pickup movement
    def update(self, wind):
        ''' Updates shield pickup movement. 
        - Moves with wind 
        - Wraps around screen edges ''' 
        
        if not self.active:
            return

        self.x += wind * 0.5

        # screen wrap-around 
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0


    # rendering
    # draws shield pickup with layered glow effect 
    def draw(self, surface):
        
        if not self.active:
            return

        # outer glow (light blue)
        pygame.draw.circle(
            surface,
            (180, 220, 255),
            (int(self.x), int(self.y)),
            self.radius + 4
        )

        # main body (core shield orb)
        pygame.draw.circle(
            surface,
            (80, 160, 255),
            (int(self.x), int(self.y)),
            self.radius
        )

        # outline (deep blue)
        pygame.draw.circle(
            surface,
            (40, 90, 180),
            (int(self.x), int(self.y)),
            self.radius,
            2
        )


    # collision detection 
    def collides_with(self, projectile):
        # checks collision with projectile 
        if not self.active:
            return False

        dx = projectile.x - self.x
        dy = projectile.y - self.y
        
        return dx * dx + dy * dy <= HIT_RADIUS ** 2



# shield effect logic 
# applies shield effect when shield pickup is collected
def shield_on_hit(game, player):
    ''' Grants: 
    - Temporary damage reduction 
    - Randomized block strength '''

    block_amount = random.randint(5, 15)

    player.has_shield = True
    player.shield_block = block_amount

    game._log(f"{player.name} gained shield ({block_amount})")
    game._show_message(f"Shield +{block_amount}")