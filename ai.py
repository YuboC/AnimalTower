from projectile import Projectile

''' AI module - Handles computer-controlled opponent logic.

AI behavior is split into phases: 
- thinking: chooses action 
- aiming: calculates trajectory preview 
- charging: builds power 
- firing: executes attack '''

# Simple turn-based AI controler as the opponent.
# Handles decision-making and timed action phases 
class AI:

    # intialization 
    def __init__(self):
        self.timer = 0
        self.state = "thinking"
        self.target_power = 14

        # stores simulated projectile trajectory for 
        # UI visualization 
        self.preview_points = []


    # reset 
    def reset(self):
        self.timer = 0
        self.state = "thinking"
        self.target_power = 14
        self.preview_points = []


    # main update loop 
    def update(self, game):
        # runs AI logic each fram during opponent turn 
        
        self.timer += 1

        # only active on AI turn 
        if game.turn != 1:
            return

        # don't act if already used action this turn (e.g. got shield)
        if game.turn_action_used:
            return

        # thinking phase (decision making)
        if self.state == "thinking":

            if self.timer == 10:

                # action scoring system 
                scores = {
                    "attack": 0,
                    "defend": 0,
                    "special": 0,
                    "heal_orb": 0,
                    "shield_orb": 0,
                }

                me = game._current()
                enemy = game._opponent()

                # simple heuristic rules 
                if enemy.hp < 25:
                    scores["attack"] += 3
                if me.hp > 50:
                    scores["attack"] += 2

                if me.hp < 40:
                    scores["defend"] += 2

                if me.special_cooldown == 0:
                    scores["special"] += 2

                # pick best action: attack or defend
                if scores["defend"] > scores["attack"] and not me.shield_used:
                    # AI chooses to defend this turn
                    from game.actions import activate_shield
                    activate_shield(game, me, source="manual")
                    self.state = "thinking"
                    self.timer = 0
                    return

                # switch to aiming phase (attack)
                self.state = "aiming"

                # trajectory simulation (for UI preview)
                ox, oy = me.aim_origin()
                
                self.preview_points = Projectile.simulate_trajectory(
                    ox, 
                    oy, 
                    game.aim_angle, 
                    14, 
                    game.wind
                )

                self.timer = 0


        # aiming phase 
        elif self.state == "aiming":

            if self.timer > 25:
                self.state = "charging"
                self.timer = 0


        # charging phase 
        elif self.state == "charging":

            game.power += 0.35
            game.power = min(game.power, self.target_power)

            if game.power >= self.target_power:
                self.state = "firing"


        # firing phase 
        elif self.state == "firing":

            game.handle_fire()
            self.state = "thinking"
            self.timer = 0