from enum import Enum


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

    def __init__(self):
        self._grid = [[Cell() for _ in range(Board._NUM_COLS)] for _ in range(Board._NUM_ROWS)]
        # Initialize starting positions
        self.set_cell_state(0, 3, CellState.PLAYER_1)
        self.set_cell_state(7, 2, CellState.PLAYER_2)

    def set_cell_state(self, row, col, state):
        """Set the state of a cell at a specific position."""
        if not Board.is_within_board(row, col):
            raise ValueError(f"Position ({row}, {col}) is out of board boundaries.")
        if not isinstance(state, CellState):
            raise ValueError("Invalid state provided. Must be an instance of CellState.")
        self._grid[row][col].state = state

    def get_cell_state(self, row, col):
        """Get the state of a cell at a specific position."""
        if Board.is_within_board(row, col):
            return self._grid[row][col].state
        return None

    @staticmethod
    def is_within_board(row, col):
        """Determine if the given move (row, col) is within the board boundaries."""
        return 0 <= row < Board._NUM_ROWS and 0 <= col < Board._NUM_COLS

    def display(self):
        """Display the board in a visually appealing format."""
        col_indices = '    ' + '   '.join([f"{col}" for col in range(self._NUM_COLS)])
        separator = '  +' + '---+' * self._NUM_COLS
        rows = [separator]
        for row in range(self._NUM_ROWS):
            rows.append(f"{row} | " + " | ".join([cell.value for cell in self._grid[row]]) + " |")
            rows.append(separator)
        return "\n".join([col_indices] + rows)

    def simulate_move(self, row, col, state):
        """Simulates a move and returns the resulting new board state without modifying the current board."""
        new_board = Board()
        new_board._grid = [[Cell(cell.state) for cell in row] for row in self._grid]  # Deep copy of the board grid
        new_board.set_cell_state(row, col, state)
        return new_board
