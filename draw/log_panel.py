import pygame
from constants import (DARK_GRAY, BLACK, LOG_LINE_H)

''' Log Panel Module - Handles the following: 
- Text wrapping for log entries 
- Rending the history/log UI panel '''

# text wrapping utility 
def wrap_text(text, font, max_width):
    
    ''' splits a string into multiple lines so that each line 
    fits within the given max_width when rendered.'''
    
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        
        # tests adding next wrod to current line 
        test_line = current_line + (" " if current_line else "") + word

        # if it fits, keep building the line 
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            # push current line and start new one 
            if current_line:
                lines.append(current_line)
            current_line = word

    # adds final line if exists 
    if current_line:
        lines.append(current_line)

    return lines


# history / log panel rendering 
def draw_history_log(surface, game, renderer, x, y, w, h):
    # draws the scrolling history/log panel 
    # displays recent game events with automatic text wrapping 

    # panel position and size 
    px, py, pw, ph = x, y, w, h

    # background (semi-transparent)
    panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
    panel.fill((220, 220, 220, 180))
    surface.blit(panel, (px, py))

    # border
    pygame.draw.rect(surface, DARK_GRAY, (px, py, pw, ph), 2)

    # title
    title = renderer.font_small.render("-- LOG --", True, BLACK)
    surface.blit(title, (px + pw // 2 - title.get_width() // 2, py + 4))

    # layout calculations 
    visible_start = py + 24     # where text starts vertically 
    max_width = pw - 12         # horizontal padding 
    line_height = LOG_LINE_H
    max_lines = (ph - 30) // line_height    # number of visible lines 

    # Wrap entries
    wrapped_lines = []
    for entry in game.history:
        wrapped_lines.extend(
            wrap_text(entry, renderer.font_log, max_width)
        )

    # only shows the most recent lines 
    visible_lines = wrapped_lines[-max_lines:]

    # renders visible lines 
    for i, line in enumerate(visible_lines):
        y = visible_start + i * line_height
        txt = renderer.font_log.render(line, True, DARK_GRAY)
        surface.blit(txt, (px + 6, y))