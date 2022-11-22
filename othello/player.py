
#des questions que je me suis posé... à garder en tête pour être moins bête la prochaine fois 

"""pour optimiser le cout en mémoire, il ne faut pas charger tous les plateaux, mais chargé un seul plateau virtuel ainsi 
que les mouvements nécessaires pour passer d'un noeud à l'autre... et une fonction qui transforme le plateau virtuel au 
plateau suivant"""

"""une bonne façon d'écrire le programme serait de créer une classe node = un plateau, un state terminal ou non,
un state min ou un state max """

"""plus generalement : comment mon objet aiplayer doit interagir avec Othello"""

"""comment je fais pour garder en mémoire les boards et pas changer le plateau initial ?"""

"""2 problemes : 1/ l'utilisation de fonction d'othello dans la classe player
                 2/ la mise en mémoire des plateaux pendant que l'algo tourne"""


from othello import Othello

import random
import numpy as np
from copy import deepcopy
from time import time
from math import *

class RandomPlayer():  
    
    def __init__(self) :
        self.auto = True

    def pick_move(self, game, side):
        t = game.possible_moves(side)
        if len(t) == 0:
            return (-1, -1)
        r = random.randint(0, len(t)-1)
        return (t[r][0], t[r][1])
    
class HumanPlayer(): 

    def __init__(self) :
        self.auto = False


    def move_from_tkinter(self, game, side, event):
        t = game.possible_moves(side)
        if len(t) == 0:
            print("No moves availible. Turn skipped.") #message boxe
            return (-1, -1)
        y = floor(event.x / 100)
        x = floor(event.y / 100)
        if (x, y) in t :
            return (x, y)
        return (-1, -1)

    def pick_move(self, game, side):
        game.print_board()
        print("You are playing", Othello.piece_map(side))
        t = game.possible_moves(side)
        if len(t) == 0:
            print("No moves availible. Turn skipped.")
            return (-1, -1)
        move = (-1, -1)
        while move not in t:
            try:
                row = int(input("Please input row: "))
                col = int(input("Please input col: "))
                move = (row, col)
                if move not in t:
                    game.print_board()
                    print("Please input a valid move")
            except Exception:
                print("Please input a valid move")
        return move
            


class IAplayer():
    
    def __init__(self,Jside = 1, param = np.array([1,1,1]), depth = 1):
        self.Jside = Jside
        self.depth = depth
        self.param = param
        self.auto = True    
    

    def pick_move(self, game, side):
        gain, move = self.minmax(game, side, self.depth)
        return move


    def minmax(self,game, side, depth):

        if game.game_over() or depth == 0:
            return self.evaluation_function(game), (-1,-1)

        else:
            if self.Jside == side:
                Bgain = -10000
                Bmove = (-1,-1)              
                for move in game.possible_moves(side):
                    next_board = deepcopy(game)
                    next_board.play_move(move[0],move[1],side)
                    #print('aaaah', side ,depth)
                    yMM  = self.minmax(next_board, -side, depth-1) 
                    #print(yMM)
                    gain, _ = yMM[0], yMM[1]
                    if gain > Bgain:
                        Bmove = move 
                        Bgain = gain 
                return Bgain, Bmove    #le max de ce qui nous est proposé
            else:
                Wgain = 10000
                Wmove = (-1,-1)
                for move in game.possible_moves(side): 
                    next_board = deepcopy(game)
                    next_board.play_move(move[0],move[1],side)
                    #print('ooooh' ,side, depth)
                    gain, _ = self.minmax(next_board, -side, depth-1)
                    if gain < Wgain:
                        Wmove = move 
                        Wgain = gain 
                return Wgain,Wmove      #le min de ce qui nous est proposé

             
    
    def evaluation_function(self,game):
        mobilite = len(game.possible_moves(self.Jside)) - len(game.possible_moves(-self.Jside))
        materiel = game.count_pieces(self.Jside)
        coins = 0
        a = self.param[0]*mobilite + self.param[1]*materiel + self.param[2]*coins
        return a


    '''fonction pour optimiser les paramètres de la fonction d'evaluation... ne fonctionne pas '''
    def train(self):
        ia = IAplayer(param = np.array([0,0,0]))
        while compare_algo(Othello,self,ia,10) > 50:
            ia = IAplayer(param = self.param)
            self.param = self.param + np.array([1,0,0])
            print('xxx' ,self.param)
        ia = IAplayer(param = np.array([0,0,0]))
        while compare_algo(Othello,self,ia,10) >= 50:
            ia = IAplayer(param = self.param)
            self.param = self.param + np.array([0,0,1])
            print('zzz' ,self.param)
            
            



'''
option possibles pour les differents IA : 
-soit la class peut prendre des attributs differents selon l'ia a generer (fonctions differentes 
et parametres de fonctions differnets)
-soit on fait plusieurs classes differentes
''' 

'''
class IAplayer_MCTS():
    
    def __init__(self,Jside = 1, param = np.array([1,1,1]), depth = 1):
        self.Jside = Jside
        self.depth = depth
        self.param = param
    

    def pick_move(self, game, side):
        gain, move = self.MCTS(game, side, self.depth)
        return move


    def MCTS(self,game,Playtime):
        execStart = time()
        currentExec = time()
        execTime = currentExec - execStart
        estimated_nodes = [game,1,0,None] #une liste de node de la forme [game, estim_value, numberOfVisit, noeuds_fils_visités]
        while execTime < Playtime:
            leaf = traverse(estimated_nodes)
            simulation_result = rollout(leaf)
            backpropagate(leaf, simulation_result)
            execTime = currentExec - execStart
            
            
        return best_child(root)

# function for node traversal
def traverse(game,estimated_nodes):
    if estimated_nodes[3] == None:
        #createLeaf et rajouter à estimated_nodes
    else:
        UCT(estimated_nodes[3]) #retourne le meilleur des noeuds 
        traverse(game,estimated_nodes[])

    return all possibility of game.play_game()

    
    # while fully_expanded(node):
    #     node = best_uct(node)
        
    # in case no children are present / node is terminal
    return pick_unvisited(node.children) or node

# function for the result of the simulation
def rollout(game):
    while non_terminal(node):
        node = rollout_policy(node)
    return result(node)

# function for randomly selecting a child node
def rollout_policy(node):
    return pick_random(node.children)

# function for backpropagation
def backpropagate(node, result):
    if is_root(node) return
    node.stats = update_stats(node, result)
    backpropagate(node.parent)

# function for selecting the best child
# node with highest number of visits
def best_child(node):
    pick child with highest number of visits

'''