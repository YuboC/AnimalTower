import pygame
import sys

from constants import WIDTH, HEIGHT, FPS
from game.game_state import Game
from draw.renderer import Renderer

''' Animal Tower Game 

Game Overview: 
Two players take turns launching projectiles over a fence. 

Core mechanics: 
- Aim using mouse 
- Hold LEFT click to charge power, release to fire 
- RIGHT click to activate shield (reduces damage)
- HEAL button restores HP (limited use)
- R key restarts after game over '''


# main entry point
def main():
    # intializes pygame systems and runs the main game loop 
    
    # pygame initialization 
    pygame.init()
    pygame.mixer.init()

    # screen setup 
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Animal Tower Game")
    clock = pygame.time.Clock()
    
    
    # loads background music 
    import os
    music_path = os.path.join(
        os.path.dirname(__file__),
        "sounds", 
        "background_music.mp3"
    )
    
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)  # loop forever

    # game objects 
    game = Game()
    renderer = Renderer()

    # main game loop 
    while True:
        
        # handle events (keyboard, mouse, closing the window)
        for event in pygame.event.get():
            
            # quit game safely 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # forward all input to game logic 
            game.handle_event(event)


        # update game logic
        game.update()

        # rendering 
        renderer.draw(screen, game)
        pygame.display.flip()

        # limit speed to 60 frames per second
        clock.tick(FPS)


if __name__ == "__main__":
    main()
