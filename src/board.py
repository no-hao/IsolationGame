from enum import Enum
from copy import deepcopy


class CellState(Enum):
    EMPTY = " "
    PLAYER_1 = "1"
    PLAYER_2 = "2"
    REMOVED = "X"


class Cell:
    def __init__(self, state=CellState.EMPTY):
        self.state = state

    @property
    def value(self):
        return self.state.value


class Board:
    _NUM_ROWS = 8  # Class constant for number of rows
    _NUM_COLS = 6  # Class constant for number of columns

    @staticmethod
    def get_possible_moves(row, col):
        return [
            (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
            (row, col - 1),                         (row, col + 1),
            (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)
        ]

    def __init__(self):
        self._observers = []
        self._grid = [[Cell() for _ in range(Board._NUM_COLS)] for _ in range(Board._NUM_ROWS)]

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        print("[DEBUG] Notifying all observers of the board change.")
        for observer in self._observers:
            observer.update()

    def set_cell_state(self, row, col, state):
        if not Board.is_within_board(row, col):
            raise ValueError(f"Position ({row}, {col}) is out of board boundaries.")
        if not isinstance(state, CellState):
            raise ValueError("Invalid state provided. Must be an instance of CellState.")
        self._grid[row][col].state = state
        self.notify_observers()  # Notify observers of the change

    def get_cell_state(self, row, col):
        if Board.is_within_board(row, col):
            return self._grid[row][col].state
        return None

    @staticmethod
    def is_within_board(row, col):
        return 0 <= row < Board._NUM_ROWS and 0 <= col < Board._NUM_COLS

    def display(self):
        col_indices = '    ' + '   '.join([f"{col}" for col in range(self._NUM_COLS)])
        separator = '  +' + '---+' * self._NUM_COLS
        rows = [separator]
        for row in range(self._NUM_ROWS):
            rows.append(f"{row} | " + " | ".join([cell.value for cell in self._grid[row]]) + " |")
            rows.append(separator)
        return "\n".join([col_indices] + rows)

    def simulate_move(self, row, col, state):
        new_board = Board()
        new_board._grid = deepcopy(self._grid)
        new_board.set_cell_state(row, col, state)
        return new_board
