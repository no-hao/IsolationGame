from unittest import TestCase, mock
from src.board import Board, CellState
from src.player import HumanPlayer, ComputerPlayer


class TestPlayer(TestCase):

    def setUp(self):
        self.board = Board()
        self.human_player = HumanPlayer()
        self.computer_player = ComputerPlayer()

    def test_player_initialization(self):
        """Test if the player initializes correctly."""
        self.assertEqual(self.human_player.name, "Human")
        self.assertEqual(self.human_player.type, "Human")
        self.assertIsNone(self.human_player.position)

    def test_valid_moves(self):
        """Test valid moves for the player."""
        self.human_player.position = (4, 3)
        # Test a valid move
        self.assertEqual(self.human_player.position, (4, 3))
        self.assertTrue(self.human_player._is_valid_move(5, 3, self.board))
        # Test moving to an occupied cell
        self.assertFalse(self.human_player._is_valid_move(0, 3, self.board))
        # Test moving outside the board boundaries
        self.assertFalse(self.human_player._is_valid_move(8, 3, self.board))

    def test_token_removal(self):
        """Test valid token removal for the player."""
        # Test a valid token removal
        self.assertTrue(self.human_player._is_valid_removal(5, 3, self.board))
        # Test removing token from a cell occupied by a player
        self.assertFalse(self.human_player._is_valid_removal(0, 3, self.board))
        # Test removing token outside the board boundaries
        self.assertFalse(self.human_player._is_valid_removal(8, 3, self.board))

    def test_boundary_movements(self):
        """Test moving to all edge cells from an edge cell."""
        self.human_player.position = (0, 0)
        self.assertTrue(self.human_player._is_valid_move(0, 1, self.board))
        self.assertTrue(self.human_player._is_valid_move(1, 0, self.board))
        self.assertTrue(self.human_player._is_valid_move(1, 1, self.board))
        self.assertFalse(self.human_player._is_valid_move(-1, 0, self.board))
        self.assertFalse(self.human_player._is_valid_move(0, -1, self.board))

    def test_same_cell_movement(self):
        """Test that a player cannot remain in the same cell."""
        self.human_player.position = (4, 3)
        self.assertFalse(self.human_player._is_valid_move(4, 3, self.board))

    def test_invalid_input_handling(self):
        """Test handling of invalid inputs."""
        # This test might need more implementation in the player or board classes 
        # to handle and catch invalid inputs gracefully
        pass

    def test_full_board_movement(self):
        """Test movement when almost all cells are filled."""
        # Fill the board, leaving only cells around (4, 3) empty
        for i in range(8):
            for j in range(6):
                self.board.set_cell_state(i, j, CellState.REMOVED)
        self.board.set_cell_state(4, 3, CellState.PLAYER_1)
        self.human_player.position = (4, 3)
        self.assertFalse(self.human_player._is_valid_move(5, 3, self.board))
        self.board.set_cell_state(5, 3, CellState.EMPTY)
        self.assertTrue(self.human_player._is_valid_move(5, 3, self.board))
        self.board.set_cell_state(5, 3, CellState.PLAYER_1)
        self.human_player.position = (5, 3)
        self.assertFalse(self.human_player._is_valid_move(4, 3, self.board))
        self.board.set_cell_state(4, 3, CellState.EMPTY)
        self.assertTrue(self.human_player._is_valid_move(4, 3, self.board))
        # Add more assertions as needed to validate possible and impossible moves

    def test_token_removal_restrictions(self):
        """Test token removal restrictions."""
        self.human_player.position = (4, 3)
        self.board.set_cell_state(4, 3, CellState.PLAYER_1)
        self.assertFalse(self.human_player._is_valid_removal(4, 3, self.board))
        self.board.set_cell_state(5, 3, CellState.PLAYER_1)
        self.assertFalse(self.human_player._is_valid_removal(5, 3, self.board))
        self.board.set_cell_state(5, 3, CellState.REMOVED)

    def test_endgame_scenario(self):
        """Test scenarios where one player cannot move."""
        # Fill the board except for the player's position
        for i in range(8):
            for j in range(6):
                self.board.set_cell_state(i, j, CellState.REMOVED)
        self.board.set_cell_state(4, 3, CellState.PLAYER_1)
        self.human_player.position = (4, 3)
        self.assertFalse(self.human_player._is_valid_move(5, 3, self.board))
        # Add more assertions to validate that the game recognizes endgame situations

    # Mocking user input for the HumanPlayer's move method
    @mock.patch('builtins.input', side_effect=["5 3", "4 4"])
    def test_human_player_move(self, mock_input):
        """Test the move method of the HumanPlayer class."""
        self.human_player.position = (4, 3)
        self.human_player.move(self.board)
        self.assertEqual(self.human_player.position, (5, 3))

    # Mocking user input for the HumanPlayer's move method
    @mock.patch('builtins.input', side_effect=["5 3", "4 4"])
    def test_human_player_move(self, mock_input):
        """Test the move method of the HumanPlayer class."""
        self.human_player.position = (4, 3)
        self.human_player.move(self.board)
        self.assertEqual(self.human_player.position, (5, 3))

    # Mocking user input for the HumanPlayer's remove_token method
    @mock.patch('builtins.input', side_effect=["5 3", "4 4"])
    def test_human_player_remove_token(self, mock_input):
        """Test the remove_token method of the HumanPlayer class."""
        self.human_player.remove_token(self.board)
        # No state change happens in this test, so we just verify the method runs correctly
