from othello import Othello
from time import sleep
from copy import deepcopy, copy
from time import time
from run import simulation
from math import *
import random
import numpy as np


class RandomPlayer():
    """
    Random player will get a random move from the valid moves list
    """
    
    def __init__(self) :
        self.auto = True # Inform about that it is a automatic player

    def pick_move(self, game) -> list:
        r = random.randint(0, len(game.moves)-1)
        return (game.moves[r][0], game.moves[r][1])
    
class HumanPlayer(): 
    """
    Human player will get the choice of the user thank to a click.
    It will check if this click is in the legal move before otherwise it return an impossible position (-1, -1)
    """
    
    def __init__(self) :
        self.auto = False # Inform that it is not a automatic player

    def move_from_tkinter(self, game : object, side : int, event : enumerate, size : int) -> list:
        t = game.possible_moves(side)
        if len(t) == 0:
            return (-1, -1)
        y = floor(event.x / size)
        x = floor(event.y / size)
        if (x, y) in t :
            return (x, y)
        return (-1, -1)
            
class dummy_evaluation_player():
    """
    Take a game an evaluate a ratio :
    ratio = gain / risk
    Thanks to a density map provided during the course
    we will go through the border and each square accessible from an enemy piece will be a potential gain,
    conversely any square of the considered player will be a potential risk.
    Gain = P(last move) + Sum(P(player_opportunity_on_border)i)
    Risk = Sum(P(ennemy_opportunity_on_border)i)

    Better than random [80-90]%
    """
    def __init__(self, depth = 1):
        self.depth = depth
        self.auto = True

    def pick_move(self, game) -> list :
        self.density_map = np.array([[120,-20,20,5,5,20,-20,120],
                       [-20,-30,-5,-5,-5,-5,-30,-20],
                       [20 ,-5 ,15,3,3,15,-5,20],
                       [5  ,-5 ,3,3,3,3,-5,5],
                       [5  ,-5 ,3,3,3,3,-5,5],
                       [20 ,-5 ,15,3,3,15,-5,20],
                       [-20,-30,-5,-5,-5,-5,-30,-20],
                       [120,-20,20,5,5,20,-20,120]])
        ret = -10000
        for move in game.moves:
            new_game = simulation(deepcopy(game.players[0]),deepcopy(game.players[1]), deepcopy(game.game.board), game.side)
            new_game.play_one_turn(move[0], move[1])
            ratio = self.evaluation_board(new_game, move[0], move[1])
            if ratio > ret :
                ret = ratio
                ret_move = move
        return ret_move

    def evaluation_board(self, game, x : int, y : int) -> int :
        gain = self.density_map[x,y] * 2
        risk = 0
        for i in range(7):
            for j in range(7):
                if game.game.board[i,j] == -game.side:
                    risk += max(self.check_neighborhood(game, i, j))
                elif game.game.board[i,j] == game.side :
                    gain += max(self.check_neighborhood(game, i, j))
        if risk == 0 :
            return (gain/1)
        elif gain < 0:
            return (-1000)
        elif risk < 0 and gain > 0:
            return ((gain / -(1/risk)))
        return ((gain/risk))

    def check_neighborhood(self, game, i : int, j : int) -> None:
        tot = [0]
        for dx in range(i-1,i+2):
            for dy in range(j-1,j+2):
                if game.game.board[dx,dy] == 0:
                    tot.append(self.density_map[dx,dy])
        return tot  

        
class DensityMinMax():
    """
    Logic min_max algorithme with a density map as an evaluation function.
    Better than random but weak against dummy_evaluation.
    Maybe be increasing depth it could win but the evaluation function doesn't seem good
    """

    def __init__(self, depth : int = 2) -> None:
        self.depth = depth    
        self.auto = True

    def pick_move(self, game) -> tuple :
        gain, move = self.minmax(game, self.depth, game.side)
        return move

    def minmax(self, game, depth : int , maximizingplayer  : int, x : int = -1, y : int = -1) -> tuple :
        if depth == 0 or game.moves == [] :
            return self.evaluation_function(game, maximizingplayer, x, y), (-1, -1)
        
        if game.side == maximizingplayer :
            value = 100000
            Bmove = (-1,-1)   
            for move in game.moves :
                new_game = simulation(game.players[0],game.players[1], deepcopy(game.game.board), game.side)
                new_game.play_one_turn(move[0], move[1])
                yMM = self.minmax(new_game, depth-1, maximizingplayer, move[0], move[1])
                gain, _ = yMM[0], yMM[1]
                if gain < value :
                    value = gain
                    Bmove = move
        else :
            value = -10000000
            Bmove = (-1,-1)   
            for move in game.moves :
                new_game = simulation(game.players[0],game.players[1], deepcopy(game.game.board), game.side)
                new_game.play_one_turn(move[0], move[1])
                yMM = self.minmax(new_game, depth-1, maximizingplayer, move[0], move[1])
                gain, _ = yMM[0], yMM[1]
                if gain > value :
                    value = gain
                    Bmove = move
        
        return value, Bmove

    
    def check_neighborhood(self, game, i : int, j : int) -> int:
        tot = [0]
        for dx in range(i-1,i+2):
            for dy in range(j-1,j+2):
                if game.game.board[dx,dy] == 0:
                    tot.append(self.density_map[dx,dy])
        return tot               

    def evaluation_function(self, game, maximizingplayer, x = -1, y = -1):
        self.density_map = np.array([[120,-20,20,5,5,20,-20,120],
                       [-20,-30,-5,-5,-5,-5,-30,-20],
                       [20 ,-5 ,15,3,3,15,-5,20],
                       [5  ,-5 ,3,3,3,3,-5,5],
                       [5  ,-5 ,3,3,3,3,-5,5],
                       [20 ,-5 ,15,3,3,15,-5,20],
                       [-20,-30,-5,-5,-5,-5,-30,-20],
                       [120,-20,20,5,5,20,-20,120]])
        risk = 0 
        gain = 0
        for i in range(7):
            for j in range(7):
                if game.game.board[i,j] == -maximizingplayer:
                    risk += max(self.check_neighborhood(game, i, j))
                    # gain += self.density_map[i,j]
                elif game.game.board[i,j] == maximizingplayer :
                    gain += max(self.check_neighborhood(game, i, j))
                    # risk += self.density_map[i,j]
        if risk == 0 :
            return (100)
        elif risk < 0 and gain < 0:
            return ((gain/risk))
        elif risk < 0 and gain > 0:
            return ((gain / -(1/risk)))
        return ((gain/risk))