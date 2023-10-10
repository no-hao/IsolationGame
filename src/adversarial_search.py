class AdversarialSearch:
    def __init__(self, heuristic_strategy):
        self.heuristic_strategy = heuristic_strategy

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        # Implementation will be added later
        pass

    def best_move(self, board, player):
        # Implementation will be added later
        pass


class MCTS:
    def __init__(self, root, heuristic=None, exploration_constant=1.4):
        self.root = MCTSNode(root)
        self.heuristic = heuristic
        self.C = exploration_constant  # exploration vs exploitation balance

    def ucb(self, node):
        """
        Calculate the Upper Confidence Bound (UCB) for a node.
        """
        if node.visits == 0:
            return float('inf')
        return node.average_reward + self.C * (node.parent.visits ** 0.5 / (1 + node.visits))

    def select(self, node):
        """
        Traverse the tree to select a node using UCB.
        """
        while node.children and not node.unexplored_moves:
            node = max(node.children, key=self.ucb)
        return node

    def expand(self, node):
        """
        Expand the node by adding one child for an unexplored move.
        """
        move = random.choice(node.unexplored_moves)
        # Assuming game_state has a method called make_move which returns a new state
        child_state = node.game_state.make_move(move)
        child_node = MCTSNode(child_state, parent=node)
        node.children.append(child_node)
        return child_node

    def simulate(self, node):
        """
        Simulate the game from the node to a terminal state.
        If a heuristic is provided, use it to guide the moves.
        """
        current_state = node.game_state
        # Assuming game_state has methods is_terminal (checks if game is over) and result (returns 1 for win, 0 for loss)
        while not current_state.is_terminal():
            if self.heuristic:
                move = self.heuristic(current_state)
            else:
                move = random.choice(current_state.possible_moves())
            current_state = current_state.make_move(move)
        return current_state.result()

    def backpropagate(self, node, reward):
        """
        Update the node and its ancestors with the simulation result.
        """
        while node:
            node.visits += 1
            node.value += reward
            node = node.parent

    def best_child(self, node):
        """
        Return the child with the highest average reward.
        """
        return max(node.children, key=lambda child: child.average_reward)

    def search(self, iterations):
        """
        Perform MCTS for a specified number of iterations.
        Return the best move found.
        """
        for _ in range(iterations):
            selected_node = self.select(self.root)
            if not selected_node.game_state.is_terminal():
                expanded_node = self.expand(selected_node)
                reward = self.simulate(expanded_node)
                self.backpropagate(expanded_node, reward)
        return self.best_child(self.root).game_state

