import run
import evaluation

class Alpha_Beta():

    def __init__(self, depth : int = 2) -> None:
        self.depth = depth    
        self.auto = True
        self.name = "Alpha-Beta"

    def pick_move(self, game) -> tuple :
        newgame = run.simulation(game.players[0],game.players[1], game.game.board, game.side)
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
                fliped = game.game.fliped
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
                fliped = game.game.fliped
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
        self.name = "NegaMax"

    def pick_move(self, game) -> tuple :
        newgame = run.simulation(game.players[0],game.players[1], game.game.board, game.side)
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
                fliped = game.game.fliped
                side = game.side
                yMM = self.negamax(game, depth-1, side, -beta, -alpha, move[0], move[1])
                game.side = game.game.unmake_move(fliped, move[0], move[1], side)
                gain, _ = -yMM[0], yMM[1]
                if gain > alpha :
                    alpha = gain
                    Bmove = move
                    if (alpha >= beta):
                        break
        return alpha, Bmove

class failsoft():
    """
    get the value that caused the cut.
        - if alpha < current < beta, then current is the minimax value
        - if current <= alpha, then the true minimax value m checks : m <= current <= alpha
        - if beta <= current then the true minimax value m verifies : beta <= current <= m
    """
    def __init__(self, depth : int = 2) -> None:
        self.depth  = depth    
        self.auto   = True
        self.name   = "Failsoft"

    def pick_move(self, game) -> tuple :
        newgame = run.simulation(game.players[0],game.players[1], game.game.board, game.side)
        gain, move = self.failsoft(newgame, self.depth, game.side, -100000000, 100000000)
        return move

    def failsoft(self, game, depth : int , maximizingplayer  : int, alpha : int, beta : int, x : int = -1, y : int = -1) -> tuple :
        if depth == 0 or game.moves == [] :
            res = evaluation.full_evaluation(game, maximizingplayer, x, y), (-1, -1)
            return res
        Bmove = (-1,-1)
        current = -100000000
        for move in game.moves :
                game.play_one_turn(move[0], move[1])
                fliped = game.game.fliped
                side = game.side
                yMM = self.failsoft(game, depth-1, side, -beta, -alpha, move[0], move[1])
                game.side = game.game.unmake_move(fliped, move[0], move[1], side)
                gain, _ = -yMM[0], yMM[1]
                if (gain > current) :
                    current = gain
                    Bmove = move
                    if gain > alpha :
                        alpha = gain
                        Bmove = move
                        if (alpha >= beta):
                            break
        return current, Bmove



class PrincipalVariationSearch():
    """
    Rather than blindly launching a new, time-consuming alpha-beta search to explore sister branches,
    A quick search with a null window (beta = alpha+1) would inform us of its utility.
    10 % faster than classical alpha-beta on depth 4 (non linear when increasing depth)
    """
    def __init__(self, depth : int = 2) -> None:
        self.depth  = depth    
        self.auto   = True
        self.name   = " PVS"

    def pick_move(self, game) -> tuple :
        newgame = run.simulation(game.players[0],game.players[1], game.game.board, game.side)
        gain, move = self.principalvariationsearch(newgame, self.depth, game.side, -100000000, 100000000)
        return move

    def principalvariationsearch(self, game, depth : int , maximizingplayer  : int, alpha : int, beta : int, x : int = -1, y : int = -1) -> tuple :
        if depth == 0 or game.moves == [] :
            res = evaluation.full_evaluation(game, maximizingplayer, x, y), (-1, -1)
            return res

        moves = game.moves
        Bmove = moves[0]
        game.play_one_turn(Bmove[0], Bmove[1])
        fliped = game.game.fliped
        side = game.side  
        yMM = self.principalvariationsearch(game, depth-1, side, -beta, -alpha, Bmove[0], Bmove[1])
        game.side = game.game.unmake_move(fliped, Bmove[0], Bmove[1], side)
        current, _ = -yMM[0], yMM[1]
        if current > alpha :
            alpha = current
        if current < beta :
            for move in moves[1:] :
                    game.play_one_turn(move[0], move[1])
                    fliped = game.game.fliped
                    side = game.side    
                    yMM = self.principalvariationsearch(game, depth-1, side, -(alpha +1), -alpha, move[0], move[1])
                    gain, _ = -yMM[0], yMM[1]
                    if (gain > alpha and gain < beta) :
                            self.principalvariationsearch(game, depth-1, side, -beta, -alpha, move[0], move[1])
                    game.side = game.game.unmake_move(fliped, move[0], move[1], side)
                    gain, _ = -yMM[0], yMM[1]
                    if (gain > current) :
                        current = gain
                        Bmove = move
                        if gain > alpha :
                            alpha = gain
                            if (gain >= beta):
                                break
        return current, Bmove

# class MTD():
#     """
#     MTD = Memory Test Driver
#     exploration of the tree with a null window
#     Rather than blindly launching a new, time-consuming alpha-beta search to explore sister branches,
#     A quick search with a null window (beta = alpha+1) would inform us of its utility.
#     10 % faster than classical alpha-beta on depth 4 (non linear when increasing depth)
#     """
#     def __init__(self, depth : int = 2) -> None:
#         self.depth = depth    
#         self.auto = True

#     def pick_move(self, game) -> tuple :
#         newgame = run.simulation(game.players[0],game.players[1], deepcopy(game.game.board), game.side)
#         gain, move = self.MTDF(newgame, self.depth, game.side, 0)
#         return move

#     def MTDF(self, game, depth, maximizingplayer, init_g) :
#         g = init_g
#         upperbound = 10000000000
#         lowerbound = -100000000000
#         while True :
#             beta = ((g + 1) if (g == lowerbound) else g)
#             yMM = self.alphabetawithmemory(game, depth, maximizingplayer, beta -1 , beta)
#             g = yMM[0]
#             if (g < beta) :
#                 upperbound = g
#             else :
#                 lowerbound = g
#             if (lowerbound != upperbound):
#                 break
#         return yMM
