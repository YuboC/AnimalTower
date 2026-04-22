import pygame
import random
import math
from constants import WIDTH, GROUND_Y

''' Heal Pickup Module - Features: 
- Floating healing orb with bobbing animation 
- Wind drift movement 
- Collision detection with projectil 
- Turn-based respawn system 
- Healing effect handler (heal_on_hit) '''


# healing pickup object 
class HealPickup:
    ''' Behavior: 
    - Spawns at random position 
    - Floats with sine-wave bobbing motion 
    - Moves with wind 
    - Respawns after a cooldown (turn-based) '''
    
    # intialization 
    def __init__(self):
        self.respawn_turns = 3
        self.turns_since_used = 0
        self.reset()

    # spawn / reset 
    def reset(self):
    # resets heal pickup to a new random position 
        self.x = random.randint(100, WIDTH - 100)
        
        self.base_y = random.randint(60, GROUND_Y - 120)
        self.y = self.base_y
        
        self.radius = 10
        self.active = True
        
        # phase offset for bobbing animation 
        self.bob_offset = random.uniform(0, 2 * math.pi)

    # update logic 
    # updates heal pickup position 
    def update(self, wind):
        ''' Wind affects horizontal movement. 
        Sine wave creates floating/bobbing motion '''
        
        if not self.active:
            return

        # wind drift 
        self.x += wind * 0.5

        # bobbien animation (smooth vertical motion)
        t = pygame.time.get_ticks() * 0.005
        self.y = self.base_y + math.sin(t + self.bob_offset) * 5

        # screen wrap-around 
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0


    # rendering 
    # draws heal pickup with glow and layered styling 
    def draw(self, surface):
        
        if not self.active:
            return

        # outer glow (lighter green aura)
        pygame.draw.circle(
            surface,
            (120, 220, 140),
            (int(self.x), int(self.y)),
            self.radius + 4
        )

        # main body (core pickup)
        pygame.draw.circle(
            surface,
            (70, 170, 90),
            (int(self.x), int(self.y)),
            self.radius
        )

        # outline (darker green)
        pygame.draw.circle(
            surface,
            (40, 120, 60),
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
        
        return dx * dx + dy * dy <= self.radius ** 2


    # turn-based respawn system 
    # handles respawn timing after pickup is used 
    def on_turn_passed(self):
        if self.active:
            return

        self.turns_since_used += 1
        
        if self.turns_since_used >= self.respawn_turns:
            self.turns_since_used = 0
            self.reset()


# heal effect logic 
# applies healing effect when projectile hits pickup 
def heal_on_hit(game, pickup):
    """Called when heal pickup is hit by a projectile.
    Heals the current player without costing XP."""

    player = game._current()

    # direct heal (doesn't spend XP - it's a pickup reward)
    lost = player.base_hp - player.hp
    if lost <= 0:
        game._log("heal orb wasted (full HP)")
        game._show_message("Already full HP!")
    else:
        heal_amount = max(1, lost // 2)
        player.hp = min(player.base_hp, player.hp + heal_amount)

        game._log(f"{player.name} healed +{heal_amount}")
        game._show_message(f"+{heal_amount} HP!")

    if hasattr(pickup, "reset"):
        pickup.reset()