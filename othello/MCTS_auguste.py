
from math import *
from copy import deepcopy, copy

class node():

    def __init__(self, board = None, move : tuple = None, parent = None):
        """
        parent = previous node
        """
        self.win = 0 # Nbr of win passed by the node
        self.board = board
        self.n = 1 # Nbr of simulation passed by the node
        self.move = move # Move that generated the child
        self.parent = parent
        self.child = []


class MCTS():

    def __init__(self, game, c : int = 0.1416, threshold : int = 30, iteration : int = 50) -> None:
        self.game = game
        self.c = c
        self.threshold = threshold
        self.iteration = iteration
        self.init = node() # First node
        self.Bchild = None
        self.selection(game, self.init, 1)
        # print(child.board)
        # print(self.Bchild.board)

    def generatechild(self, game, parent):
        """
        Generate all possible child for none terminal node
        """
        for move in  game.moves :
            child = node(move = move, parent = parent)
            parent.child.append(child)

    def selectionchild(self, parent):
        """
        Return the child with the highest value selection
        """
        Bvalue = 0
        Bchild = parent.child[0]
        for child in parent.child :
            value_child = (child.win / child.n) + self.c * sqrt(log(parent.n)/child.n)
            if Bvalue < value_child :
                value_child = Bvalue
                Bchild = child
        return Bchild

    def selection(self, game, parent, threshold : int = 30):
        """
        Store in Bchild the child that will be use for expansion
        """
        if game.moves != [] : # if it is not the end of the game
            # Case where we reach the limit
            if threshold == 0 :
                if parent.child == []:
                    self.generatechild(game, parent)
                Bchild = self.selectionchild(parent) # get the child that will be used for Expansion
                game.play_one_turn(Bchild.move[0], Bchild.move[1])
                fliped = game.game.fliped
                side = game.side
                Bchild.board = copy(game.game.board) # Will maybe need deepcopy
                game.side = game.game.unmake_move(fliped, Bchild.move[0], Bchild.move[1], side)
                self.Bchild = Bchild

            # Case Where there is no childs
            elif parent.child == [] and threshold > 0:
                self.generatechild(game, parent)
                Bchild = self.selection(game, parent, threshold) # recursion on selection
            
            # Case where we travel the tree
            else :
                child = self.selectionchild(parent) # get the child that will be used for next selection
                game.play_one_turn(child.move[0], child.move[1]) # Play the first move
                fliped = game.game.fliped
                side = game.side  
                Bchild = self.selection(game, child, threshold - 1) # recursion on selection
                game.side = game.game.unmake_move(fliped,child.move[0], child.move[1], side)
        # Case where the end of the game is reach before the reaching the fronter
        else :
            return parent
