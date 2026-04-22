# Explanation of Animal Tower Game 


https://github.khoury.northeastern.edu/user-attachments/assets/27fdd960-6568-4b24-9996-f97306301698

This project is a turn-based projectile game built using Python and Pygame. The game is structured around a central `Game` class that manages all core systems, including turn logic, physics updates, input handling, and game state transitions. The program is designed using a modular architecture where systems like physics, rendering, combat, and AI are separated into different files for clarity and maintainability.

## Launch
```
python main.py
```

## Game Loop
Every game follows the same pattern, called the **game loop**. It runs 60
times per second (60 FPS):

```
┌─────────────────────────────────────────────┐
│              GAME LOOP (every frame)        │
│                                             │
│   1. Handle Events  ←── keyboard, mouse     │
│   2. Update Logic   ←── physics, AI, rules  │
│   3. Draw Screen    ←── render everything   │
│   4. Flip Display   ←── show to the player  │
│   5. Tick Clock     ←── wait for next frame │
│                                             │
└─────────────────────────────────────────────┘
```
The main game loop runs continuously in `main.py`. It handles three key steps each frame: event processing, game state updates, and rendering. First, Pygame events are collected and passed into the game’s `handle_event()` function, which processes mouse and keyboard inputs. Next, the `update()` function is called on the `Game` object to handle all gameplay logic such as projectile movement, collision detection, AI decisions, and XP collection. Finally, the `Renderer` class draws the entire game state onto the screen before the display is updated using `pygame.display.flip()`. The loop is capped at a fixed FPS to ensure consistent timing.

## Turn Handling System
```
Player's Turn
     │
     ├── Option A: ATTACK  (left-click to charge, release to fire)
     │       │
     │       ├── MOUSEBUTTONDOWN → self.charging = True, self.power = 0
     │       │
     │       ├── Every frame while charging:
     │       │       self.power += 0.3
     │       │       if self.power > MAX_POWER: self.power = MAX_POWER
     │       │       (power bar + trajectory preview drawn by Renderer)
     │       │
     │       ├── MOUSEBUTTONUP → self.charging = False
     │       │       _fire() is called:
     │       │           player.attacks_left -= 1
     │       │           Projectile created at aim_origin()
     │       │           with current angle, power, wind
     │       │
     │       ├── Projectile flies (physics each frame):
     │       │       vx += wind * WIND_FACTOR
     │       │       vy += GRAVITY
     │       │       x += vx, y += vy
     │       │
     │       ├── _check_collisions() runs each frame:
     │       │       ├── |x - FENCE_X| < 8?      → "Hit the fence!"
     │       │       ├── y >= GROUND_Y?            → "Missed!"
     │       │       └── distance to opponent < 30? → "Hit! -N HP"
     │       │
     │       └── Projectile dies → check win, then _switch_turn()
     │
     ├── Option B: DEFEND
     │       ├── player.defending = True
     │       ├── _show_message("Cat is defending!")
     │       ├── _log("defending")
     │       └── _switch_turn()
     │           (bubble shows until this player's NEXT turn starts)
     │
     └── Option C: HEAL  (click HEAL button)
             ├── Check: heal_used? → "Heal already used!", return
             ├── Check: hp >= MAX_HP? → "Already full HP!", return
             ├── amount = player.heal()
             ├── _show_message("Cat healed +30 HP!")
             ├── _log("healed +30")
             └── _switch_turn()
```

The game uses a strict turn-based system controlled by the `turn` variable inside the `Game` class. Each player takes alternating turns, and the `_switch_turn()` method resets key variables such as wind, projectile state, and charging power. It also clears temporary effects like defending status and updates cooldown-based abilities.

During a player’s turn, input is enabled only for the active player. When a projectile is fired and becomes inactive (either by hitting a target or leaving the screen), the game checks for a winner before switching turns. This ensures that all actions are fully resolved before control passes to the next player.

## GUI and Rendering System

The graphical interface is handled by the `Renderer` class, which is responsible for drawing all visual elements each frame. This includes the background, characters, projectiles, health bars, XP bars, UI buttons, and trajectory previews. The renderer also displays contextual information such as turn history logs and damage estimates.

UI components are drawn using helper functions from the `draw` module, which keeps rendering logic modular. Interactive elements like heal, shield, and special ability buttons return clickable rectangles that are stored in the `Game` class for input detection.

The rendering system also visualizes physics-based elements such as wind effects and projectile trajectories, helping the player understand aiming mechanics in real time.

Overall, the architecture separates logic, physics, input, and rendering into distinct layers, making the game easier to debug, extend, and maintain.
