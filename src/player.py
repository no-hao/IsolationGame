from abc import ABC, abstractmethod
from .board import CellState, Board


def get_possible_moves(row, col):
    return [
        (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
        (row, col - 1),                         (row, col + 1),
        (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)
    ]


class Player(ABC):
    def __init__(self, name: str, player_type: str):
        self.name = name
        self.type = player_type
        self.position = None  # No default position here

    @abstractmethod
    def move(self, board: Board) -> None:
        pass

    @abstractmethod
    def remove_token(self, board: Board) -> None:
        pass

    def _is_valid_move(self, row: int, col: int, board: Board) -> bool:
        """Checks if the move is to an adjacent cell, within board boundaries, and the target cell is empty."""
        curr_row, curr_col = self.position
        dx = abs(curr_row - row)
        dy = abs(curr_col - col)

        return ((dx, dy) != (0, 0) and
                dx <= 1 and dy <= 1 and
                Board.is_within_board(row, col) and board.get_cell_state(row, col) == CellState.EMPTY)

    def _is_valid_removal(self, row: int, col: int, board: Board) -> bool:
        """Checks if the chosen token is within boundaries and is empty."""
        return Board.is_within_board(row, col) and board.get_cell_state(row, col) == CellState.EMPTY


class PlayerFactory:
    @staticmethod
    def create_player(player_type: str, name: str = None) -> Player:
        if player_type == "Human":
            return HumanPlayer(name=name or "Human")
        elif player_type == "Computer":
            return ComputerPlayer(name=name or "Computer")
        else:
            raise ValueError(f"Unknown player type: {player_type}")


class HumanPlayer(Player):
    def __init__(self, name: str = "Human", player_type: str = "Human"):
        super().__init__(name, player_type)

    def move(self, board: Board) -> None:
        while True:
            try:
                # Prompt user for the new position
                new_row, new_col = map(int, input("Enter row and column separated by space: ").split())
                if self._is_valid_move(new_row, new_col, board):
                    # Clear the player's old position
                    board.set_cell_state(*self.position, CellState.EMPTY)
                    # Update to the new position
                    board.set_cell_state(new_row, new_col, CellState.PLAYER_1 if self.name == "Player 1" else CellState.PLAYER_2)
                    self.position = (new_row, new_col)  # Update the player's internal position
                    break  # Exit the loop once a valid move is made
                else:
                    print("Invalid move. Please try again.")
            except ValueError:
                print("Invalid input format. Please enter row and column separated by space.")

    def remove_token(self, board: Board) -> None:
        while True:
            try:
                # Prompt user for the token they wish to remove
                row, col = map(int, input("Enter row and column of the token to remove, separated by space: ").split())
                if self._is_valid_removal(row, col, board):
                    board.set_cell_state(row, col, CellState.REMOVED)
                    break  # Exit the loop once a valid token is removed
                else:
                    print("Invalid token selection. Please try again.")
            except ValueError:
                print("Invalid input format. Please enter row and column separated by space.")


class ComputerPlayer(Player):
    def __init__(self, name: str = "Computer", player_type: str = "Computer"):
        super().__init__(name, player_type)

    def move(self, board: Board) -> None:
        pass

    def remove_token(self, board: Board) -> None:
        pass
