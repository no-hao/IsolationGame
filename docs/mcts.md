# Monte Carlo Tree Search (MCTS)

## Overview

Monte Carlo Tree Search (MCTS) is an algorithm used for making optimal decisions in complex domains like games. It's particularly useful for games with high branching factors, such as Isolation.

## How MCTS Works

### 1. Selection
Starting from the root node (current game state), the algorithm recursively selects the most promising child node until it reaches a leaf node.

### 2. Expansion
If the leaf node isn't a terminal state (end of the game), create one or more child nodes and select one.

### 3. Simulation (Rollout)
Perform a random simulation from this node to a game end. This involves making random moves for both players until the game ends.

### 4. Backpropagation
After the game ends, backpropagate the result from the leaf node to the root node, updating the scores and visit counts of each node along the way.

### 5. Best Move
After a certain number of simulations or a set period, the child of the root with the highest score or the most visits is chosen as the best move.

## Integrating Heuristics with MCTS

While classic MCTS relies on random simulations, integrating heuristics can guide the search more effectively:

### 1. Guided Rollouts
Instead of making entirely random moves during the simulation phase, use heuristics to guide the move choices, making the simulations more representative of "reasonable" play.

### 2. Node Evaluation
When expanding a node, use heuristics to prioritize which moves to consider first.

### 3. Pruning
Use heuristics to avoid exploring obviously bad moves.

## Benefits of MCTS for Isolation

- **Handles High Branching Factor**: MCTS doesn't try to evaluate all possible moves. Instead, it focuses on the most promising ones, making it suitable for Isolation.
  
- **Anytime Algorithm**: MCTS can be stopped at any time to provide the best move found so far. This is useful if you want to set a time limit on move calculations.
  
- **Adaptable**: MCTS can easily integrate heuristics, and as more simulations are run, its decisions tend to improve.

## Implementation Details

### 1. MCTS Node Structure

- **Game state**: Represents the board configuration at this node.
  
- **Parent**: A reference to the parent node.
  
- **Children**: A list of child nodes.
  
- **Number of visits**: The number of times this node has been visited during the search.
  
- **Average reward**: The average reward obtained from simulations that passed through this node.

### 2. MCTS Class

- **Root**: The root of the search tree, representing the current game state.
  
- **Exploration constant**: A parameter that balances exploration and exploitation.
  
- **Heuristic**: The heuristic function to guide rollouts and evaluate nodes.

### 3. MCTS Methods

- **Selection**: Traverse the tree from the root to a leaf using the Upper Confidence Bound (UCB) formula.
  
- **Expansion**: Expand a leaf node by adding one or more children.
  
- **Simulation (Rollout)**: Simulate the game from a node to a terminal state using random or heuristic-guided moves.
  
- **Backpropagation**: Backpropagate the result of a simulation to update the nodes from the leaf to the root.
