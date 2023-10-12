import unittest
from src.game import Game
from src.board import Board, CellState
from src.player import HumanPlayer, ComputerPlayer, Heuristics

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player1 = HumanPlayer(player_id="1", player_type="Human")
        self.player2 = ComputerPlayer(player_id="2", player_type="Computer", game=None, board=None, heuristic_function=Heuristics.mobility)
        self.game = Game(self.player1, self.player2)  # Initialize the game with both players
        self.board = self.game.board
        # Update the game and board references for player2
        self.player2.game = self.game
        self.player2.board = self.board

    def test_initialization(self):
        self.assertIsInstance(self.player1, HumanPlayer)
        self.assertIsInstance(self.player2, ComputerPlayer)
        self.assertEqual(self.player1.player_id, "1")
        self.assertEqual(self.player2.player_id, "2")

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
