virtual_boards[str(board.name) + str(move)]
chemin 
from copy import deepcopy

Jside = 1
initial_board = deepcopy(board)
def minmax(board, side, depth, chemin):
    current_board = create_board(initial_board, chemin)
    if board == terminal_board(board) or depth == 0:
        return evaluation_function(board)

    else:
        if Jside == side:
            gain = -10000
            for move in possible_moves(board,side):
                next_board = currentboardinitial_board
                play_move(move[0],move[1],side)
                gain = max(gain, minmax(next_board, -side, depth-1) )
                return gain     #le max de ce qui nous est proposé
        else:
            gain = 10000
            for move in possible_moves(side): 
                play_move(move[0],move[1],side)
                gain = min(gain, minmax(virtual_board, -side, depth-1) )
                return gain     #le min de ce qui nous est proposé

def possible_moves(board,side):
    pass

def evaluation_function(board,side):
    pass

def terminal_board(board):
    pass

def play_move(board):
    pass

def create_board(board,chemin)