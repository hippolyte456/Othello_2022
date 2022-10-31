import random as rd

def minmax(board, side, depth):
    if game_over(board) or depth == 0:
        return evaluation_function(board)

    else:
        if 1 == side:
            gain = -10000
            Bmove = [-1,-1]
            for move in possible_moves(board,side):
                if gain < minmax(play_move(board, move[0], move[1], side), -side, depth-1):
                    gain, Bmove = minmax(play_move(board, move[0], move[1], side), -side, depth-1), move
            return gain, Bmove    #le max de ce qui nous est proposé
        else:
            gain = 10000
            Bmove = [-1,-1]
            for move in possible_moves(board,side): 
                if gain > minmax(play_move(board, move[0], move[1], side), -side, depth-1):
                    gain, Bmove = minmax(play_move(board, move[0], move[1], side), -side, depth-1), move
            return gain, Bmove    #le min de ce qui nous est proposé


def evaluation_function(board,side):
    return rd.random()

def play_move(board, x, y, side):
        if x == -1 and y == -1:
            return
        board[x,y] = side
        flip(x, y, side)



def game_over(board):
        for i in range(8):
            for j in range(8):
                if board[i,j] == 0 and (valid_flip(board,i,j, -1) or valid_flip(board,i,j, 1)):
                    return False
        return True

def possible_moves(board, side):
        moves = []
        for i in range(8):
            for j in range(8):
                if board[i,j] == 0 and valid_flip(board,i,j, side):
                    moves.append((i, j))
        return moves
    
def valid_flip(board, x, y, side):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dy == 0 and dx == 0:
                continue
            if(valid_ray(board,x, y, side, dx, dy)):
                return True
    return False

def valid_ray(board, x, y, side, dx, dy):
    tx = x + 2*dx
    if tx < 0 or tx > 7:
        return False
    ty = y + 2*dy
    if ty < 0 or ty > 7:
        return False
    if board[x+dx, y+dy] != -1*side:
        return False
    while board[tx, ty] != side:
        if board[tx, ty] == 0:
            return False
        tx += dx
        ty += dy
        if tx < 0 or tx > 7:
            return False
        if ty < 0 or ty > 7:
            return False
    return True

def flip(board, x, y, side):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dy == 0 and dx == 0:
                continue
            if(valid_ray(board,x, y, side, dx, dy)):
                flip_ray(board,x, y, side, dx, dy)

def flip_ray(board, x, y, side, dx, dy):
    tx = x + dx
    ty = y + dy
    while board[tx, ty] != side:
        board[tx, ty] = side
        tx += dx
        ty += dy