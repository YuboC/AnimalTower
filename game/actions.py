import random

from constants import XP_HEAL_COST
from projectile import Projectile
from game.audio import play_sound

''' Actions Module - Handles player-triggered gameplay actions:
- Defend 
- Shield Activation 
- Healing 
- Firing projectiles '''

# defend action 
def defend(game):
    # defend action - reduces damage on next hit 
    
    player = game._current()
    
    # enables defensive state 
    player.defending = True

    # log and switch turn 
    game._log("defending")
    game._switch_turn()

# shield activation 
def activate_shield(game, player, source="manual"):
    ''' activates a shield for the player. 
    Always ends the turn - shield OR attack, never both.'''
    
    # prevents reuse 
    if player.shield_used:
        game._show_message("Shield already used!")
        return False
    
    # apply shield effects 
    player.has_shield = True
    player.shield_used = True
    player.shield_block = random.randint(5, 20)

    # log and feedback 
    game._log(f"{player.name} got shield +{player.shield_block}")
    game._show_message("Shield activated!")
    
    # shield always uses the turn
    game.turn_action_used = True
    game._switch_turn()
    
    return True


# heal action 
def try_heal(game):
    # attempts to heal the current player (requires full XP bar)
    
    player = game._current()

    # check if healing is available (need full XP)
    if not player.can_heal():
        if player.exp < XP_HEAL_COST:
            game._show_message("Need full XP to heal!")
        else:
            game._show_message("Nothing to heal!")
        return

    # perform heal (spends all XP)
    healed = player.heal()

    # nothing to heal 
    if healed <= 0:
        game._show_message("Nothing to heal!")
        return

    # log and feedback 
    game._log(f"{player.name} healed +{healed}")
    game._show_message(f"+{healed} HP!")

    # healing uses the turn
    game.turn_action_used = True
    game._switch_turn()


# fire projectile 
def fire(game):
    # fires a projectile using current aim, power, and wind 

    # prevents multiple proectiles at once 
    if game.projectile is not None:
        return
    
    player = game._current()

    # retrieves origin point for projectile 
    ox, oy = player.aim_origin()

    # create projectile 
    game.projectile = Projectile(
        ox,
        oy,
        game.aim_angle,
        game.power,
        game.wind
    )

    # log action 
    game._log(f"fired (power={game.power:.0f})")
    play_sound(game.sound_throw)

    # attacking uses the turn
    game.turn_action_used = True
    
