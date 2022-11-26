from copy import deepcopy
import run
import evaluation

class Alpha_Beta():

    def __init__(self, depth : int = 2) -> None:
        self.depth = depth    
        self.auto = True

    def pick_move(self, game) -> tuple :
        newgame = run.simulation(game.players[0],game.players[1], deepcopy(game.game.board), game.side)
        gain, move = self.alphabeta(newgame, self.depth, game.side, -100000000, 100000000)
        return move

    def alphabeta(self, game, depth : int , maximizingplayer  : int, alpha : int, beta : int, x : int = -1, y : int = -1) -> tuple :
        if depth == 0 or game.moves == [] :
            res = evaluation.full_evaluation(game, maximizingplayer, x, y), (-1, -1)
            # print(res[0])
            return res
        Bmove = (-1,-1)   
        if game.side == maximizingplayer :
            for move in game.moves :
                game.play_one_turn(move[0], move[1])
                fliped = deepcopy(game.game.fliped)
                side = game.side # keep the previous player in case we have a no move for the next player
                yMM = self.alphabeta(game, depth-1, maximizingplayer, alpha, beta, move[0], move[1])
                game.side = game.game.unmake_move(fliped, move[0], move[1], side)
                gain, _ = yMM[0], yMM[1]
                if gain > alpha :
                    alpha = gain
                    Bmove = move
                    if (alpha >= beta) :
                        break
            return alpha, Bmove
        else :
            for move in game.moves :
                game.play_one_turn(move[0], move[1])
                fliped = deepcopy(game.game.fliped) 
                side = game.side      
                yMM = self.alphabeta(game, depth-1, maximizingplayer, alpha, beta, move[0], move[1])
                game.side = game.game.unmake_move(fliped, move[0], move[1], side)
                gain, _ = yMM[0], yMM[1]
                if gain < beta :
                    beta = gain
                    Bmove = move
                    if (alpha >= beta):
                        break
            return beta, Bmove

class NegaMax():
    """
    we evaluate a position not from the point of view of a fixed player (e.g. player MAX = program) 
    But from the point of view of the player who has the stroke on this position.
    No change comparing to alpha-beta, just shorter to program :D
    """
    def __init__(self, depth : int = 2) -> None:
        self.depth = depth    
        self.auto = True

    def pick_move(self, game) -> tuple :
        newgame = run.simulation(game.players[0],game.players[1], deepcopy(game.game.board), game.side)
        gain, move = self.negamax(newgame, self.depth, game.side, -100000000, 100000000)
        return move

    def negamax(self, game, depth : int , maximizingplayer  : int, alpha : int, beta : int, x : int = -1, y : int = -1) -> tuple :
        if depth == 0 or game.moves == [] :
            res = evaluation.full_evaluation(game, maximizingplayer, x, y), (-1, -1)
            # print(res[0])
            return res
        Bmove = (-1,-1)   
        for move in game.moves :
                game.play_one_turn(move[0], move[1])
                fliped = deepcopy(game.game.fliped)
                side = deepcopy(game.side)    
                yMM = self.negamax(game, depth-1, side, -beta, -alpha, move[0], move[1])
                game.side = game.game.unmake_move(fliped, move[0], move[1], side)
                gain, _ = -yMM[0], yMM[1]
                if gain > alpha :
                    alpha = gain
                    Bmove = move
                    if (alpha >= beta):
                        break
        return alpha, Bmove