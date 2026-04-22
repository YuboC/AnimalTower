from constants import GRAVITY, WIND_FACTOR

''' Physics Module - Handles basic projectile physics simulation 

Responsibilities: 
- Apply graity and wind forces 
- Updates projectile position 
- Provides boundary check utility '''


# projectile physics update 
# updates projectile velocity and position each frame 
def update_projectile(game):
    '''Applies: 
    - Wind force (horizontal acceleration)
    - Gravity (vertical acceleration)'''
    
    p = game.projectile
    
    # validate projectle state 
    if not p or not p.alive:
        return False


    # force application 
    p.vx += game.wind * WIND_FACTOR
    p.vy += GRAVITY


    # position update 
    p.x += p.vx
    p.y += p.vy

    return True


# boundary check 
# checks if projectile has fallen below ground level 
def is_out_of_bounds(p):
    from constants import GROUND_Y
    
    return p.y > GROUND_Y