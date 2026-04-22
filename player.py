import pygame

from constants import XP_HEAL_COST

''' Player Class - Defines the characters for Animal Tower Game

Responsibilities: 
- Stores player stats( HP, attack, defense, etc.)
- Handles combat logic (damage, healing)
- Manages XP (collected from orbs, spent on healing)
- Provides UI helper methods (aim origin, button positions) '''


# player class 
# represents a single player (Cat, Wolf, Elephant, etc.)
class Player:
    
    # initialization 
    def __init__(self, name, x, y, aim_x_offset, default_aim_angle):

        # identify / position 
        self.name = name
        self.x = x
        self.y = y
        self.aim_x_offset = aim_x_offset
        self.default_aim_angle = default_aim_angle


        # base stats
        self.base_hp = 100
        self.hp = self.base_hp
        self.max_hp = self.base_hp

        self.atk = 10
        self.defense = 5
        self.special_bonus = 1.0


        # state flags 
        self.defending = False

        self.heal_used = False
        self.heal_cooldown = 0

        self.has_shield = False
        self.shield_used = False
        self.shield_block = 0

        self.special_active = False
        self.special_used = 0
        self.max_specials = 2
        self.special_cooldown = 0


        # XP system (used for healing)
        self.exp = 0


    # reset player state (new game)
    # resets all state including XP
    def reset(self):
        self.hp = self.base_hp

        self.defending = False

        self.heal_used = False
        self.heal_cooldown = 0

        self.has_shield = False
        self.shield_used = False
        self.shield_block = 0

        self.special_active = False
        self.special_used = 0
        self.special_cooldown = 0

        # reset XP on game reset
        self.exp = 0


    # stat system (character selection scaling)
    # applies character-specific stat modifiers 
    def apply_stats(self, stats):
        
        if not stats:
            return

        for key, value in stats.items():
            
            if key == "hp":
                self.base_hp += value
                self.hp += value  # keep scaling consistent

            elif key == "atk":
                self.atk += value

            elif key == "defense":
                self.defense += value

            elif key == "special_bonus":
                self.special_bonus *= value

        # prevents overhealing overflow
        self.hp = min(self.hp, self.base_hp)


    # combat
    # currently always allow attacking 
    def can_attack(self):
        return True
    
    
    # applies incoming damage, accounting for 
    # shield and defense states
    def take_damage(self, amount):
        if self.has_shield:
            self.has_shield = False
            return 0

        if self.defending:
            amount = amount // 2

        self.hp = max(0, self.hp - amount)
        return amount


    # heals the player based on missing HP 
    # costs full XP bar
    def heal(self):
        lost = self.base_hp - self.hp
        if lost <= 0:
            return 0

        heal_amount = max(1, lost // 2)
        self.hp = min(self.base_hp, self.hp + heal_amount)
        
        # spend all XP
        self.exp = 0

        return heal_amount

    # checks whether healing is allowed 
    # requires full XP bar
    def can_heal(self):
        return self.exp >= XP_HEAL_COST and self.hp < self.base_hp
    
    
    # UI helpers 
    # returns the clickable heal button region 
    def get_heal_rect(self):
        _, _, btn_x, btn_y = self.get_ui_positions()
        return pygame.Rect(btn_x, btn_y, 70, 24)
    
    def is_dead(self):
        return self.hp <= 0

    def aim_origin(self):
        return self.x + self.aim_x_offset, self.y - 15

    # returns UI anchor positions for this player 
    def get_ui_positions(self):
        label_x = self.x
        label_y = self.y + 35

        btn_x = self.x - 30
        btn_y = label_y + 25

        return label_x, label_y, btn_x, btn_y
    

    # XP system 
    # adds XP (collected from orbs), caps at heal cost
    def add_exp(self, amount):
        self.exp = min(self.exp + amount, XP_HEAL_COST)