from othello import Othello
import random
import numpy as np
from copy import deepcopy

    
class RandomPlayer():  
    
    def pick_move(self, game, side):
        t = game.possible_moves(side)
        if len(t) == 0:
            return (-1, -1)
        r = random.randint(0, len(t)-1)
        return (t[r][0], t[r][1])
    
class HumanPlayer(): 
    
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
            


'''question : comment on fait pour donner les moves possibles à minmax? il ne faut pas faire d'héritage multiple à priori
par contre le minmax est exécuté par un player qui a un side précis, donc on sait quand on est dans un noeud max ou min
 en appelant le side  avec self'''

"""pour optimiser le cout en mémoire, il ne faut pas charger tous les plateaux, mais chargé un seul plateau virtuel ainsi 
que les mouvements nécessaires pour passer d'un noeud à l'autre... et une fonction qui transforme le plateau virtuel au 
plateau suivant"""

"""une bonne façon d'écrire le programme serait de créer une classe node = un plateau, un state terminal ou non,
un state min ou un state max """

"""plus generalement : comment mon objet aiplayer doit interagir avec Othello"""


"""comment je fais pour garder en mémoire les boards et pas changer le plateau initial ?"""

"""2 problemes : 1/ l'utilisation de fonction d'othello dans la classe player
                 2/ la mise en mémoire des plateaux pendant que l'algo tourne"""

class IAplayer():
    
    def __init__(self,Jside, depth = 3, x1 = 1, x2 = 1, x3 = 1):
        self.Jside = Jside
        self.depth = depth
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
    

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
        a = self.x1*mobilite + self.x2*materiel + self.x2*coins
        #print(a)
        return a


'''
option possibles pour les differents IA : 
-soit la class peut prendre des attributs differents selon l'ia a generer (fonctions differentes 
et parametres de fonctions differnets)
-soit on fait plusieurs classes differentes
''' 