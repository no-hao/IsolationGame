from abc import ABC, abstractmethod
import random

class Player(ABC):
    @abstractmethod
    def choose_move(self, game_state):
        pass

class HumanPlayer(Player):
    def choose_move(self, game_state):
        # The logic for a human player to choose a move.
        # This will be handled by GUI events.
        pass

class ComputerPlayer(Player):
    def choose_move(self, game_state):
        # The logic for the computer to select a move.
        # This will be a simple random choice for now.
        valid_moves = game_state.get_valid_moves_for_current_player()
        move = random.choice(valid_moves) if valid_moves else None
        return move

    def choose_cell_to_remove(self, game_state):
        valid_remove_cells = [
            (r, c) for r in range(game_state.rows) for c in range(game_state.columns)
            if (r, c) not in game_state.removed_tokens and
            (r, c) != game_state.get_player_position("A") and 
            (r, c) != game_state.get_player_position("B")
        ]
        remove_cell = random.choice(valid_remove_cells) if valid_remove_cells else None
        return remove_cell
