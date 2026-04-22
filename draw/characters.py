import pygame
from constants import BLACK


# routes which character drawing function to use based on character name
def draw_character(surface, x, y, name, font):
    
    # character selection logic 
    if name == "Cat":
        _draw_cat(surface, x, y)
    elif name == "Dog":
        _draw_dog(surface, x, y)
    elif name == "Wolf":
        _draw_wolf(surface, x, y)
    elif name == "Elephant":
        _draw_elephant(surface, x, y)
    else:
        # default fallback character
        pygame.draw.circle(surface, (200, 200, 200), (x, y), 25)

    # name label rendering
    label = font.render(name, True, BLACK)
    surface.blit(label, (x - label.get_width() // 2, y - 55))


# individual designs 
# cat design 
def _draw_cat(surface, x, y):
    body = (255, 170, 180)
    outline = (80, 40, 50)

    # body
    pygame.draw.circle(surface, body, (x, y), 22)
    pygame.draw.circle(surface, outline, (x, y), 22, 2)

    # ears
    pygame.draw.polygon(surface, body, [(x - 14, y - 14), (x - 6, y - 35), (x, y - 14)])
    pygame.draw.polygon(surface, body, [(x + 14, y - 14), (x + 6, y - 35), (x, y - 14)])

    pygame.draw.polygon(surface, outline, [(x - 14, y - 14), (x - 6, y - 35), (x, y - 14)], 2)
    pygame.draw.polygon(surface, outline, [(x + 14, y - 14), (x + 6, y - 35), (x, y - 14)], 2)

    # eyes
    pygame.draw.circle(surface, BLACK, (x - 6, y - 4), 2)
    pygame.draw.circle(surface, BLACK, (x + 6, y - 4), 2)


# dog design 
def _draw_dog(surface, x, y):
    body = (210, 180, 120)
    ear = (160, 130, 90)
    outline = (70, 60, 40)

    # head/body
    pygame.draw.circle(surface, body, (x, y), 22)
    pygame.draw.circle(surface, outline, (x, y), 22, 2)

    # floppy ears
    pygame.draw.circle(surface, ear, (x - 18, y - 5), 9)
    pygame.draw.circle(surface, ear, (x + 18, y - 5), 9)

    pygame.draw.circle(surface, outline, (x - 18, y - 5), 9, 2)
    pygame.draw.circle(surface, outline, (x + 18, y - 5), 9, 2)

    # nose
    pygame.draw.circle(surface, BLACK, (x, y + 3), 3)


# wolf design 
def _draw_wolf(surface, x, y):
    body = (120, 120, 130)
    outline = (30, 30, 40)

    # head/body
    pygame.draw.circle(surface, body, (x, y), 24)
    pygame.draw.circle(surface, outline, (x, y), 24, 2)

    # sharp ears
    pygame.draw.polygon(surface, body, [(x - 16, y - 10), (x - 8, y - 38), (x - 2, y - 10)])
    pygame.draw.polygon(surface, body, [(x + 16, y - 10), (x + 8, y - 38), (x + 2, y - 10)])

    pygame.draw.polygon(surface, outline, [(x - 16, y - 10), (x - 8, y - 38), (x - 2, y - 10)], 2)
    pygame.draw.polygon(surface, outline, [(x + 16, y - 10), (x + 8, y - 38), (x + 2, y - 10)], 2)

    # glowing eyes
    pygame.draw.circle(surface, (255, 80, 80), (x - 6, y - 4), 3)
    pygame.draw.circle(surface, (255, 80, 80), (x + 6, y - 4), 3)


# elephant design 
def _draw_elephant(surface, x, y):
    body = (170, 170, 150)
    ear = (140, 140, 120)
    outline = (60, 60, 50)

    # head/body
    pygame.draw.circle(surface, body, (x, y), 28)
    pygame.draw.circle(surface, outline, (x, y), 28, 2)

    # big ears
    pygame.draw.circle(surface, ear, (x - 22, y), 14)
    pygame.draw.circle(surface, ear, (x + 22, y), 14)

    pygame.draw.circle(surface, outline, (x - 22, y), 14, 2)
    pygame.draw.circle(surface, outline, (x + 22, y), 14, 2)

    # trunk (arcade stylized)
    pygame.draw.rect(surface, body, (x - 4, y + 10, 8, 22))
    pygame.draw.rect(surface, outline, (x - 4, y + 10, 8, 22), 2)