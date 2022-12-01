from copy import deepcopy, copy
from run import simulation
from math import *
from random import choice
import numpy as np
import evaluation


class RandomPlayer():
    """
    Random player will get a random move from the valid moves list
    """
    
    def __init__(self) :
        self.auto = True # Inform about that it is a automatic player
        self.name = "Random"

    def pick_move(self, game) -> list:
        # print(game.game.board)
        move = choice(game.moves)
        return (move[0], move[1])
    
class HumanPlayer(): 
    """
    Human player will get the choice of the user thank to a click.
    It will check if this click is in the legal move before otherwise it return an impossible position (-1, -1)
    """
    
    def __init__(self) :
        self.auto = False # Inform that it is not a automatic player
        self.name = "Human"

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
        self.name = "Dummy"

    def pick_move(self, game) -> list :
        self.density_map = np.array([[120, -20, 20, 5 , 5,20,-20,120],
                                     [-20, -30, -5, -5, -5,-5,-30,-20],
                                     [20 , -5 , 15, 3 , 3,15,-5,20],
                                     [5  , -5 , 3 , 3 , 3,3,-5,5],
                                     [5  , -5 , 3 , 3 , 3,3,-5,5],
                                     [20 , -5 , 15, 3 , 3,15,-5,20],
                                     [-20, -30, -5, -5, -5,-5,-30,-20],
                                     [120, -20, 20, 5 , 5,20,-20,120]])
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

        
class MinMax():
    """
    heuristics take into account the mobility, coin parity, stability and corners-captured
    Not good against random but pretty good against density, dummy function is still better ...
    """

    def __init__(self, depth : int = 2) -> None:
        self.depth = depth    
        self.auto = True
        self.name = "MinMax"

    def pick_move(self, game : object) -> tuple :
        newgame = simulation(game.players[0],game.players[1], deepcopy(game.game.board), deepcopy(game.side))
        gain, move = self.minmax(newgame, self.depth, deepcopy(game.side))
        return move

    def minmax(self, game : object, depth : int , maximizingplayer  : int, x : int = -1, y : int = -1) -> tuple :
        if depth == 0 or game.moves == [] :
            return evaluation.full_evaluation(game, maximizingplayer, x, y), (-1, -1)
        
        if game.side == maximizingplayer :
            value = 1000000000
            Bmove = (-1,-1)   
            for move in game.moves :
                game.play_one_turn(move[0], move[1])
                fliped = game.game.fliped
                yMM = self.minmax(game, depth-1, maximizingplayer, move[0], move[1])
                game.side = game.game.unmake_move(fliped, move[0], move[1], game.side)
                gain, _ = yMM[0], yMM[1]
                if gain < value :
                    value = gain
                    Bmove = move
        else :
            value = -1000000000
            Bmove = (-1,-1)   
            for move in game.moves :
                game.play_one_turn(move[0], move[1])
                fliped = game.game.fliped
                yMM = self.minmax(game, depth-1, maximizingplayer, move[0], move[1])
                game.side = game.game.unmake_move(fliped, move[0], move[1], game.side)
                gain, _ = yMM[0], yMM[1]
                if gain > value :
                    value = gain
                    Bmove = move
        
        return value, Bmove