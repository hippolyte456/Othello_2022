#au final il faudra créer une classe partie qui hérite du jeu othello et des joueurs... pas une fonction 
from othello import Othello 
import player 



def play_game(game,joueur1, joueur2, display = True):
    joueurs = [joueur1, joueur2]
    tour = 0
    currentPlayer = 0
    side = 1
    game = Othello()
    while game.game_over() == False:
        if game.possible_moves(side) != []:
            x,y = joueurs[currentPlayer].pick_move(game,side)
            game.play_move(x,y,side)
            if display:
                game.print_board()
            tour += 1
            currentPlayer = 1 - currentPlayer
            side = - side
        else:
            currentPlayer = 1 - currentPlayer
            side = - side
    if display:
        print('le joueur gagnant est le joueur' + str(int(1.5 - 0.5*game.get_winner())))
    return(game.get_winner()) 

          
def compare_algo(game,algo1,algo2, n = 10):
    wgame1 = 0
    for i in range(n):
        if i % 2 == 0:
            algo1.Jside = 1
            algo1.Jside = -1
            winner = play_game(game,algo1,algo2, False)
            if winner == 1:
                wgame1 += 1 
        else:
            algo1.Jside = -1
            algo1.Jside = 1
            winner = play_game(Othello,algo2,algo1, False)
            if winner == -1:
                wgame1 += 1 
    
    print ('Le 1er algorithme gagne ' + str(wgame1 / n * 100 ) + '%' + ' des parties sur ' + str(n) + 'jouées.') 
    return wgame1 / n * 100







if __name__ == '__main__':
    #joueur1 = player.HumanPlayer()
    joueur1 = player.RandomPlayer()
    joueur2 = player.IAplayer(Jside = -1, depth=1)
    #play_game(Othello,joueur1,joueur2, False)
    #compare_algo(Othello,joueur1,joueur2,100)
    hippo = player.IAplayer()
    hippo.train()

   
