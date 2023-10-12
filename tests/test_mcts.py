import unittest
from src.game import Game
from src.mcts import MCTS, MCTSNode
from src.board import Board, CellState
from src.player import ComputerPlayer, PlayerFactory, Heuristics

class TestMCTS(unittest.TestCase):

    # Initialization Tests
    def test_mcts_node_initialization(self):
        board = Board()
        node = MCTSNode(board)
        self.assertEqual(node.board, board)
        self.assertEqual(node.move, None)
        self.assertEqual(node.parent, None)
        self.assertEqual(node.children, [])
        self.assertEqual(node.wins, 0)
        self.assertEqual(node.visits, 0)

    def test_mcts_initialization(self):
        game = Game(PlayerFactory.create_player("Human", "Player1"), PlayerFactory.create_player("Computer", "Player2"))
        board = game.board
        mcts = MCTS(game, board, heuristic=Heuristics.mobility)
        self.assertEqual(mcts.game, game)
        self.assertEqual(mcts.board, board)
        self.assertEqual(mcts.heuristic, Heuristics.mobility)

    # Functional Tests
    def test_node_expansion(self):
        board = Board()
        root = MCTSNode(board)
        child_board = board  # Simulate a move on the board to get child_board
        child_node = MCTSNode(child_board, move=(0, 0), parent=root)
        root.add_child(child_node)
        self.assertIn(child_node, root.children)

    def test_mcts_simulation(self):
        game = Game(PlayerFactory.create_player("Human", "Player1"), PlayerFactory.create_player("Computer", "Player2"))
        board = game.board
        mcts = MCTS(game, board, heuristic=Heuristics.mobility)
        root = MCTSNode(board)
        reward = mcts._simulate(root)
        self.assertIn(reward, [1, -1])  # Assuming only two outcomes: win or lose

    # ... add more functional tests ...

    # Integration Tests
    def test_mcts_search(self):
        game = Game(PlayerFactory.create_player("Human", "Player1"), PlayerFactory.create_player("Computer", "Player2"))
        board = game.board
        mcts = MCTS(game, board, heuristic=Heuristics.mobility)
        move = mcts.search()
        self.assertIsInstance(move, tuple)

    # ... add more integration tests ...

if __name__ == "__main__":
    unittest.main()
