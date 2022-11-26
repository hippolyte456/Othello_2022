import numpy as np

class Othello(object):
    """
    Object that will store all informations related to the board and tkinter associated object (case, token ...)
    """
    
    def __init__(self, board : int = np.zeros((8, 8), dtype=int)):
        self.board = board
        if not 1 in self.board : # If it is a not an emty board
            self.board[3, 3] = 1
            self.board[3, 4] = -1
            self.board[4, 3] = -1
            self.board[4, 4] = 1
    
    def unmake_move(self, fliped, x : int, y : int,  side : int) -> int:
        """
        Undo last move
        return the last player
        """
        self.board[x, y] = 0
        for tx, ty in fliped :
            self.board[tx,ty] = -self.board[tx,ty]
        return -side

    def play_move(self, x : int, y : int, side : int) -> None:
        """
        Actualized the board if it is a real position
        """
        if x == -1 and y == -1 :
            return
        self.board[x,y] = side
        self.flip(x, y, side)
        self.x = x # Keep information for undo move
        self.y = y
        
    def game_over(self) -> bool:
        """
        Inform if there still
        """
        return (0 not in self.board)

    def get_winner(self):
        """
        inform the winner
        """
        t = np.sum(self.board)
        if t > 0:
            return 1
        if t < 0:
            return -1
        return 0
    
    def possible_moves(self, side : int) -> list :
        """
        return list (xi, yi) of possible moves
        """
        return [(i, j) for i in range(8) for j in range(8) if self.board[i,j] == 0 and self.valid_flip(i,j, side)]
    
    def valid_flip(self, x : int, y : int, side : int) -> bool:
        """
        For each flip check if it is a valid move
        """
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dy == 0 and dx == 0:
                    continue
                if(self.valid_ray(x, y, side, dx, dy)):
                    return True
        return False
    
    def valid_ray(self, x : int, y : int, side : int, dx : int, dy : int) -> bool:
        """
        For each ray check if it is a valid move
        """
        tx = x + 2*dx
        if tx < 0 or tx > 7:
            return False
        ty = y + 2*dy
        if ty < 0 or ty > 7:
            return False
        if self.board[x+dx, y+dy] != -1*side:
            return False
        while self.board[tx, ty] != side:
            if self.board[tx, ty] == 0:
                return False
            tx += dx
            ty += dy
            if tx < 0 or tx > 7:
                return False
            if ty < 0 or ty > 7:
                return False
        return True
    
    def flip(self, x : int , y : int, side : int) -> None :
        """
        Flip the position and then flip ray
        """
        self.fliped = [] # will store all flipped tokens
        for dx in range(-1, 2) :
            for dy in range(-1, 2) :
                if dy == 0 and dx == 0:
                    continue
                if(self.valid_ray(x, y, side, dx, dy)):
                    self.flip_ray(x, y, side, dx, dy)
    
    def flip_ray(self, x : int, y : int, side : int, dx : int, dy : int) -> None:
        """
        Flip the ray
        """
        tx = x + dx
        ty = y + dy
        while self.board[tx, ty] != side:
            self.board[tx, ty] = side
            self.fliped.append((tx, ty))
            tx += dx
            ty += dy
    
    def tkinter_board_init(self, canva, size : int) -> None :
        """
        Create all tkinter object related to the board
        Input : tkinter windows & bord
        Output : - Lst of token represented by an oval
                 - Lst of valid marker position represented by a smaller oval
        """
        # Display square on the windows
        self.color_square = ['green','DarkSeaGreen3']
        self.color_oval = ['black','white']
        self.tkn_lst = []
        self.oval_lst = []
        i = 0
        while i < 8 :
            j = 0
            while j < 8 :
                canva.create_rectangle(i * size, j * size, i * size + size, j * size + size, fill = self.color_square[(i + j) % 2])
                token = canva.create_oval(i * size + (size * 0.05), j * size + (size * 0.05), i* size + (size * 0.95) , j * size + (size * 0.95), fill = self.color_square[(i + j) % 2], outline="")
                oval = canva.create_oval(i * size + (size * 0.40), j * size + (size * 0.40), i * size + (size * 0.60), j * size + (size * 0.60), fill = self.color_square[(i + j) % 2], outline="")
                self.tkn_lst.append(token)
                self.oval_lst.append(oval)
                j += 1
            i += 1
    
    def display_legal_moves(self, coor : list, canva) -> None :
        """
        Take the list of valid positions (coor) and change the color of the corresponding small ovals to yellow
        """
        for (i,j) in coor:
            canva.itemconfig(self.oval_lst[j * 8 + i], fill= 'yellow')

    def hide_legal_moves(self, coor : list, canva) -> None :
        """
        Take the list of previous valid position and change back the color depending of board state
        """
        for (i,j) in coor:
            if (self.board[i ,j] == 1) :
                canva.itemconfig(self.oval_lst[j * 8 + i], fill= 'black', outline="")
            elif (self.board[i ,j] == -1) :
                canva.itemconfig(self.oval_lst[j * 8 + i], fill= 'white', outline="")
            else :
                canva.itemconfig(self.oval_lst[j * 8 + i], fill= self.color_square[(i + j) % 2], outline="")

    def update_color(self, canva) -> None:
        """
        Update the canva object according the state of the board
        """
        i = 0
        while i < 8 :
            j = 0
            while j < 8 :
                if (self.board[j ,i] == 1) :
                    canva.itemconfig(self.tkn_lst[i * 8 + j], fill= 'black')
                    canva.itemconfig(self.oval_lst[i * 8 + j], fill= 'black', outline="")
                elif (self.board[j ,i] == -1) :
                    canva.itemconfig(self.tkn_lst[i * 8 + j], fill= 'white')
                    canva.itemconfig(self.oval_lst[i * 8 + j], fill= 'white', outline="")
                j += 1
            i += 1

    #
    #   TO REMOVE (but can be usefull for debugging)
    #

    def print_board(self):  
        print("   ", end="")
        for i in range(8):
            print("%2d" % (i) , end="")
        print("\n   ", end="")
        for _ in range(16):
            print("-", end="")
        print("-")
        for i in range(8):
            print("%2d " % (i) , end="")
            for j in range(8):
                print("|" + Othello.piece_map(self.board[i,j]), end="")
            print("|")
            print("   ", end="")
            for _ in range(16):
                print("-", end="")
            print("-")
    
    @staticmethod
    def piece_map(x):
        return {
            1: 'W',
            -1: 'B',
            0: ' ',
        }[x]
        
    @staticmethod
    def move_id(move):
        if move == (-1,-1):
                return 64
        return move[0]+move[1]*8
    
    move_count = 65
    
    def get_move(mid):
        if mid == 64:
            return (-1, -1)
        x = mid%8
        y = mid//8
        return (x, y)
           
    @staticmethod
    def state_id(board):
        x = np.add(board, 1).flatten()
        id = 0
        mult = 1
        for t in x:
            id += mult*int(t)
            mult *= 3
        return id
