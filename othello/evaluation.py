import numpy as np

def num_valid_moves(player : int, game) -> int :
    count = 0
    for i in range(8) :
        for j in range(8) :
            if (game.game.valid_flip(i, j , player)) :
                count += 1
    return count     


def full_evaluation(game, maximizingplayer, x = -1, y = -1) -> int:
    # Variable initialization
    density_map = np.array([[20, -3, 11, 8, 8, 11, -3, 20],
	                             [-3, -7, -4, 1, 1, -4, -7, -3],
	                             [11, -4, 2, 2, 2, 2, -4, 11],
	                             [8, 1, 2, -3, -3, 2, 1, 8],
	                             [8, 1, 2, -3, -3, 2, 1, 8],
	                             [11, -4, 2, 2, 2, 2, -4, 11],
	                             [-3, -7, -4, 1, 1, -4, -7, -3],
	                             [20, -3, 11, 8, 8, 11, -3, 20] ])
    X1 = [-1, -1 , 0, 1, 1, 1, 1, 0, -1]
    Y1 = [0, 1, 1, 1, 0, -1, -1, -1]
    density_value = 0
    my_coin = 0
    my_front = 0
    opp_coin = 0
    opp_front = 0
    
    # number of coin, frontier and density
    for i in range(8):
        for j in range(8) :
            if game.game.board[i,j] == maximizingplayer :
                density_value += density_map[i,j]
                my_coin += 1
            elif game.game.board[i,j] == -maximizingplayer :
                density_value -= density_map[i,j]
                opp_coin += 1
            elif game.game.board[i,j] != 0 :
                for k in range(8):
                    x = i + X1[k]
                    y = j + Y1[k]
                    if (x >= 0 and x < 8 and y >= 0 and y < 8 and game.game.board[x,y] == 0) :
                        if (game.game.board[i,j] == maximizingplayer):
                            my_front += 1
                        else :
                            opp_front += 1
                        break
    if (my_coin > opp_coin) :
        coin_value = (100 * my_coin)/(my_coin + opp_coin)
    elif (my_coin < opp_coin) :
        coin_value = -(100 * opp_coin)/(my_coin + opp_coin)
    else :
        coin_value = 0
    
    if (my_front > opp_front):
        front_value = -(100 * my_front)/(my_front + opp_front)
    elif (my_front < opp_front):
        front_value = (100 * opp_front)/(opp_front + my_front)
    else :
        front_value = 0
    
    # Corner occupancy
    my_coin = opp_coin = 0
    if (game.game.board[0,0] == maximizingplayer):
        my_coin +=1
    elif (game.game.board[0,0] == -maximizingplayer):
        opp_coin +=1
    if (game.game.board[0,7] == maximizingplayer):
        my_coin +=1
    elif (game.game.board[0,7] == -maximizingplayer):
        opp_coin +=1
    if (game.game.board[7,0] == maximizingplayer):
        my_coin +=1
    elif (game.game.board[7,0] == -maximizingplayer):
        opp_coin +=1
    if (game.game.board[7,7] == maximizingplayer):
        my_coin +=1
    elif (game.game.board[7,7] == -maximizingplayer):
        opp_coin +=1
    corner_value = 25 * (my_coin - opp_coin)

    # Corner nearess
    my_coin = opp_coin = 0
    if (game.game.board[0,0] == 0):
        if (game.game.board[0,1] == maximizingplayer):
            my_coin += 1
        elif (game.game.board[0,1] == -maximizingplayer):
            opp_coin += 1
        if (game.game.board[1,1] == maximizingplayer):
            my_coin += 1
        elif (game.game.board[1,1] == -maximizingplayer):
            opp_coin += 1
        if (game.game.board[1,0] == maximizingplayer):
            my_coin += 1
        elif (game.game.board[1,0] == -maximizingplayer):
            opp_coin += 1
    if (game.game.board[0,7] == 0):
        if (game.game.board[0,6] == maximizingplayer):
            my_coin += 1
        elif (game.game.board[0,6] == -maximizingplayer):
            opp_coin += 1
        if (game.game.board[1,7] == maximizingplayer):
            my_coin += 1
        elif (game.game.board[1,7] == -maximizingplayer):
            opp_coin += 1
        if (game.game.board[1,6] == maximizingplayer):
            my_coin += 1
        elif (game.game.board[1,6] == -maximizingplayer):
            opp_coin += 1
    if (game.game.board[7,0] == 0):
        if (game.game.board[6,0] == maximizingplayer):
            my_coin += 1
        elif (game.game.board[6,0] == -maximizingplayer):
            opp_coin += 1
        if (game.game.board[7,1] == maximizingplayer):
            my_coin += 1
        elif (game.game.board[7,1] == -maximizingplayer):
            opp_coin += 1
        if (game.game.board[6,1] == maximizingplayer):
            my_coin += 1
        elif (game.game.board[6,1] == -maximizingplayer):
            opp_coin += 1
    if (game.game.board[7,7] == 0):
        if (game.game.board[6,7] == maximizingplayer):
            my_coin += 1
        elif (game.game.board[6,7] == -maximizingplayer):
            opp_coin += 1
        if (game.game.board[7,6] == maximizingplayer):
            my_coin += 1
        elif (game.game.board[7,6] == -maximizingplayer):
            opp_coin += 1
        if (game.game.board[6,6] == maximizingplayer):
            my_coin += 1
        elif (game.game.board[6,6] == -maximizingplayer):
            opp_coin += 1
    corner_nearess_value = -12.5 * (my_coin - opp_coin)
    # Mobility
    my_coin = num_valid_moves(maximizingplayer, game)
    opp_coin = num_valid_moves(-maximizingplayer, game)
    if (my_coin > opp_coin) :
        mobility_value = (100 * my_coin)/(my_coin + opp_coin)
    elif (my_coin < opp_coin) :
        mobility_value = -(100 * opp_coin)/(my_coin + opp_coin)
    else :
        mobility_value = 0
    
    return ((10 * coin_value) + (801.724 * corner_value) + (382.026 * corner_nearess_value) + (78.922 * mobility_value) + (74.396 * front_value) + (10 * density_value))
# Inspired from https://github.com/kartikkukreja/blog-codes/blob/master/src/Heuristic%20Function%20for%20Reversi%20(Othello).cpp

def check_neighborhood(game, i : int, j : int) -> int:
    # self.density_map = np.array([[20 , -3, 11, 8, 8, 11, -3, 20],
    #                              [-3 , -7, -4, 1, 1, -4, -7, -3],
    #                              [11 , -4, 2, 2, 2, 2, -4, 11],
    #                              [8  , 1, 2, -3, -3, 2, 1, 8],
    #                              [8  , 1, 2, -3, -3, 2, 1, 8],
    #                              [11 , -4, 2, 2, 2, 2, -4, 11],
    #                              [-3 , -7, -4, 1, 1, -4, -7, -3],
    #                              [20 , -3, 11, 8, 8, 11, -3, 20] ])
    density_map = np.array([[120, -20 , 20 , 5  , 5  , 20 , -20 , 120],
                                [-20 , -30 , -5 , -5 , -5 , -5 , -30 , -20],
                                [20  , -5  , 15 , 3  , 3  , 15 , -5  , 20 ],
                                [5   , -5  , 3  , 3  , 3  , 3  , -5  , 5  ],
                                [5   , -5  , 3  , 3  , 3  , 3  , -5  , 5  ],
                                [20  , -5  , 15 , 3  , 3  , 15 , -5  , 20 ],
                                [-20 , -30 , -5 , -5 , -5 , -5 , -30 , -20],
                                [120 , -20 , 20 , 5  , 5  , 20 , -20 , 120]])
    tot = [0]
    for dx in range(i-1,i+2):
        for dy in range(j-1,j+2):
            if game.game.board[dx,dy] == 0:
                tot.append(density_map[dx,dy])
    return tot       

def density_evalutation(game, maximizingplayer, x = -1, y = -1):
    risk = 0 
    gain = 0
    for i in range(7):
        for j in range(7):
            if game.game.board[i,j] == -maximizingplayer:
                risk += max(check_neighborhood(game, i, j))
            elif game.game.board[i,j] == maximizingplayer :
                gain += max(check_neighborhood(game, i, j))
    if risk == 0 :
        return (100)
    elif risk < 0 and gain < 0:
        return ((gain/risk))
    elif risk < 0 and gain > 0:
        return ((gain / -(1/risk)))
    return ((gain/risk))