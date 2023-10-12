import math
from .game import Game
from random import choice
from .board import Board, CellState


class MCTSNode:
    def __init__(self, game: Game, move: tuple = None, parent=None):
        self.game = game
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def add_child(self, child_node):
        self.children.append(child_node)

    def is_fully_expanded(self):
        return len(self.children) == len(self.game.board.get_possible_moves())

    def best_child(self, exploration_weight=1.4):
        return max(self.children, key=lambda child: child.wins / child.visits + exploration_weight * math.sqrt(2 * math.log(self.visits) / child.visits))


class MCTS:
    def __init__(self, game: Game, heuristic=None):
        self.game = game
        self.heuristic = heuristic or (lambda board: 0)  # Default to a no-op heuristic if none provided

    def search(self, iterations: int = 1000):
        root = MCTSNode(self.game)

        for _ in range(iterations):
            node = self._select_node(root)
            if not node.game.is_game_over():
                node = self._expand(node)
                reward = self._simulate(node)
                self._backpropagate(node, reward)

        return root.best_child().move

    def _select_node(self, node: MCTSNode):
        while not node.is_fully_expanded():
            node = node.best_child()  # Use the heuristic to guide the selection
        return node

    def _expand(self, node: MCTSNode):
        possible_moves = node.game.board.get_possible_moves()
        move = choice(possible_moves)
        child_game = deepcopy(node.game)
        child_game.make_move(*move)
        child_node = MCTSNode(child_game, move, node)
        node.add_child(child_node)
        return child_node

    def _simulate(self, node: MCTSNode):
        simulated_game = deepcopy(node.game)
        
        while not simulated_game.is_game_over():
            possible_moves = simulated_game.board.get_possible_moves()
            if not possible_moves:
                break
            move = choice(possible_moves)
            simulated_game.make_move(*move)

        return 1 if simulated_game.winner() == "Computer" else -1

    def _backpropagate(self, node: MCTSNode, reward: int):
        while node is not None:
            node.visits += 1
            node.wins += reward
            node = node.parent
