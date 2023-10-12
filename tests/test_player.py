import unittest
from src.board import Board, CellState
from src.player import HumanPlayer, ComputerPlayer

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.player1 = HumanPlayer(player_id="1", player_type="Human")
        self.player2 = ComputerPlayer(player_id="2", player_type="Computer")
        # Set initial positions for the players for the purpose of these tests
        self.player1.position = (3, 3)
        self.player2.position = (4, 4)

    def test_initialization(self):
        self.assertEqual(self.player1.player_id, "1")
        self.assertEqual(self.player1.player_type, "Human")
        self.assertEqual(self.player2.player_id, "2")
        self.assertEqual(self.player2.player_type, "Computer")

    def test_valid_move(self):
        self.assertTrue(self.player1._is_valid_move(4, 3, self.board))
        self.assertTrue(self.player1._is_valid_move(3, 4, self.board))
        self.assertFalse(self.player1._is_valid_move(5, 5, self.board))
        self.assertFalse(self.player1._is_valid_move(8, 8, self.board))

    def test_move_to_non_empty_cell(self):
        self.board.set_cell_state(4, 3, CellState.PLAYER_2)
        self.assertFalse(self.player1._is_valid_move(4, 3, self.board))

    def test_valid_removal(self):
        self.board.set_cell_state(3, 3, CellState.REMOVED)
        self.assertFalse(self.player1._is_valid_removal(3, 3, self.board))
        self.assertTrue(self.player1._is_valid_removal(4, 3, self.board))
        self.assertFalse(self.player1._is_valid_removal(8, 8, self.board))

if __name__ == "__main__":
    unittest.main()
