import random
from constants import *
from game.audio import play_sound
from game.heal_pickup import heal_on_hit
from game.shield_pickup import shield_on_hit

''' Combat Module - handles all projectile collison logic: 
- Fence collision 
- Pickup interactions (heal and shield)
- Player damage calculations 
- Ground impact (misses) '''

# main collision handler for active projectile
def check_collisions(game):
    ''' checks interactions in the following order: 
    1. Fence
    2. Heal pickup 
    3. Shield pickup 
    4. Opponent hit 
    5. Ground (miss) 
    
    Ends projectile lifecycle on any collision '''
    
    # get active projectile 
    p = game.projectile
    if not p:
        return

    # fence collision 
    if abs(p.x - FENCE_X) < 8 and p.y > GROUND_Y - FENCE_HEIGHT:
        p.alive = False
        game._log("hit fence")
        game._show_message("Hit fence!")
        return

    # heal pickup collision 
    if game.heal_pickup.active and game.heal_pickup.collides_with(p):
        heal_on_hit(game, game.heal_pickup)
        game.heal_pickup.active = False
        p.alive = False
        return

    # shield pickup collision (attack chosen = no shield granted, just destroys pickup)
    if game.shield_pickup.active and game.shield_pickup.collides_with(p):
        game._log("shield orb destroyed")
        game._show_message("Shield orb destroyed!")
        game.shield_pickup.active = False
        p.alive = False
        return

    # opponent hit detection 
    target = game._opponent()

    if p.check_hit(target.x, target.y, HIT_RADIUS):

        # base damage calculation (scaled by power)
        dmg = int(
            DAMAGE_MIN 
            + (game.power / MAX_POWER) * (DAMAGE_MAX - DAMAGE_MIN)
        )

        attacker = game._current()

        #spcial attack bonus
        if attacker.special_active:
            bonus = random.uniform(0.01, 0.25)
            dmg = int(dmg * (1 + bonus))

            game._log(f"{attacker.name} SPECIAL! + {int(bonus * 100)}% dmg")
            game._show_message("SPECIAL HIT!")

            # reset special after use 
            attacker.special_active = False

        # shield damage reduction (50%)
        if target.has_shield:
            dmg = max(1, int(dmg * 0.5)) 
            
            game._log(f"{target.name}'s shield reduced damage by 50%")
            game._show_message("Shield absorbed hit!")
            
            # consumes shield after blocking 
            target.has_shield = False
            target.shield_block = 0 

        # apply damage 
        actual = target.take_damage(dmg)

        game._log(f"hit -{actual}")
        game._show_message(f"Hit! -{actual} HP")
        play_sound(game.sound_hit)

        p.alive = False
        return

    # ground collision (miss)
    if p.y >= GROUND_Y:
        p.alive = False
        game._log("miss")
        game._show_message("Missed!")
        play_sound(game.sound_miss)