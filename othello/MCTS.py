
from math import *
from copy import deepcopy, copy
from random import choice
import run
import minmax
import numpy as np
import othello

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


class MCTS():

    def __init__(self, game : None, c : int = 0.1416, threshold : int = 30, iteration : int = 50) -> None:
        self.auto = True
        # self.player = game.side
        self.c = c
        self.threshold = threshold
        self.iteration = iteration
        self.first_node = node() # First node
        self.init = self.first_node
        self.Bchild = None
    
    def pick_move(self, game, c : int = 0.1416, threshold : int = 30, iteration : int = 100) -> tuple :
        if game.moves == [] :
            self.init = node()
            self.Bchild = None
        if self.init.move != None :
            if game.game.board[self.init.move[0], self.init.move[1]] == 0 :
                self.init = node()
                self.Bchild = None           
        self.find_node(game, self.init)
        self.init.n += 1
        self.game = run.simulation(game.players[0], game.players[1], deepcopy(game.game.board), game.side)
        self.player = game.side
        while (iteration > 0 ) :
            self.Bchild = None
            self.selection(self.game, self.init, self.threshold)
            if (self.Bchild != None) : # If we are at the last turn, we don't need the simulation
                self.simulation(self.Bchild)
            iteration -= 1
        return_child = self.selectionchild(self.init)
        self.init = return_child # We Will start the next MCTS search from the last move (keep in memory the previous searches)
        # if(np.sum(np.where((game.game.board == 0), 1,0))) <= 1 : # Pointless ?
        #     self.init = node()
        return return_child.move
    
    def find_node(self, game, init) -> bool:
        """
        Find where we are in the tree after the move from the ennemy
        """
        # Depth 1
        for node in init.child :
            if game.game.board[node.move[0], node.move[1]] != 0:
                self.init = node
        # Depth 2
        for node in init.child :
            for node2 in node.child :
                if game.game.board[node2.move[0], node2.move[1]] != 0:
                    self.init = node2
        # Maybe need to find a way to iterate for each Depth until it found the correct map

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
            if child.n == 0 : # Child no tried yet
                return child
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
                child.n += 1
                game.play_one_turn(child.move[0], child.move[1]) # Play the first move
                fliped = game.game.fliped
                side = game.side  
                Bchild = self.selection(game, child, threshold - 1) # recursion on selection
                game.side = game.game.unmake_move(fliped,child.move[0], child.move[1], side)
        # Case where the end of the game is reach before the reaching the fronter
        else :
            return parent
    

    def simulation(self, node):
        """
        Simulate random moves until end of game and backpropagation of the result
        """
        if (0 in node.board):
            side = node.board[node.move[0],node.move[1]]
            game = othello.Othello(node.board)
            moves = game.possible_moves(side)
            board = node.board   
            if moves != [] :
                result = run.simulation(minmax.RandomPlayer(), minmax.RandomPlayer(), board, side).play()
            else :
                result = np.sum(node.board)
        else :
            result = np.sum(node.board)
        if ((result > 0 and self.player == 1) or (result < 0 and self.player == -1)) :
            while (node != None):
                node.win += 1
                node = node.parent