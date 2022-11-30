
from math import *
from copy import deepcopy
import run
import minmax
import numpy as np

class node():

    def __init__(self, board = None, move : tuple = None, parent = None) -> None:
        """
        parent = previous node
        """
        self.win = 0 # Nbr of win passed by the node
        self.board = board # Copy of the board 
        self.n = 0 # Nbr of simulation passed by the node
        self.move = move # Move that generated the child
        self.parent = parent # Parent of the node
        self.child = [] # List that will store all chils
        self.side = 0
        self.moves = None

class MCTS():
    """
    Class for MCTS Algorithm
    """

    def __init__(self, game : object = None, c : int = 0.1416, threshold : int = 30, iteration : int = 100) -> None:
        """
        Init all the variable for MCTS
        """
        self.auto = True # Inform that it is an automatic player
        self.player = game.side # Will be use to know if the result of MCTS is a win or not
        self.c = c # Parameter of MCTS formula
        self.threshold = threshold
        self.iteration = iteration
        self.init = node(game.game.board) # Root
        self.init.side = game.side # Inform the root about the side
        self.Bchild = None 
    
    def pick_move(self, game : object) -> tuple :
        """
        Return the move to play according to MCTS algorithm
        """
        self.Is_New_Game(game) # Check if we want to start a new MCTS simulation
        self.Selection(game)                                        # 1. SELECTION
        self.init.n += 1 # Increment the starting position
        iteration = self.iteration
        while (iteration > 0 ) :
            self.Expansion(game, self.init, self.threshold)         # 2. EXPANSION
            result = self.Simulation(self.Bchild)                   # 3. SIMULATION
            self.Backpropagation(result , self.Bchild)              # 4. BACKPROPAGATION
            iteration -= 1
        if self.init.child != [] :                                  # 5. CHOICE
            return_child = self.selectionchild(self.init)
            self.init = return_child # Next MCTS will start from return_child
            self.init.parent = None # Don't need to keep in mind the previous tree
        return return_child.move


    def Selection(self, game : object) -> None :
        """
        Repositioning the root 
        If no node was found on the first try it means that the node is not present in our tree 
        (example: when a player plays more times in a row than the depth of the tree). 
        So we reinitialize the root to the actual state of the game and we start the MCTS
        """
        if self.init.child == [] :
            self.generatechild(self.init)
        if not self.find_node(game, self.init) :
            self.init = node(game.game.board)
            self.init.side = game.side
            self.Selection(game)

    def Is_New_Game(self, game : object) -> bool :
        """
        Check if the game provided in input is a new board.
        To do so, we are just checking if there is only 4 tokens on the board.
        If true, we reset the starting variables.
        """
        if np.count_nonzero(game.game.board) == 4 :
            self.init = node(game.game.board)
            self.init.side = game.side
            self.Bchild = None
            return True
        return False

    def find_node(self, game : object, node : object) -> bool:
        """
        Find where we are in the tree after the move from the ennemy
        """
        if np.array_equal(game.game.board, node.board) :
            self.init = node
            return True
        else :
            for child in node.child :
                if self.find_node(game, child) :
                    return True
        return False

    def generatechild(self, parent : object) -> None :
        """
        Generate all possible childs
        """
        game = run.simulation(board = parent.board, side = parent.side)
        for move in  game.moves :
            child = node(move = move, parent = parent) # Create a new node
            game.play_one_turn(child.move[0], child.move[1]) # Play the move
            child.side = game.side
            child.board = deepcopy(game.game.board) # Copy the board
            child.moves = game.moves # Store next possibles moves
            game.side = game.game.unmake_move(game.game.fliped ,child.move[0], child.move[1], game.side) # Undo move         
            parent.child.append(child) # Add node to parent's child

    def selectionchild(self, parent : object) -> object:
        """
        MCTS Formula
        Return the child with the highest value selection
        """
        Bvalue = 0
        Bchild = parent.child[0]
        for child in parent.child :
            if child.n == 0 : # Child not tried yet
                return child
            value_child = (child.win / child.n) + self.c * sqrt(log(parent.n)/child.n)
            if Bvalue < value_child :
                Bvalue = value_child
                Bchild = child
        return Bchild

    def Expansion(self, game : object, parent, threshold : int = 30):
        """
        Store in Bchild the child that will be use for simulation
        """
        # Final Node or end of game
        if parent.moves == [] or threshold == 0:
            self.Bchild = parent
            return
        
        # EXPANSION
        if parent.child == []:
            self.generatechild(parent)
        
        # EXPLOTATION
        if parent.child != []:
            child = self.selectionchild(parent) # get the child that will be used for next selection
            child.n += 1
            self.Expansion(game, child, threshold - 1) # recursion on selection

    def Simulation(self, node: object) -> int:
        """
        Simulate random moves until end of game and backpropagation of the result
        """
        board = deepcopy(node.board)
        side = -node.board[node.move[0],node.move[1]] # Side = - last move value
        othello = run.simulation(minmax.RandomPlayer(), minmax.RandomPlayer(), board, side)
        if othello.moves != [] :
            result = othello.play()
        else :
            result = np.sum(othello.game.board)
        return result
        

    def Backpropagation(self, result : int, node : object) -> None :
        """
        Backprogragation step of MCTS
        Traces back to the root by informing if it is a win
        """
        if ((result > 0 and self.player == 1) or (result < 0 and self.player == -1)) :
            while (node != None):
                node.win += 1
                node = node.parent