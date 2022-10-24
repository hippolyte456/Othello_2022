#au final il faudra créer une classe partie qui hérite du jeu othello et des joueurs... pas une fonction 
from othello import Othello 
import player 



class partie(Othello):
    
    def __init__(self,joueur1,joueur2):
        self.currentplayer = 0
        self.side = 1
        self.joueurs = [joueur1, joueur2]

    def run(self):
        while game.game_over() == False:
        if game.possible_move(side) #possible_move du current player != empty:
            x,y = joueurs[currentplayer].pick_move()
            game.play_move(x,y,side)
        else:
            current_player = 1 - current_player
    
    
    game = Othello()
    
          





if __name__ == '__main__':
    joueur1 = player.RandomPlayer()
    joueur2 = player.HumanPlayer()
    play_game(Othello,joueur1,joueur2)
   
