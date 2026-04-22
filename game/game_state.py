import math
import random
import pygame

# constants & core imports 
from constants import *
from player import Player
from ai import AI

# game system modules 
from game.audio import load_sound, play_sound
from game.combat import check_collisions
from game.physics import update_projectile
from game.input import update_aim
from game.actions import defend, try_heal, fire
from game.heal_pickup import HealPickup
from game.shield_pickup import ShieldPickup
from game.exp_orb import ExpOrb


# main game controller 
class Game:
    '''Handles the following: 
    - Game states (Title, Playing, Select, Game_Over)
    - Turn-based gameplay 
    - Input routing 
    - Entitiy updates '''

    # game states 
    TITLE = 0
    PLAYING = 1
    GAME_OVER = 2
    SELECT = 3
    SELECT_P2 = 4


    # intialization 
    def __init__(self):
        
        # player objects 
        self.player1 = None
        self.player2 = None
        
        # pickups 
        self.heal_pickup = HealPickup()
        self.shield_pickup = ShieldPickup()

        # AI system 
        self.ai = AI()

        # audio 
        self.sound_throw = load_sound("throw.wav")
        self.sound_hit = load_sound("hit.wav")
        self.sound_miss = load_sound("miss.wav")
        self.sound_win = load_sound("win.wav")

        # game state dlags 
        self.state = Game.TITLE
        self.two_player = False
        
        # XP system objects 
        self.exp_orbs = []

        # special UI placeholders 
        self.special_rect = None
        self.heal_rect = None
        
        # intialize game 
        self.reset()
        
        
    # reset game state 
    # resets all runtime game variables 
    def reset(self):
        
        self.ai.reset()

        # turn system 
        self.turn = 0
        self.turn_number = 1

        # combat state 
        self.charging = False
        self.power = 0
        self.projectile = None
        self.turn_action_used = False

        # environment 
        self.wind = random.uniform(-1.5, 1.5)
        self.aim_angle = -math.pi / 4   

        # UI feedback 
        self.message = ""
        self.message_timer = 0
        self.winner = None
        self.history = []
             

        # reset pickups
        self.heal_pickup.reset()
        self.shield_pickup.reset()
        
        # spawn XP orbs 
        self.exp_orbs = [ExpOrb() for _ in range(15)]  # adjust count freely

        # reset player safely 
        for p in [self.player1, self.player2]:
            if p:
                p.reset()          # resets HP
                p.hp = p.base_hp   # guarantees full heal
                p.defending = False
                p.special_active = False
                p.special_cooldown = 0
                p.has_shield = False
                p.shield_used = False
                p.shield_block = 0
            
            
    # internal helpers 
    # retuns current player based on turn 
    def _current(self):
        return self.player1 if self.turn == 0 else self.player2

    # returns opponent player 
    def _opponent(self):
        return self.player2 if self.turn == 0 else self.player1

    # displays temporary UI message 
    def _show_message(self, text):
        self.message = text
        self.message_timer = 90

    # adds entry to turn history log 
    def _log(self, text):
        who = self._current().name
        self.history.append(f"[T{self.turn_number}] {who}: {text}")


    # turn management 
    # switches active player and resets turn-based system 
    def _switch_turn(self):
        
        self.turn = 1 - self.turn
        self.turn_number += 1

        # reset turn mechanices 
        self.wind = random.uniform(-1.5, 1.5)
        self.charging = False
        self.power = 0
        self.projectile = None
        self.turn_action_used = False

        # reset per-turn abilities 
        self._current().defending = False
        self._current().heal_used = False
        
        self.ai.reset()
        self.aim_angle = self._current().default_aim_angle

        # log turn start 
        self._log(f"turn start (wind={self.wind:.1f})")
        
        # pickup logic 
        self.heal_pickup.on_turn_passed()
        
        # cooldowns 
        for p in (self.player1, self.player2):
            if hasattr(p, "special_cooldown") and p.special_cooldown > 0:
                p.special_cooldown -= 1
            p.heal_used = False


    # main game loop update 
    def update(self):

        # only update during gameplay 
        if self.state != Game.PLAYING:
            return

        # pickup updates 
        self.heal_pickup.update(self.wind)
        self.shield_pickup.update(self.wind)
        
        # XP orb system 
        for orb in self.exp_orbs:
            orb.update(self.wind)

            if self.player1:
                orb.attract(self.player1)
            if self.player2:
                orb.attract(self.player2)

            # XP collection via projectile 
            if self.projectile and self.projectile.alive and orb.collides_with_projectile(self.projectile):

                player = self._current()
                player.add_exp(orb.value)

                self._log(f"+{orb.value} XP")

                orb.pop_text = f"+{orb.value} XP"
                orb.pop_timer = 60

                orb.reset()

        # message timer 
        if self.message_timer > 0:
            self.message_timer -= 1

        # AI turn update 
        if not self.two_player and self.turn == 1:
            self.ai.update(self)

        # input / aim / charge 
        is_human = (self.turn == 0) or self.two_player

        if is_human and self.charging:
            self.power = min(self.power + 0.3, MAX_POWER)

        if is_human:
            update_aim(self)

        # projectile update 
        if self.projectile and self.projectile.alive:
            update_projectile(self)
            check_collisions(self)
            
        # XP collection (second pass)
        for orb in self.exp_orbs:
            if orb.collides_with_projectile(self.projectile):

                player = self._current()
                player.add_exp(orb.value)

                self._log(f"+{orb.value} XP")

                # visual feedback
                orb.pop_text = f"+{orb.value} XP"
                orb.pop_timer = 45

                # only remove orb
                orb.collect()

        # turn end check 
        if self.projectile and not self.projectile.alive:
            self.check_winner()

            if self.state != Game.GAME_OVER:
                self._switch_turn()
           
    # wind condition  
    def check_winner(self):
        p1_dead = self.player1.is_dead()
        p2_dead = self.player2.is_dead()

        # handle tie case first 
        if p1_dead and p2_dead:
            self.state = Game.GAME_OVER
            self.winner = "Draw"
            play_sound(self.sound_win)
            return

        if p1_dead:
            self.state = Game.GAME_OVER
            self.winner = self.player2.name
            play_sound(self.sound_win)
            return

        if p2_dead:
            self.state = Game.GAME_OVER
            self.winner = self.player1.name
            play_sound(self.sound_win)
            return       


    # action wrappers 
    def handle_defend(self):
        defend(self)

    def handle_heal(self):
        try_heal(self)

    def handle_fire(self):
        fire(self)
        
        
    # input handler 
    def handle_event(self, event):


        # title screen 
        if self.state == Game.TITLE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.two_player = False
                    self.state = Game.SELECT

                elif event.key == pygame.K_2:
                    self.two_player = True
                    self.state = Game.SELECT
            return


        # character select (Player 1)
        if self.state == Game.SELECT:

            if event.type == pygame.KEYDOWN:

                choices = ["Cat", "Dog", "Wolf", "Elephant"]

                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    index = event.key - pygame.K_1
                    name = choices[index]
                    stats = CHARACTERS[name]

                    # PLAYER 1 (always human)
                    self.player1 = Player(
                        name = name,
                        x = PLAYER1_X,
                        y = PLAYER1_Y,
                        aim_x_offset= 15,
                        default_aim_angle =- math.pi / 4
                        )
                    self.player1.apply_stats(stats)

                    if self.two_player:
                        # 2-player: let player 2 pick next
                        self.state = Game.SELECT_P2
                    else:
                        # 1-player: AI gets random character
                        enemy_name = random.choice(choices)
                        enemy_stats = CHARACTERS[enemy_name]

                        self.player2 = Player(
                            name = enemy_name,
                            x = PLAYER2_X,
                            y = PLAYER2_Y,
                            aim_x_offset =- 15,
                            default_aim_angle =- 3 * math.pi / 4
                            )
                        self.player2.apply_stats(enemy_stats)

                        self.reset()
                        self.state = Game.PLAYING

            return


        # character select (Player 2 - 2 player mode only)
        if self.state == Game.SELECT_P2:

            if event.type == pygame.KEYDOWN:

                choices = ["Cat", "Dog", "Wolf", "Elephant"]

                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    index = event.key - pygame.K_1
                    name = choices[index]
                    stats = CHARACTERS[name]

                    # PLAYER 2 (human)
                    self.player2 = Player(
                        name = name,
                        x = PLAYER2_X,
                        y = PLAYER2_Y,
                        aim_x_offset =- 15,
                        default_aim_angle =- 3 * math.pi / 4
                        )
                    self.player2.apply_stats(stats)

                    self.reset()
                    self.state = Game.PLAYING

            return


        # game over screen 
        if self.state == Game.GAME_OVER:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    self.reset()
                    self.state = Game.TITLE

                elif event.key == pygame.K_1:
                    self.two_player = False
                    self.reset()
                    self.state = Game.PLAYING

                elif event.key == pygame.K_2:
                    self.two_player = True
                    self.state = Game.SELECT

            return


        # playing input only 
        if self.state != Game.PLAYING:
            return

        # only human turns
        is_human = (self.turn == 0) or self.two_player
        if not is_human:
            return

        # don't allow input while projectile is flying
        if self.projectile and self.projectile.alive:
            return

        # block input if player already used their action this turn
        if self.turn_action_used:
            return

        player = self._current()
            
        
        # mouse input
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            player = self._current()

            if event.button == 1:

                # special button (modifier for next attack, doesn't use turn)
                if self.special_rect and self.special_rect.collidepoint(mx, my):
                    if player.special_used >= player.max_specials:
                        self._show_message("No specials left!")
                        return

                    if player.special_cooldown == 0 and not player.special_active:
                        player.special_active = True
                        player.special_cooldown = 2
                        player.special_used += 1

                        self._log(f"{player.name} used SPECIAL ({player.special_used}/2)")
                        self._show_message("Special Attack Ready!")
                    else:
                        self._show_message("Special on cooldown!")
                    return

                # heal button (uses the turn)
                if self.heal_rect and self.heal_rect.collidepoint(mx, my):
                        try_heal(self)
                        return

                # shield button (uses the turn)
                if self.shield_rect and self.shield_rect.collidepoint(mx, my):
                    from game.actions import activate_shield
                    activate_shield(self, player, source="manual")
                    return

                # attack (uses the turn)
                if not player.can_attack():
                    self._show_message("No attacks left!")
                    return

                self.charging = True
                self.power = 0


            # right click shield (uses the turn)
            elif event.button == 3:
                from game.actions import activate_shield
                activate_shield(self, player, source="manual")
                return

        # fire projectile
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.charging:
                self.charging = False
                fire(self)
                
    
    # damage calculation 
    def get_damage_estimate(self, player=None):
        # returns predicted damaged based on current charge 
        
        base = int(
            DAMAGE_MIN +
            (self.power / MAX_POWER) * (DAMAGE_MAX - DAMAGE_MIN)
        )

        # default: current player if none passed
        if player is None:
            player = self._current()

        if player.special_active:
            base = int(base * 1.25)

        return base