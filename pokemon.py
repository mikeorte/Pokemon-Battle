import time
import numpy as np
import sys
import tkinter as tk
from tkinter import ttk
from enum import Enum
from typing import List, Dict

# Constants
HEALTH_BAR_LENGTH = 20
TYPE_ADVANTAGE_MULTIPLIER = 1.5  # Slightly reduced multiplier for balancing
TYPE_DISADVANTAGE_MULTIPLIER = 0.75  # Slightly reduced multiplier for balancing
PRINT_DELAY = 0.05
TYPE_NEUTRAL = 1

def delay_print(s: str) -> None:
    """Print one character at a time with a delay."""
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(PRINT_DELAY)

class PokemonType(Enum):
    FIRE = "Fire"
    WATER = "Water"
    GRASS = "Grass"
    ELECTRIC = "Electric"
    ICE = "Ice"
    DRAGON = "Dragon"
    PSYCHIC = "Psychic"
    NEUTRAL = "Neutral"

class MoveType(Enum):
    FIRE = "Fire"
    WATER = "Water"
    GRASS = "Grass"
    ELECTRIC = "Electric"
    ICE = "Ice"
    DRAGON = "Dragon"
    PSYCHIC = "Psychic"

class Move:
    def __init__(self, name: str, power: int, m_type: MoveType):
        self.name = name
        self.power = power
        self.m_type = m_type

class Pokemon:
    def __init__(self, name: str, p_type: PokemonType, moves: List[Move], EVs: Dict[str, int]):
        self.name = name
        self.p_type = p_type
        self.moves = moves
        self.attack = EVs["ATTACK"]
        self.defense = EVs["DEFENSE"]
        self.max_bars = HEALTH_BAR_LENGTH
        self.bars = HEALTH_BAR_LENGTH

    def health_percentage(self):
        return int((self.bars / self.max_bars) * 100)

class Battle:
    def __init__(self, pokemon1: Pokemon, pokemon2: Pokemon):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.create_gui()

    def type_advantage(self):
        return {
            MoveType.FIRE: {PokemonType.FIRE: TYPE_NEUTRAL, PokemonType.WATER: TYPE_DISADVANTAGE_MULTIPLIER, PokemonType.GRASS: TYPE_ADVANTAGE_MULTIPLIER, PokemonType.ELECTRIC: TYPE_NEUTRAL, PokemonType.ICE: TYPE_ADVANTAGE_MULTIPLIER, PokemonType.DRAGON: TYPE_NEUTRAL, PokemonType.PSYCHIC: TYPE_NEUTRAL, PokemonType.NEUTRAL: TYPE_NEUTRAL},
            MoveType.WATER: {PokemonType.FIRE: TYPE_ADVANTAGE_MULTIPLIER, PokemonType.WATER: TYPE_NEUTRAL, PokemonType.GRASS: TYPE_DISADVANTAGE_MULTIPLIER, PokemonType.ELECTRIC: TYPE_DISADVANTAGE_MULTIPLIER, PokemonType.ICE: TYPE_NEUTRAL, PokemonType.DRAGON: TYPE_NEUTRAL, PokemonType.PSYCHIC: TYPE_NEUTRAL, PokemonType.NEUTRAL: TYPE_NEUTRAL},
            MoveType.GRASS: {PokemonType.FIRE: TYPE_DISADVANTAGE_MULTIPLIER, PokemonType.WATER: TYPE_ADVANTAGE_MULTIPLIER, PokemonType.GRASS: TYPE_NEUTRAL, PokemonType.ELECTRIC: TYPE_NEUTRAL, PokemonType.ICE: TYPE_DISADVANTAGE_MULTIPLIER, PokemonType.DRAGON: TYPE_NEUTRAL, PokemonType.PSYCHIC: TYPE_NEUTRAL, PokemonType.NEUTRAL: TYPE_NEUTRAL},
            MoveType.ELECTRIC: {PokemonType.FIRE: TYPE_NEUTRAL, PokemonType.WATER: TYPE_ADVANTAGE_MULTIPLIER, PokemonType.GRASS: TYPE_NEUTRAL, PokemonType.ELECTRIC: TYPE_NEUTRAL, PokemonType.ICE: TYPE_NEUTRAL, PokemonType.DRAGON: TYPE_NEUTRAL, PokemonType.PSYCHIC: TYPE_NEUTRAL, PokemonType.NEUTRAL: TYPE_NEUTRAL},
            MoveType.ICE: {PokemonType.FIRE: TYPE_DISADVANTAGE_MULTIPLIER, PokemonType.WATER: TYPE_NEUTRAL, PokemonType.GRASS: TYPE_ADVANTAGE_MULTIPLIER, PokemonType.ELECTRIC: TYPE_NEUTRAL, PokemonType.ICE: TYPE_NEUTRAL, PokemonType.DRAGON: TYPE_ADVANTAGE_MULTIPLIER, PokemonType.PSYCHIC: TYPE_NEUTRAL, PokemonType.NEUTRAL: TYPE_NEUTRAL},
            MoveType.DRAGON: {PokemonType.FIRE: TYPE_NEUTRAL, PokemonType.WATER: TYPE_NEUTRAL, PokemonType.GRASS: TYPE_NEUTRAL, PokemonType.ELECTRIC: TYPE_NEUTRAL, PokemonType.ICE: TYPE_DISADVANTAGE_MULTIPLIER, PokemonType.DRAGON: TYPE_NEUTRAL, PokemonType.PSYCHIC: TYPE_NEUTRAL, PokemonType.NEUTRAL: TYPE_NEUTRAL},
            MoveType.PSYCHIC: {PokemonType.FIRE: TYPE_NEUTRAL, PokemonType.WATER: TYPE_NEUTRAL, PokemonType.GRASS: TYPE_NEUTRAL, PokemonType.ELECTRIC: TYPE_NEUTRAL, PokemonType.ICE: TYPE_NEUTRAL, PokemonType.DRAGON: TYPE_NEUTRAL, PokemonType.PSYCHIC: TYPE_NEUTRAL, PokemonType.NEUTRAL: TYPE_NEUTRAL}
        }

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Pokemon Battle")

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.pokemon1_label = tk.Label(self.frame, text=f"{self.pokemon1.name}")
        self.pokemon1_label.grid(row=0, column=0, padx=10)

        self.pokemon1_health = ttk.Progressbar(self.frame, length=200, maximum=100)
        self.pokemon1_health.grid(row=1, column=0, padx=10)
        self.pokemon1_health['value'] = self.pokemon1.health_percentage()

        self.pokemon2_label = tk.Label(self.frame, text=f"{self.pokemon2.name}")
        self.pokemon2_label.grid(row=0, column=1, padx=10)

        self.pokemon2_health = ttk.Progressbar(self.frame, length=200, maximum=100)
        self.pokemon2_health.grid(row=1, column=1, padx=10)
        self.pokemon2_health['value'] = self.pokemon2.health_percentage()

        self.moves_frame = tk.Frame(self.root)
        self.moves_frame.pack(pady=10)

        self.move_buttons = []
        for move in self.pokemon1.moves:
            button = tk.Button(self.moves_frame, text=move.name, command=lambda m=move: self.perform_move(self.pokemon1, self.pokemon2, m))
            button.pack(side=tk.LEFT, padx=5)
            self.move_buttons.append(button)

        self.log_label = tk.Label(self.root, text="", justify=tk.LEFT)
        self.log_label.pack(pady=10)

        self.root.mainloop()

    def log(self, message):
        self.log_label.config(text=message)

    def perform_move(self, attacker: Pokemon, defender: Pokemon, move: Move):
        self.log(f"{attacker.name} used {move.name}!")
        self.apply_damage(defender, move, attacker.attack)
        self.update_health()

        if self.check_faint(defender):
            self.log(f"{defender.name} fainted!")
            self.disable_move_buttons()
        else:
            self.disable_move_buttons()
            self.root.after(1000, self.opponent_turn)

    def opponent_turn(self):
        move = np.random.choice(self.pokemon2.moves)
        self.log(f"{self.pokemon2.name} used {move.name}!")
        self.apply_damage(self.pokemon1, move, self.pokemon2.attack)
        self.update_health()

        if self.check_faint(self.pokemon1):
            self.log(f"{self.pokemon1.name} fainted!")
        else:
            self.enable_move_buttons()

    def apply_damage(self, defender: Pokemon, move: Move, attacker_attack: int):
        type_advantages = self.type_advantage()
        type_multiplier = type_advantages[move.m_type][defender.p_type]
        damage = (move.power * (attacker_attack / 10)) * type_multiplier - (defender.defense / 10)  # Adjusted damage calculation
        damage = max(1, damage)  # Ensure at least 1 damage is dealt
        defender.bars -= damage
        defender.bars = max(0, defender.bars)  # Ensure health doesn't drop below 0

    def update_health(self):
        self.pokemon1_health['value'] = self.pokemon1.health_percentage()
        self.pokemon2_health['value'] = self.pokemon2.health_percentage()

    def check_faint(self, pokemon: Pokemon) -> bool:
        return pokemon.bars <= 0

    def disable_move_buttons(self):
        for button in self.move_buttons:
            button.config(state=tk.DISABLED)

    def enable_move_buttons(self):
        for button in self.move_buttons:
            button.config(state=tk.NORMAL)

if __name__ == "__main__":
    # Create Pokemon
    Charizard = Pokemon("Charizard", PokemonType.FIRE, 
        [Move("Flamethrower", 10, MoveType.FIRE), Move("Fly", 8, MoveType.FIRE), Move("Blast Burn", 12, MoveType.FIRE), Move("Fire Punch", 8, MoveType.FIRE)], 
        {"ATTACK": 12, "DEFENSE": 8})

    Blastoise = Pokemon("Blastoise", PokemonType.WATER, 
        [Move("Water Gun", 8, MoveType.WATER), Move("Bubblebeam", 6, MoveType.WATER), Move("Hydro Pump", 10, MoveType.WATER), Move("Surf", 9, MoveType.WATER)], 
        {"ATTACK": 10, "DEFENSE": 10})

    Venusaur = Pokemon("Venusaur", PokemonType.GRASS, 
        [Move("Vine Whip", 8, MoveType.GRASS), Move("Razor Leaf", 10, MoveType.GRASS), Move("Earthquake", 12, MoveType.GRASS), Move("Frenzy Plant", 14, MoveType.GRASS)], 
        {"ATTACK": 8, "DEFENSE": 12})

    Pikachu = Pokemon("Pikachu", PokemonType.ELECTRIC, 
        [Move("Thunder Shock", 6, MoveType.ELECTRIC), Move("Quick Attack", 5, MoveType.ELECTRIC), Move("Thunderbolt", 9, MoveType.ELECTRIC), Move("Iron Tail", 7, MoveType.ELECTRIC)], 
        {"ATTACK": 7, "DEFENSE": 5})

    Gyarados = Pokemon("Gyarados", PokemonType.WATER, 
        [Move("Bite", 7, MoveType.DRAGON), Move("Dragon Rage", 8, MoveType.DRAGON), Move("Hydro Pump", 10, MoveType.WATER), Move("Hyper Beam", 12, MoveType.DRAGON)], 
        {"ATTACK": 11, "DEFENSE": 9})

    Arcanine = Pokemon("Arcanine", PokemonType.FIRE, 
        [Move("Flame Wheel", 8, MoveType.FIRE), Move("Bite", 6, MoveType.FIRE), Move("Extreme Speed", 10, MoveType.FIRE), Move("Fire Blast", 12, MoveType.FIRE)], 
        {"ATTACK": 10, "DEFENSE": 7})

    Jolteon = Pokemon("Jolteon", PokemonType.ELECTRIC, 
        [Move("Thunder Shock", 7, MoveType.ELECTRIC), Move("Quick Attack", 5, MoveType.ELECTRIC), Move("Thunder", 10, MoveType.ELECTRIC), Move("Pin Missile", 6, MoveType.ELECTRIC)], 
        {"ATTACK": 9, "DEFENSE": 5})

    Lapras = Pokemon("Lapras", PokemonType.WATER, 
        [Move("Ice Beam", 8, MoveType.ICE), Move("Body Slam", 7, MoveType.WATER), Move("Surf", 9, MoveType.WATER), Move("Hydro Pump", 10, MoveType.WATER)], 
        {"ATTACK": 9, "DEFENSE": 10})

    Exeggutor = Pokemon("Exeggutor", PokemonType.GRASS, 
        [Move("Seed Bomb", 8, MoveType.GRASS), Move("Confusion", 7, MoveType.PSYCHIC), Move("Solar Beam", 12, MoveType.GRASS), Move("Stomp", 6, MoveType.GRASS)], 
        {"ATTACK": 8, "DEFENSE": 9})

    Vaporeon = Pokemon("Vaporeon", PokemonType.WATER, 
        [Move("Water Gun", 7, MoveType.WATER), Move("Quick Attack", 5, MoveType.WATER), Move("Hydro Pump", 10, MoveType.WATER), Move("Aurora Beam", 8, MoveType.ICE)], 
        {"ATTACK": 8, "DEFENSE": 9})

    Flareon = Pokemon("Flareon", PokemonType.FIRE, 
        [Move("Ember", 6, MoveType.FIRE), Move("Bite", 5, MoveType.FIRE), Move("Flamethrower", 10, MoveType.FIRE), Move("Fire Blast", 12, MoveType.FIRE)], 
        {"ATTACK": 9, "DEFENSE": 6})

    Leafeon = Pokemon("Leafeon", PokemonType.GRASS, 
        [Move("Razor Leaf", 7, MoveType.GRASS), Move("Quick Attack", 5, MoveType.GRASS), Move("Solar Beam", 10, MoveType.GRASS), Move("Leaf Blade", 8, MoveType.GRASS)], 
        {"ATTACK": 9, "DEFENSE": 8})
    
    Charmeleon = Pokemon(
        "Charmeleon",
        "Fire",
        ["Ember", "Scratch", "Flamethrower", "Fire Punch"],
        {"ATTACK": 6, "DEFENSE": 5},
    )
    Wartortle = Pokemon(
        "Wartortle",
        "Water",
        ["Bubblebeam", "Water Gun", "Headbutt", "Surf"],
        {"ATTACK": 5, "DEFENSE": 5},
    )
    Ivysaur = Pokemon(
        "Ivysaur\t",
        "Grass",
        ["Vine Wip", "Razor Leaf", "Bullet Seed", "Leech Seed"],
        {"ATTACK": 4, "DEFENSE": 6},
    )

    Charmander = Pokemon(
        "Charmander",
        "Fire",
        ["Ember", "Scratch", "Tackle", "Fire Punch"],
        {"ATTACK": 4, "DEFENSE": 2},
    )
    Squirtle = Pokemon(
        "Squirtle",
        "Water",
        ["Bubblebeam", "Tackle", "Headbutt", "Surf"],
        {"ATTACK": 3, "DEFENSE": 3},
    )
    Bulbasaur = Pokemon(
        "Bulbasaur",
        "Grass",
        ["Vine Wip", "Razor Leaf", "Tackle", "Leech Seed"],
        {"ATTACK": 2, "DEFENSE": 4},
    )

    # Example Battle
    battle = Battle(Charizard, Leafeon)
