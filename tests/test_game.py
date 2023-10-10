import random
import unittest
from src.game import Game
from src.board import Board, CellState
from src.player import HumanPlayer, ComputerPlayer


class TestGame(unittest.TestCase):

    def setUp(self):
        self.player1 = HumanPlayer()
        self.player2 = ComputerPlayer()
        self.game = Game(self.player1, self.player2)

    def test_initialization(self):
        """Test if the game initializes correctly."""
        self.assertEqual(self.player1.position, (0, 3))
        self.assertEqual(self.player2.position, (7, 2))
        self.assertIn(self.game.current_player, [self.player1, self.player2])
        self.assertIn(self.game.next_player, [self.player1, self.player2])
        self.assertNotEqual(self.game.current_player, self.game.next_player)

    def test_switch_players(self):
        """Test if players switch correctly after a move."""
        initial_current_player = self.game.current_player
        initial_next_player = self.game.next_player
        self.game.switch_players()
        self.assertEqual(self.game.current_player, initial_next_player)
        self.assertEqual(self.game.next_player, initial_current_player)

    def test_is_game_over(self):
        """Test the game over condition."""
        # Setting up a scenario where player2 is isolated
        for i in range(8):
            for j in range(6):
                self.game.board.set_cell_state(i, j, CellState.REMOVED)
        self.game.board.set_cell_state(7, 2, CellState.PLAYER_2)
        self.game.current_player = self.player1
        self.game.next_player = self.player2
        self.assertTrue(self.game.is_game_over())


if __name__ == "__main__":
    unittest.main()
