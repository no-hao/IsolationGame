from abc import ABC, abstractmethod
from .board import CellState, Board


class Player(ABC):
    def __init__(self, player_id: str, player_type: str):
        self.player_id = player_id
        self.player_type = player_type
        self.position = None  # No default position here

    def __str__(self):
        return f"Player {self.player_id}"  # Using player_id as the display

    @abstractmethod
    def move(self, board: Board) -> tuple:
        pass

    @abstractmethod
    def remove_token(self, board: Board) -> tuple:
        pass

    def _is_valid_move(self, row: int, col: int, board: Board) -> bool:
        """Checks if the move is to an adjacent cell, within board boundaries, and the target cell is empty."""
        curr_row, curr_col = self.position
        dx = abs(curr_row - row)
        dy = abs(curr_col - col)

        return ((dx + dy) != 0 and
                dx <= 1 and dy <= 1 and
                Board.is_within_board(row, col) and board.get_cell_state(row, col) == CellState.EMPTY)


    def _is_valid_removal(self, row: int, col: int, board: Board) -> bool:
        """Checks if the chosen token is within boundaries and is empty."""
        return Board.is_within_board(row, col) and board.get_cell_state(row, col) == CellState.EMPTY

    def update(self):
        print(f"[DEBUG] Player {self.player_id} is being updated due to board change.")
        # Here, you can add any logic that the player should execute in response to board changes.

class PlayerFactory:
    @staticmethod
    def create_player(player_type: str, player_id: str) -> Player:
        if player_type == "Human":
            return HumanPlayer(player_id=player_id, player_type="Human")
        elif player_type == "Computer":
            return ComputerPlayer(player_id=player_id, player_type="Computer")
        else:
            raise ValueError(f"Unknown player type: {player_type}")


class HumanPlayer(Player):
    def move(self, board: Board) -> tuple:
        while True:
            try:
                row, col = map(int, input("Enter your move (row col): ").split())
                if self._is_valid_move(row, col, board):
                    return row, col
                else:
                    print("Invalid move. Please try again.")
            except ValueError:
                print("Invalid input format. Please enter row and column separated by space.")

    def remove_token(self, board: Board) -> tuple:
        while True:
            try:
                row, col = map(int, input("Enter the token position to remove (row col): ").split())
                if self._is_valid_removal(row, col, board):
                    return row, col
                else:
                    print("Invalid position. Please try again.")
            except ValueError:
                print("Invalid input format. Please enter row and column separated by space.")


class ComputerPlayer(Player):
    def move(self, board: Board) -> tuple:
        pass
        # This method will decide a move using the MCTS algorithm and heuristics.
        # The details will be added later when we integrate the MCTS logic.

    def remove_token(self, board: Board) -> tuple:
        pass
        # This method will decide a token to remove using the MCTS algorithm and heuristics.


class HeuristicStrategy(ABC):
    @abstractmethod
    def evaluate_board(self, board, player):
        pass


class HeuristicStrategy1(HeuristicStrategy):
    def evaluate_board(self, board, player):
        pass
        # Implementation for the first heuristic will be added later


class HeuristicStrategy2(HeuristicStrategy):
    def evaluate_board(self, board, player):
        pass
        # Implementation for the second heuristic will be added later
