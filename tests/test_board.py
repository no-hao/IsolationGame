import unittest
from src.board import Board, CellState


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_initialization(self):
        """Test if the board initializes correctly."""
        for i in range(Board._NUM_ROWS):
            for j in range(Board._NUM_COLS):
                self.assertEqual(self.board.get_cell_state(i, j), CellState.EMPTY)

    def test_set_get_cell_state(self):
        """Test setting and getting cell states."""
        self.board.set_cell_state(1, 1, CellState.PLAYER_1)
        self.assertEqual(self.board.get_cell_state(1, 1), CellState.PLAYER_1)
        self.board.set_cell_state(1, 1, CellState.PLAYER_2)
        self.assertEqual(self.board.get_cell_state(1, 1), CellState.PLAYER_2)
        self.board.set_cell_state(1, 1, CellState.REMOVED)
        self.assertEqual(self.board.get_cell_state(1, 1), CellState.REMOVED)

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

    def test_observer_notification(self):
        """Test if observers are correctly notified when the board changes."""
        class MockObserver:
            def __init__(self):
                self.notified = False

            def update(self, *args, **kwargs):
                self.notified = True

        observer = MockObserver()
        self.board.add_observer(observer)
        self.board.set_cell_state(1, 1, CellState.PLAYER_1)
        self.assertTrue(observer.notified)

    def test_invalid_set_cell_state(self):
        """Test setting a cell state outside grid boundaries."""
        with self.assertRaises(ValueError):
            self.board.set_cell_state(10, 10, CellState.PLAYER_1)


if __name__ == "__main__":
    unittest.main()
