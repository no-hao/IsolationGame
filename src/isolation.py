import random
from .player import HumanPlayer, ComputerPlayer

class IsolationGameState:
    def __init__(self, player_A=None, player_B=None):
        # Parameters
        self.rows = 8
        self.columns = 6

        # Initialize or reset the game state
        self.current_player = random.choice(["A", "B"])

        default_player_A = {"row": 0, "column": 3, "player_obj": HumanPlayer()}
        default_player_B = {"row": 7, "column": 2, "player_obj": HumanPlayer()}

        # Set the players based on the provided arguments
        self.players = {
            "A": player_A if player_A and self._is_valid_player(player_A) else default_player_A,
            "B": player_B if player_B and self._is_valid_player(player_B) else default_player_B
        }

        self.removed_tokens = set()
        self.is_move_phase = True
        self.game_over = False
        print("End of __init__ in IsolationGameState:", self.players)

    def _is_valid_player(self, player):
        """Helper function to check if a player dictionary is valid."""
        return all(key in player for key in ["row", "column", "player_obj"])

    def is_valid_removal(self, row, column):
        """
        Check if a cell is a valid target for removal.

        Parameters:
        - row (int): The row index of the cell.
        - column (int): The column index of the cell.

        Returns:
        - bool: True if the cell is a valid target for removal, otherwise False.
        """
        # Check if the cell is within the board dimensions
        if not (0 <= row < 8 and 0 <= column < 6):
            return False

        # Check if the cell already has a removed token
        if (row, column) in self.removed_tokens:
            return False

        # Check if the cell has a player in it
        if (row, column) == self.get_player_position("A") or (row, column) == self.get_player_position("B"):
            return False

        return True

    def get_current_player_obj(self):
        return self.players[self.current_player].get("player_obj", None)

    def get_player_position(self, player):
        return (self.players[player]['row'], self.players[player]['column'])

    def get_valid_moves_for_current_player(self):
        row, column = self.get_player_position(self.current_player)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        valid_moves = []
        for dr, dc in directions:
            new_row, new_column = row + dr, column + dc
            if (0 <= new_row < 8 and 
                0 <= new_column < 6 and 
                (new_row, new_column) not in self.removed_tokens and
                (new_row, new_column) != self.get_player_position("A") and 
                (new_row, new_column) != self.get_player_position("B")):
                    valid_moves.append((new_row, new_column))
        return valid_moves

    def apply_move(self, move):
        row, column = move
        self.players[self.current_player]['row'] = row
        self.players[self.current_player]['column'] = column
        print(f"Player {self.current_player} moved to {move}.")

    def can_remove_token(self, row, column):
        """Checks if the cell can be validly removed."""
        if (row, column) in self.removed_tokens:
            return False
        if (row, column) == self.get_player_position("A") or (row, column) == self.get_player_position("B"):
            return False
        return True

    def apply_remove_token(self, row, column):
        """Removes a cell and updates the game state if it's valid."""
        if self.can_remove_cell(row, column):
            self.removed_tokens.add((row, column))
            print(f"Token removed from cell ({row}, {column}).")
            return True
        return False

    def switch_phase(self):
        self.is_move_phase = not self.is_move_phase
        phase = "Move Phase" if self.is_move_phase else "Removal Phase"
        print(f"Switched to {phase} for Player {self.current_player}.")

    def switch_player(self):
        self.current_player = "A" if self.current_player == "B" else "B"
        self.is_move_phase = True
        print(f"Switched to Player {self.current_player}'s turn.")

    def check_win_condition(self):
        valid_moves = self.get_valid_moves_for_current_player()
        return not valid_moves
