import time
import numpy as np
import sys
import tkinter as tk
from tkinter import ttk
from enum import Enum
from typing import List, Dict

# Constants
HEALTH_BAR_LENGTH = 20
TYPE_ADVANTAGE_MULTIPLIER = 1.5
TYPE_DISADVANTAGE_MULTIPLIER = 0.75
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
    NORMAL = "Normal"

class MoveType(Enum):
    FIRE = "Fire"
    WATER = "Water"
    GRASS = "Grass"
    ELECTRIC = "Electric"
    ICE = "Ice"
    DRAGON = "Dragon"
    PSYCHIC = "Psychic"
    NORMAL = "Normal"

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
    def __init__(self, root, pokemon1: Pokemon, pokemon2: Pokemon):
        self.root = root
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.create_battle_gui()

    def type_advantage(self):
        return {
            MoveType.FIRE: {PokemonType.FIRE: TYPE_NEUTRAL, PokemonType.WATER: TYPE_DISADVANTAGE_MULTIPLIER, PokemonType.GRASS: TYPE_ADVANTAGE_MULTIPLIER, PokemonType.ELECTRIC: TYPE_NEUTRAL, PokemonType.ICE: TYPE_ADVANTAGE_MULTIPLIER, PokemonType.DRAGON: TYPE_NEUTRAL, PokemonType.PSYCHIC: TYPE_NEUTRAL, PokemonType.NORMAL: TYPE_NEUTRAL},
            MoveType.WATER: {PokemonType.FIRE: TYPE_ADVANTAGE_MULTIPLIER, PokemonType.WATER: TYPE_NEUTRAL, PokemonType.GRASS: TYPE_DISADVANTAGE_MULTIPLIER, PokemonType.ELECTRIC: TYPE_DISADVANTAGE_MULTIPLIER, PokemonType.ICE: TYPE_NEUTRAL, PokemonType.DRAGON: TYPE_NEUTRAL, PokemonType.PSYCHIC: TYPE_NEUTRAL, PokemonType.NORMAL: TYPE_NEUTRAL},
            MoveType.GRASS: {PokemonType.FIRE: TYPE_DISADVANTAGE_MULTIPLIER, PokemonType.WATER: TYPE_ADVANTAGE_MULTIPLIER, PokemonType.GRASS: TYPE_NEUTRAL, PokemonType.ELECTRIC: TYPE_NEUTRAL, PokemonType.ICE: TYPE_DISADVANTAGE_MULTIPLIER, PokemonType.DRAGON: TYPE_NEUTRAL, PokemonType.PSYCHIC: TYPE_NEUTRAL, PokemonType.NORMAL: TYPE_NEUTRAL},
            MoveType.ELECTRIC: {PokemonType.FIRE: TYPE_NEUTRAL, PokemonType.WATER: TYPE_ADVANTAGE_MULTIPLIER, PokemonType.GRASS: TYPE_NEUTRAL, PokemonType.ELECTRIC: TYPE_NEUTRAL, PokemonType.ICE: TYPE_NEUTRAL, PokemonType.DRAGON: TYPE_NEUTRAL, PokemonType.PSYCHIC: TYPE_NEUTRAL, PokemonType.NORMAL: TYPE_NEUTRAL},
            MoveType.ICE: {PokemonType.FIRE: TYPE_DISADVANTAGE_MULTIPLIER, PokemonType.WATER: TYPE_NEUTRAL, PokemonType.GRASS: TYPE_ADVANTAGE_MULTIPLIER, PokemonType.ELECTRIC: TYPE_NEUTRAL, PokemonType.ICE: TYPE_NEUTRAL, PokemonType.DRAGON: TYPE_ADVANTAGE_MULTIPLIER, PokemonType.PSYCHIC: TYPE_NEUTRAL, PokemonType.NORMAL: TYPE_NEUTRAL},
            MoveType.DRAGON: {PokemonType.FIRE: TYPE_NEUTRAL, PokemonType.WATER: TYPE_NEUTRAL, PokemonType.GRASS: TYPE_NEUTRAL, PokemonType.ELECTRIC: TYPE_NEUTRAL, PokemonType.ICE: TYPE_DISADVANTAGE_MULTIPLIER, PokemonType.DRAGON: TYPE_NEUTRAL, PokemonType.PSYCHIC: TYPE_NEUTRAL, PokemonType.NORMAL: TYPE_NEUTRAL},
            MoveType.PSYCHIC: {PokemonType.FIRE: TYPE_NEUTRAL, PokemonType.WATER: TYPE_NEUTRAL, PokemonType.GRASS: TYPE_NEUTRAL, PokemonType.ELECTRIC: TYPE_NEUTRAL, PokemonType.ICE: TYPE_NEUTRAL, PokemonType.DRAGON: TYPE_NEUTRAL, PokemonType.PSYCHIC: TYPE_NEUTRAL, PokemonType.NORMAL: TYPE_NEUTRAL},
            MoveType.NORMAL: {PokemonType.FIRE: TYPE_NEUTRAL, PokemonType.WATER: TYPE_NEUTRAL, PokemonType.GRASS: TYPE_NEUTRAL, PokemonType.ELECTRIC: TYPE_NEUTRAL, PokemonType.ICE: TYPE_NEUTRAL, PokemonType.DRAGON: TYPE_NEUTRAL, PokemonType.PSYCHIC: TYPE_NEUTRAL, PokemonType.NORMAL: TYPE_NEUTRAL}
        }

    def create_battle_gui(self):
        self.battle_frame = tk.Frame(self.root)
        self.battle_frame.pack(pady=20)

        self.pokemon1_label = tk.Label(self.battle_frame, text=f"{self.pokemon1.name}")
        self.pokemon1_label.grid(row=0, column=0, padx=10)

        self.pokemon1_health = ttk.Progressbar(self.battle_frame, length=200, maximum=100)
        self.pokemon1_health.grid(row=1, column=0, padx=10)
        self.pokemon1_health['value'] = self.pokemon1.health_percentage()

        self.pokemon2_label = tk.Label(self.battle_frame, text=f"{self.pokemon2.name}")
        self.pokemon2_label.grid(row=0, column=1, padx=10)

        self.pokemon2_health = ttk.Progressbar(self.battle_frame, length=200, maximum=100)
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

class PokemonSelectionApp:
    def __init__(self, root):
        self.root = root
        self.create_selection_gui()

    def create_selection_gui(self):
        self.selection_frame = tk.Frame(self.root)
        self.selection_frame.pack(pady=20)

        self.pokemon_var1 = tk.StringVar()
        self.pokemon_var2 = tk.StringVar()

        pokemon_names = [p.name for p in all_pokemons]

        self.pokemon_var1.set(pokemon_names[0])
        self.pokemon_var2.set(pokemon_names[0])

        tk.Label(self.selection_frame, text="Select your Pokemon:").grid(row=0, column=0)
        self.pokemon_dropdown1 = ttk.Combobox(self.selection_frame, textvariable=self.pokemon_var1, values=pokemon_names)
        self.pokemon_dropdown1.grid(row=0, column=1)

        tk.Button(self.selection_frame, text="Random", command=self.random_select_pokemon1).grid(row=0, column=2)

        tk.Label(self.selection_frame, text="Select opponent Pokemon:").grid(row=1, column=0)
        self.pokemon_dropdown2 = ttk.Combobox(self.selection_frame, textvariable=self.pokemon_var2, values=pokemon_names)
        self.pokemon_dropdown2.grid(row=1, column=1)

        tk.Button(self.selection_frame, text="Random", command=self.random_select_pokemon2).grid(row=1, column=2)

        tk.Button(self.selection_frame, text="Start Battle", command=self.start_battle).grid(row=2, columnspan=3, pady=10)

    def random_select_pokemon1(self):
        self.pokemon_var1.set(np.random.choice([p.name for p in all_pokemons]))

    def random_select_pokemon2(self):
        self.pokemon_var2.set(np.random.choice([p.name for p in all_pokemons]))

    def start_battle(self):
        pokemon1 = next(p for p in all_pokemons if p.name == self.pokemon_var1.get())
        pokemon2 = next(p for p in all_pokemons if p.name == self.pokemon_var2.get())

        self.selection_frame.pack_forget()
        Battle(self.root, pokemon1, pokemon2)

if __name__ == "__main__":
    # Create Pokemon
    all_pokemons = [
        Pokemon("Charizard", PokemonType.FIRE, 
                [Move("Flamethrower", 10, MoveType.FIRE), Move("Fly", 8, MoveType.NORMAL), Move("Blast Burn", 12, MoveType.FIRE), Move("Fire Punch", 8, MoveType.FIRE)], 
                {"ATTACK": 12, "DEFENSE": 8}),
        Pokemon("Blastoise", PokemonType.WATER, 
                [Move("Water Gun", 8, MoveType.WATER), Move("Bubblebeam", 6, MoveType.WATER), Move("Hydro Pump", 10, MoveType.WATER), Move("Surf", 9, MoveType.WATER)], 
                {"ATTACK": 10, "DEFENSE": 10}),
        Pokemon("Venusaur", PokemonType.GRASS, 
                [Move("Vine Whip", 8, MoveType.GRASS), Move("Razor Leaf", 10, MoveType.GRASS), Move("Earthquake", 12, MoveType.NORMAL), Move("Frenzy Plant", 14, MoveType.GRASS)], 
                {"ATTACK": 8, "DEFENSE": 12}),
                Pokemon("Charmeleon", PokemonType.FIRE,
                [Move("Ember", 6, MoveType.FIRE), Move("Scratch", 5, MoveType.NORMAL), Move("Flamethrower", 10, MoveType.FIRE), Move("Fire Punch", 8, MoveType.FIRE)],
                {"ATTACK": 6, "DEFENSE": 5}),
        Pokemon("Wartortle", PokemonType.WATER,
                [Move("Bubblebeam", 6, MoveType.WATER), Move("Water Gun", 7, MoveType.WATER), Move("Headbutt", 5, MoveType.NORMAL), Move("Surf", 9, MoveType.WATER)],
                {"ATTACK": 5, "DEFENSE": 5}),
        Pokemon("Ivysaur", PokemonType.GRASS,
                [Move("Vine Whip", 8, MoveType.GRASS), Move("Razor Leaf", 10, MoveType.GRASS), Move("Bullet Seed", 5, MoveType.GRASS), Move("Leech Seed", 6, MoveType.GRASS)],
                {"ATTACK": 4, "DEFENSE": 6}),
        Pokemon("Charmander", PokemonType.FIRE,
                [Move("Ember", 6, MoveType.FIRE), Move("Scratch", 5, MoveType.NORMAL), Move("Tackle", 4, MoveType.NORMAL), Move("Fire Punch", 8, MoveType.FIRE)],
                {"ATTACK": 4, "DEFENSE": 2}),
        Pokemon("Squirtle", PokemonType.WATER,
                [Move("Bubblebeam", 6, MoveType.WATER), Move("Tackle", 4, MoveType.NORMAL), Move("Headbutt", 5, MoveType.NORMAL), Move("Surf", 9, MoveType.WATER)],
                {"ATTACK": 3, "DEFENSE": 3}),
        Pokemon("Bulbasaur", PokemonType.GRASS,
                [Move("Vine Whip", 8, MoveType.GRASS), Move("Razor Leaf", 10, MoveType.GRASS), Move("Tackle", 4, MoveType.NORMAL), Move("Leech Seed", 6, MoveType.GRASS)],
                {"ATTACK": 2, "DEFENSE": 4}),
        Pokemon("Pikachu", PokemonType.ELECTRIC, 
                [Move("Thunder Shock", 6, MoveType.ELECTRIC), Move("Quick Attack", 5, MoveType.NORMAL), Move("Thunderbolt", 9, MoveType.ELECTRIC), Move("Iron Tail", 7, MoveType.NORMAL)], 
                {"ATTACK": 7, "DEFENSE": 5}),
        Pokemon("Gyarados", PokemonType.WATER, 
                [Move("Bite", 7, MoveType.NORMAL), Move("Dragon Rage", 8, MoveType.DRAGON), Move("Hydro Pump", 10, MoveType.WATER), Move("Hyper Beam", 12, MoveType.DRAGON)], 
                {"ATTACK": 11, "DEFENSE": 9}),
        Pokemon("Arcanine", PokemonType.FIRE, 
                [Move("Flame Wheel", 8, MoveType.FIRE), Move("Bite", 6, MoveType.NORMAL), Move("Extreme Speed", 10, MoveType.NORMAL), Move("Fire Blast", 12, MoveType.FIRE)], 
                {"ATTACK": 10, "DEFENSE": 7}),
        Pokemon("Jolteon", PokemonType.ELECTRIC, 
                [Move("Thunder Shock", 7, MoveType.ELECTRIC), Move("Quick Attack", 5, MoveType.NORMAL), Move("Thunder", 10, MoveType.ELECTRIC), Move("Pin Missile", 6, MoveType.NORMAL)], 
                {"ATTACK": 9, "DEFENSE": 5}),
        Pokemon("Lapras", PokemonType.WATER, 
                [Move("Ice Beam", 8, MoveType.ICE), Move("Body Slam", 7, MoveType.NORMAL), Move("Surf", 9, MoveType.WATER), Move("Hydro Pump", 10, MoveType.WATER)], 
                {"ATTACK": 9, "DEFENSE": 10}),
        Pokemon("Exeggutor", PokemonType.GRASS, 
                [Move("Seed Bomb", 8, MoveType.GRASS), Move("Confusion", 7, MoveType.PSYCHIC), Move("Solar Beam", 12, MoveType.GRASS), Move("Stomp", 6, MoveType.NORMAL)], 
                {"ATTACK": 8, "DEFENSE": 9}),
        Pokemon("Vaporeon", PokemonType.WATER, 
                [Move("Water Gun", 7, MoveType.WATER), Move("Quick Attack", 5, MoveType.NORMAL), Move("Hydro Pump", 10, MoveType.WATER), Move("Aurora Beam", 8, MoveType.ICE)], 
                {"ATTACK": 8, "DEFENSE": 9}),
        Pokemon("Flareon", PokemonType.FIRE, 
                [Move("Ember", 6, MoveType.FIRE), Move("Bite", 5, MoveType.NORMAL), Move("Flamethrower", 10, MoveType.FIRE), Move("Fire Blast", 12, MoveType.FIRE)], 
                {"ATTACK": 9, "DEFENSE": 6}),
        Pokemon("Leafeon", PokemonType.GRASS, 
                [Move("Razor Leaf", 7, MoveType.GRASS), Move("Quick Attack", 5, MoveType.NORMAL), Move("Solar Beam", 10, MoveType.GRASS), Move("Leaf Blade", 8, MoveType.GRASS)], 
                {"ATTACK": 9, "DEFENSE": 8})
    ]

    # Start selection screen
    root = tk.Tk()
    root.title("Pokemon Battle")
    app = PokemonSelectionApp(root)
    root.mainloop()
