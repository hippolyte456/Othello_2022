#au final il faudra créer une classe partie qui hérite du jeu othello et des joueurs... pas une fonction 
from othello import Othello 
import player 



def play_game(game,joueur1, joueur2):
    joueurs = [joueur1, joueur2]
    tour = 0
    currentPlayer = 0
    side = 1
    game = Othello()
    while game.game_over() == False:
        if game.possible_moves(side) != []:
            x,y = joueurs[currentPlayer].pick_move(game,side)
            game.play_move(x,y,side)
            tour += 1
            currentPlayer = 1 - currentPlayer
            side = - side
        else:
            currentPlayer = 1 - currentPlayer
            side = - side
    print('le joueur gagnant est le joueur' + str(int(1.5 - 0.5*game.get_winner())))
          



if __name__ == '__main__':
    joueur1 = player.HumanPlayer()
    joueur2 = player.IAplayer(playerSide= -1)
    play_game(Othello,joueur1,joueur2)
   
