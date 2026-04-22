import math

''' Small reusable helper utilities used across the game 

Purpose: 
- Mathematical helpers 
- Interpolation utilities 
- Logging/formatting helpers '''


# value utilities 
def clamp(value, min_value, max_value):
    ''' Restricts a value within a given range 
    
    Useful for: 
    - limiting stats 
    - clamping angles or movement '''
    return max(min_value, min(value, max_value))


# geometry utilities 
# computes Euclidean distance between two points 
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


# interpolation utilities 
def lerp(a, b, t):
    ''' Linear intepolation between a and b. 
    
    t = 0 -> returns a 
    t = 1 -> returns b 
    '''
    return a + (b - a) * t


# formatting utilities 
def format_turn(turn_number, name, action):
    ''' standardized format for game log entries '''
    return f"[T{turn_number}] {name}: {action}"