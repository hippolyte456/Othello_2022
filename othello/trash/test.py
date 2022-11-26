from othello.minmax import Player
from othello import Othello
from copy import deepcopy

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
class IAplayer(Player):
    def __init__(self,Jside):
        self.Jside = Jside

    def pick_move():
        return minmax
#minmax 
    def minmax(self,game, side, depth):

        if game.board == self.terminal_board(game.board) or depth == 0:
            return self.evaluation_function(game.board)

        else:
            if self.Jside == side:
                gain = -10000
                for move in game.possible_moves(side):
                    game.play_move(move[0],move[1],side) #on veut jouer se coup dans un plateau virtuel !!!
                    gain = max(gain, self.minmax(self,next_board, -side, depth-1) )
                    return gain     #le max de ce qui nous est proposé
            else:
                gain = 10000
                for move in self.possible_moves(side): 
                    self.play_move(move[0],move[1],side)
                    gain = min(gain, self.minmax(self,next_board, -side, depth-1) )
                    return gain     #le min de ce qui nous est proposé

             
    
    def terminal_board(self):
        pass

    def differenceCount(self,board,joueur):
        pass
        return 0

    def evaluation_function(self):
        pass


