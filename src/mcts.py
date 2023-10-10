import random


class MCTS:
    def __init__(self, root, heuristic=None, exploration_constant=1.4, max_depth=None):
        """
        Initialize the Monte Carlo Tree Search algorithm.

        :param root: The root node of the search tree.
        :param heuristic: A heuristic function to guide the search.
        :param exploration_constant: A constant to balance exploration vs exploitation.
        :param max_depth: The maximum depth for simulations.
        """
        self.root = MCTSNode(root)
        self.heuristic = heuristic
        self.C = exploration_constant
        self.max_depth = max_depth

    def ucb(self, node):
        """
        Calculate the Upper Confidence Bound (UCB) for a node to determine 
        how promising a node is.

        :param node: The node for which UCB is being calculated.
        :return: The UCB value for the node.
        """
        if node.visits == 0:
            return float('inf')
        return node.average_reward + self.C * (node.parent.visits ** 0.5 / (1 + node.visits))

    def select(self, node):
        """
        Traverse the tree by selecting the child node with the highest UCB 
        until a leaf node or a node with unexplored children is found.

        :param node: The node from which to start selection.
        :return: The selected node.
        """
        while node.children and not node.unexplored_moves:
            node = max(node.children, key=self.ucb)
        return node

    def expand(self, node):
        """
        Expand the tree by creating a child node for a randomly chosen 
        unexplored move.

        :param node: The node to be expanded.
        :return: The newly created child node.
        """
        move = random.choice(node.unexplored_moves)
        child_state = node.game_state.make_move(move)
        child_node = MCTSNode(child_state, parent=node)
        node.children.append(child_node)
        return child_node

    def simulate(self, node):
        """
        Simulate a game from the given node to a terminal state. 
        If a heuristic is provided, it's used to guide the simulation.

        :param node: The starting node for the simulation.
        :return: The result of the simulation (win or loss).
        """
        current_state = node.game_state
        depth = 0
        while not current_state.is_terminal() and (self.max_depth is None or depth < self.max_depth):
            if self.heuristic:
                move = self.heuristic(current_state)
            else:
                move = random.choice(current_state.possible_moves())
            current_state = current_state.make_move(move)
            depth += 1
        return current_state.result()

    def backpropagate(self, node, reward):
        """
        Update the given node and its ancestors with the result of the simulation.

        :param node: The node from which backpropagation begins.
        :param reward: The result of the simulation to backpropagate.
        """
        while node:
            node.visits += 1
            node.value += reward
            node = node.parent

    def best_child(self, node):
        """
        Return the child node of the given node with the highest average reward.

        :param node: The parent node.
        :return: The best child node.
        """
        return max(node.children, key=lambda child: child.average_reward)

    def search(self, iterations):
        """
        Perform the MCTS algorithm for a specified number of iterations.

        :param iterations: The number of iterations to run the MCTS.
        :return: The game state of the best child node after the search.
        """
        for _ in range(iterations):
            selected_node = self.select(self.root)
            if not selected_node.game_state.is_terminal():
                expanded_node = self.expand(selected_node)
                reward = self.simulate(expanded_node)
                self.backpropagate(expanded_node, reward)
        best_child_node = self.best_child(self.root)
        
        # Prune unused nodes to free up memory
        self.root.children = [best_child_node]
        
        return best_child_node.game_state
