# Isolation Game

## Introduction
Isolation is an engaging board game where two players compete against each other. This implementation provides a graphical user interface, allowing players to interact with the game using a visual board.

## Dependencies
To run the game, ensure you have the following Python libraries installed:
- `tkinter`: For the graphical user interface.
- `time`: Used for handling time-related tasks.
- `random`: For generating random numbers and choices.
- `logging`: To log game events and other informational messages.
- `copy`: Used for creating deep copies of game objects.

You can install the required libraries using pip:

```
pip install tkinter
```

Note: Most of the above libraries come pre-installed with Python. Only `tkinter` might need explicit installation on some systems.

## Installation Instructions

1. Clone the repository:
   ```
   git clone [REPO_URL]
   ```
2. Navigate to the project directory:
   ```
   cd [DIRECTORY_NAME]
   ```
3. Ensure you have all the required dependencies installed. If not, install them using pip:
   ```
   pip install -r requirements.txt
   ```

## File Structure
```
.
├── main.py           # Entry point to start the game
└──src
    ├── gui.py            # Contains GUI implementation for the game
    ├── isolation.py      # Core game logic and rules
    └── player.py         # Contains player behavior and properties
    ```

## How to Play

1. Run the game using the following command:
   ```
   python main.py
   ```
2. Follow the on-screen instructions to play the game.

## License
This project is licensed under the MIT License. Please refer to the `LICENSE` file for more details.


## Gameplay Mechanics
The game of Isolation is played on a board where two players take turns moving. On each turn:
1. A player moves to any of the adjacent cells.
2. The player may then choose to remove a token from the board.
3. The game continues until one of the players cannot make a valid move, resulting in the other player winning.

## Player Behaviors
- **Human Player**: As a human player, you can interact with the graphical interface to make your moves and decide which tokens to remove from the board.
- **Computer Player**: The computer player, powered by AI, chooses its moves based on a combination of heuristics and the minimax algorithm. It evaluates the board state and decides on the best possible move to either advance its position or hinder the human player.

## AI Strategies
The computer player utilizes a set of heuristics to decide its moves:
- **Frontier Cells Heuristic**: Evaluates moves based on frontier cells.
- **Enhanced Mobility Heuristic**: Considers the player's future mobility on the board.
- **Control of Center Heuristic**: Gives importance to controlling the central cells of the board.
- **Token Removal Heuristic**: Evaluates the strategic removal of tokens to restrict the human player's movements.

Each of these heuristics contributes to the AI's decision-making process, making the game challenging and engaging.

## Troubleshooting
If you encounter any issues while playing the game:
1. Ensure all dependencies are correctly installed.
2. Check the game logs for any error messages or hints.
3. Restart the game and try again.

## Contribution
If you wish to contribute to the game's development:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and submit a pull request.
