import unittest
from src.board import Board, CellState


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

        def test_grid_initialization(self):
            """Test if the board's grid initializes correctly."""
            # Check the dimensions
            self.assertEqual(len(self.board._grid), Board._NUM_ROWS)
            for row in self.board._grid:
                self.assertEqual(len(row), Board._NUM_COLS)

            # Check that all cells are initialized to CellState.EMPTY
            for i in range(Board._NUM_ROWS):
                for j in range(Board._NUM_COLS):
                    self.assertEqual(self.board.get_cell_state(i, j), CellState.EMPTY)

    def test_initialization(self):
        """Test if the board initializes correctly."""
        self.assertEqual(self.board._NUM_ROWS, 8)
        self.assertEqual(self.board._NUM_COLS, 6)
        self.assertEqual(self.board.get_cell_state(0, 3), CellState.PLAYER_1)
        self.assertEqual(self.board.get_cell_state(7, 2), CellState.PLAYER_2)

    def test_set_get_cell_state(self):
        """Test setting and getting cell states."""
        self.board.set_cell_state(1, 1, CellState.PLAYER_1)
        self.assertEqual(self.board.get_cell_state(1, 1), CellState.PLAYER_1)

        self.board.set_cell_state(1, 1, CellState.PLAYER_2)
        self.assertEqual(self.board.get_cell_state(1, 1), CellState.PLAYER_2)

        self.board.set_cell_state(1, 1, CellState.REMOVED)
        self.assertEqual(self.board.get_cell_state(1, 1), CellState.REMOVED)

    def test_display(self):
        """Test the display method."""
        display_output = self.board.display()
        self.assertTrue("0 |   |   |   | 1 |   |   |" in display_output)
        self.assertTrue("7 |   |   | 2 |   |   |   |" in display_output)

    def test_simulate_move(self):
        """Test the simulate_move method."""
        # Setting an initial state
        self.board.set_cell_state(2, 3, CellState.PLAYER_1)

        # Simulate a move without modifying the original board
        new_board = self.board.simulate_move(3, 3, CellState.PLAYER_2)

        # Check the original board state remains unchanged
        self.assertEqual(self.board.get_cell_state(2, 3), CellState.PLAYER_1)
        self.assertEqual(self.board.get_cell_state(3, 3), CellState.EMPTY)

        # Check the new board has the simulated move
        self.assertEqual(new_board.get_cell_state(2, 3), CellState.PLAYER_1)
        self.assertEqual(new_board.get_cell_state(3, 3), CellState.PLAYER_2)


if __name__ == "__main__":
    unittest.main()
