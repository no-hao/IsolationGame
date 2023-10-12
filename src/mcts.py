from .board import Board
from .player import ComputerPlayer
from random import choice
import math

class MCTSNode:
    def __init__(self, board: Board, move: tuple = None, parent=None):
        self.board = board
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def add_child(self, child_node):
        """Add a child node to the current node."""
        self.children.append(child_node)

    def is_fully_expanded(self):
        """Check if all possible moves have been explored."""
        return len(self.children) == len(self.board.get_possible_moves())

    def best_child(self, exploration_weight=1.4):
        """Return the best child node, using the UCT formula."""
        return max(self.children, key=lambda child: child.wins / child.visits + exploration_weight * math.sqrt(2 * math.log(self.visits) / child.visits))

    def rollout(self, player):
        """Simulate a random game from this node."""
        rollout_board = self.board
        while not rollout_board.is_game_over():
            possible_moves = rollout_board.get_possible_moves()
            move = choice(possible_moves)
            rollout_board = rollout_board.simulate_move(move)
        # Return 1 if the AI player wins, -1 if the opponent wins, 0 otherwise (draw)
        return 1 if rollout_board.winner() == player else -1

class MCTS:
    def __init__(self, exploration_weight=1.4):
        self.exploration_weight = exploration_weight

    def search(self, initial_board: Board, player: ComputerPlayer, iterations: int = 1000):
        root = MCTSNode(initial_board)

        for _ in range(iterations):
            node = self._select_node(root)
            if not node.board.is_game_over():
                node = self._expand(node)
                reward = self._simulate(node, player)
                self._backpropagate(node, reward)

        return root.best_child(self.exploration_weight).move

    def _select_node(self, node: MCTSNode):
        """Select a node in the tree to expand."""
        while not node.is_fully_expanded():
            node = node.best_child(self.exploration_weight)
        return node

    def _expand(self, node: MCTSNode):
        """Expand a node by adding a new child node."""
        possible_moves = node.board.get_possible_moves()
        move = choice(possible_moves)
        child_board = node.board.simulate_move(move)
        child_node = MCTSNode(child_board, move, node)
        node.add_child(child_node)
        return child_node

    def _simulate(self, node: MCTSNode, player: ComputerPlayer):
        """Simulate a game from the node's current board state."""
        return node.rollout(player)

    def _backpropagate(self, node: MCTSNode, reward: int):
        """Update nodes with the result of the simulation."""
        while node is not None:
            node.visits += 1
            node.wins += reward
            node = node.parent

