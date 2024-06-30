
# Pokémon Battle Game

This project is a simple Pokémon battle simulation game built using Python and Tkinter. It allows users to select their Pokémon and an opponent Pokémon to engage in a turn-based battle.

## Features

- **Select Pokémon:** Choose your Pokémon and your opponent's Pokémon from a list.
- **Random Selection:** Option to randomly select a Pokémon for both the player and the opponent.
- **Turn-Based Battle:** Engage in a turn-based battle with moves and type advantages.
- **Status Effects:** Moves can apply status effects like Burn, Paralysis, and Poison.
- **Battle Log:** View detailed battle log messages including move effectiveness and critical hits.

## Pokémon Types and Moves

The game includes multiple Pokémon types such as Fire, Water, Grass, Electric, Ice, Dragon, Psychic, and Normal. Each Pokémon has a set of moves with different power and types.

## Getting Started

### Prerequisites

- Python 3.x
- Tkinter (usually included with Python)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/mikeorte/Pokemon-Battle.git
    ```
2. Navigate to the project directory:
    ```sh
    cd pokemon-battle-game
    ```

### Running the Game

Run the following command to start the game:
```sh
python pokemon_battle_game.py
```

## Code Overview

### Constants

- `HEALTH_BAR_LENGTH`: Length of the health bar.
- `TYPE_ADVANTAGE_MULTIPLIER`: Multiplier for type advantages.
- `TYPE_DISADVANTAGE_MULTIPLIER`: Multiplier for type disadvantages.
- `PRINT_DELAY`: Delay between print messages.
- `TYPE_NEUTRAL`: Neutral type multiplier.

### Classes

- `PokemonType`: Enum for Pokémon types.
- `MoveType`: Enum for move types.
- `Move`: Class representing a move with name, power, and type.
- `StatusEffect`: Enum for status effects (None, Burn, Paralysis, Poison).
- `Pokemon`: Class representing a Pokémon with name, type, moves, and stats.
- `Battle`: Class managing the battle logic and GUI.
- `PokemonSelectionApp`: Class for the Pokémon selection GUI.

## Future Improvements

- Add more Pokémon and moves.
- Implement additional status effects.
- Enhance the GUI with animations and improved graphics.
- Add sound effects for moves and status effects.

## License

This project is licensed under the MIT License.

## Acknowledgements

- Inspired by the Pokémon games by Nintendo.
- Built using Python and Tkinter.
