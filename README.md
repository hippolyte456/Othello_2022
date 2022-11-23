# Othello IODAA

## Contributors

Project of the Master IODAA - AgroParisTech & University Paris-Saclay realized by : <br>
* <a href="https://github.com/hippolyte456" target="_blank">Hippolyte Dreyfus </a> <br>
* <a href="https://github.com/Aaramis" target="_blank">Auguste Gardette </a> <br>

## Presentation

### Objectif 

The objective is to recode a complete othello game and to design algorithms to solve it

### Othello History

Othello belongs to the class of strategy games with two players, with complete information (the players know at each moment the totality of the information on the position they have to play) and with zero sum (at the end of the game, the totality of the stake, i.e. 64 pawns, is distributed entirely between the players).

Othello on 4×4 and 6×6 board  are strongly solved and proved as a second player (white) to win. For 8x8 boards, Victor Allis estimated the number of legal positions in Othello is at most 10^28, and it has a game-tree complexity of approximately 10^58. While still mathematically unsolved, there is strong suspicion that perfect play on both sides results in a draw.
[Wiki](https://www.chessprogramming.org/Othello)


## Algorithms

To solve this othello, we will try to implement the following algorithms :

### MinMax

The general method is the following: from a position (root of the tree) we generate all possible moves for the program. Then from these new positions (level 1) we generate all the possible answers for the opponent (level 2). We can then repeat the operation as long as the computer's computing power allows and generate levels 3, 4, ..., n.

The branching factor in a balanced Othello game being about 10 and the number of moves about 60, one cannot generate, in a limited time, the whole tree. We must therefore limit the depth of the procedure. Once this depth is reached, the leaves (as opposed to the root) of the tree thus constructed are evaluated by an evaluation function. The program can, starting from the root, play the move of level 1 that guarantees the maximum gain against any defense of its opponent, assuming that the latter also uses an optimal strategy, i.e. that it plays itself at each move the gain that guarantees the maximum gain against any defense. This mechanism is called the Minimax principle.
[Wiki](https://en.wikipedia.org/wiki/Minimax)

### Alpha-Beta

The minimax algorithm performs a complete exploration of the search tree up to a given level. The alpha-beta pruning allows to greatly optimize the minimax algorithm without changing the result. To do so, it performs only a partial exploration of the tree. During the exploration, it is not necessary to examine the sub-trees that lead to configurations whose value will not contribute to the calculation of the gain at the root of the tree. Put another way, pruning αβ does not evaluate nodes that, if the evaluation function is approximately correct, can be expected to be of lower quality than an already evaluated node. 
[Wiki](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)

### MCTS : Monte Carlo tree search

The MCTS algorithm is an algorithm that explores the tree of possibilities. The root is the initial configuration of the game. Each node is a configuration and its children are the following configurations. MCTS keeps a tree in memory that corresponds to the already explored nodes of the possibility tree. A leaf of this tree (a node with no children) is either a final configuration (i.e. we know if one of the players has won, or if there is a draw), or a node whose children have not yet been explored. In each node, we store two numbers: the number of winning simulations, and the total number of simulations. Each step consists of four phases.

* Selection. From the root, we successively select children until we reach a leaf. In this phase, the choice of children is guided by a trade-off between exploitation (going to a child that has been proven to be promising) and exploration (going to another child, who looks less promising but might be more promising). 
* Expansion: if this sheet is not final, create a child (or children) using the rules of the game and choose one of the children. 
* Simulation: simulate a random execution of a game from this child, until reaching a final configuration.
* Backpropagation: use the result of the random game and update the information about the branch from the child node to the root.
[Wiki](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)

###

## Execution

The work is in progress, the algorithms are not yet finished but it is already possible to have a view of the project.

```bash
python3 othello/run.py 
```

For the Graphical User Interfaces (GUIs) we used Tkinter.