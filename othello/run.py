from othello import Othello 
from tkinter import *
from tkinter import messagebox
import player 
import tkinter.ttk as ttk
import datetime
import numpy as np

class simulation():
    """
    Play a whole othello game without tkinter interface
    """

    def __init__(self, player1 : object, player2: object, board : float, side : int) -> None :
        """
        Intput :
            - Type of player chosen by the user
            - Board : numpy.ndarray (matrix representing the state of the game)
            - Side : Indicates who plays
        """
        self.players = [player1, player2]
        self.side = side
        self.game = Othello(board)
        self.moves = self.game.possible_moves(self.side)

    def play_one_turn(self, x : int , y: int) -> None:
        """
        Play one turn of the game
        Input : (x, y) coordinates of the move
        """
        self.game.play_move(x, y,self.side) # Play the move
        self.side = -self.side # Change player
        self.moves = self.game.possible_moves(self.side) # Get new possibles moves
        if self.moves == [] : # If no moves
            self.side = -self.side # Change player
            self.moves = self.game.possible_moves(self.side) # Get new possibles moves

    def play(self) -> int:
        """
        Play the whole game until someone wins
        Output : Sum of the board (representing the winner)
        """
        while (-1): # Until the end of the game
            x, y = self.players[0 if self.side == 1 else 1].pick_move(self) # Get choice
            self.play_one_turn(x, y) # Play one turn
            if self.moves == [] : # If no more moves = end of game
                return (np.sum(self.game.board)) # Return sum of the board

class game_manager():
    """
    Manager allowing to interact with the user thanks to the tkinter library. 
    Main features:
        - Choice of player type
        - Launch a visual game
        - Launching a simulation
    """

    def __init__(self) -> None :
        self.windows = Tk() # Init tkinter windows
        self.player1 = player.HumanPlayer() # By default players are humans
        self.player2 = player.HumanPlayer()

        # Labels
        Label(self.windows, text = "Othello Board", font = "Helvetica 16 bold")
        self.windows.title("Othello")

        # Get screen width and height
        self.ws = self.windows.winfo_screenwidth() # width of the screen
        self.hs = self.windows.winfo_screenheight() # height of the screen
        self.size = self.hs / 9 #Size of a square

        # Create a Canva
        self.canva = Canvas(self.windows, width = 8 * self.size, height = 8 * self.size, bg = 'white')
        self.canva.pack(padx = 10, pady = 10)

        # Create Manager Windows 
        self.manager_windows()

        # Create playing windows
        self.__init_variables()
        self.game.tkinter_board_init(self.canva, self.size)
        self.game.update_color(self.canva)

        self.display_tkinter()

    def setup_player(self) -> None:
        """
        Define a "human" variable that will be used to know if the user should be asked for a choice
        """
        self.human = False
        if not self.player1.auto or not self.player2.auto :
            self.human = True
        self.players = [self.player1, self.player2]

    def __init_variables(self) -> None:
        """
        side : Defines who plays
            1 = Black  or -1 = White
        stop : To pause the tkinter loop
        done : Avoid repetitive messabox in recursion function
        """
        self.setup_player()
        self.side = 1 # We start with the first player 
        self.stop = True
        self.game = Othello(np.zeros((8, 8), dtype=int))
        self.done = False
        self.moves = self.game.possible_moves(self.side)

    def manager_windows(self):
        """
        Method with all the information for the manager window
        """
        # Create tkinter windows under 
        self.win_manager = Toplevel(self.windows)

        Label(self.win_manager, text = "SETTINGS", font = "Helvetica 16 bold")
        self.win_manager.title("SETTINGS")

        # List choices :
        CHOICE = ["Human", "Random", "MinMax", "Alpha-Beta", "MCTS"]
        SIMULATION = [10, 20, 30, 40, 50]

        # PLAYER
        ### PLayer 1
        Label(self.win_manager, text="Players", font=("Arial 17 bold")).grid(column = 0, row = 0)
        Label(self.win_manager, text="1 :").grid(column = 0, row = 1)

        self.playerchoice1 = IntVar() # Variable that will get the user choice for player 1
        for i, label in enumerate(CHOICE):
            ttk.Radiobutton(self.win_manager, text=label, value=i, variable=self.playerchoice1
                            , command=self.choice_player1).grid(column = i + 1, row = 1)

        ### PLayer 2
        Label(self.win_manager, text="2 :").grid(column=0, row=2)        

        self.playerchoice2 = IntVar() # Variable that will get the user choice for player 2
        for i, label in enumerate(CHOICE):
            ttk.Radiobutton(self.win_manager, text=label, value=i, variable = self.playerchoice2
                            , command=self.choice_player2).grid(column = i + 1, row = 2)
        
        Label(self.win_manager, text=" ", font=("Arial 17 bold")).grid(column = 0, row = 3)

        # BUTTON
        ### PAUSE
        Button(self.win_manager, text="Start/Stop", command = self.start_and_stop, bg = 'green'
                , fg = 'white').grid(column=0, row = 10, columnspan=1)

        ### RESTART
        Button(self.win_manager, text="Restart", command = self.restart, bg = 'orange'
                , fg = 'white').grid(column=3, row = 10, columnspan=1)

        ### EXIT
        Button(self.win_manager, text="Exit", command = self.windows.destroy
                , bg = "red", fg = 'white').grid(column=6, row = 10, columnspan=1)

        Label(self.win_manager, text=" ", font=("Arial 17 bold")).grid(column = 0, row = 11)

        # SIMULATION
        Label(self.win_manager, text="Simulation", font=("Arial 17 bold")).grid(column = 0, row = 12)

        self.nb_simu = IntVar() #IntVar()
        for i, label in enumerate(SIMULATION):
            ttk.Radiobutton(self.win_manager, text=label, value=label, variable=self.nb_simu
                            , command=self.get_simu).grid(column = i + 1, row = 13)
        
        Label(self.win_manager, text=" ", font=("Arial 17 bold")).grid(column = 0, row = 14)


        # LOCALISATION
        self.win_manager.geometry('%dx%d+%d+%d' % (570, 250, self.ws, 0))

    def get_simu(self) -> None:
        """
        Launch the right number of simulation
            Input : Number of simulation choose by the user
            Output : Display result on the Manager Windows
        """
        self.now = datetime.datetime.now()
        options = self.nb_simu.get()
        cpt_black, cpt_white, equality = 0, 0, 0
        if self.player1.auto and self.player2.auto :
            while options :
                result = simulation(self.player1, self.player2, np.zeros((8, 8), dtype=int), self.side).play()
                if result > 0:
                    cpt_black += 1
                elif result < 0:
                    cpt_white += 1
                else :
                    equality += 1
                options -= 1
                if not options % 10 :
                    print(options , " - TIME ", datetime.datetime.now() - self.now)

            Label(self.win_manager, text=cpt_black, font=("Arial 9 bold")).grid(column=1, row=15)
            Label(self.win_manager, text=equality, font=("Arial 9 bold")).grid(column=3, row=15)
            Label(self.win_manager, text=cpt_white, font=("Arial 9 bold")).grid(column=5, row=15)
            Label(self.win_manager, text="Player 1", font=("Arial 9 bold")).grid(column=1, row=16)
            Label(self.win_manager, text="Equality", font=("Arial 9 bold")).grid(column=3, row=16)
            Label(self.win_manager, text="Player 2", font=("Arial 9 bold")).grid(column=5, row=16)

                
    def choice_player1(self) -> None:
        """
        Create a player 1 object of the right type
        Input : Choice for player1
        """
        options = self.playerchoice1.get()
        if options == 0:
            self.player1 = player.HumanPlayer()
        elif options == 1:
            self.player1 = player.RandomPlayer()
        else :
            self.player1 = player.dummy_evaluation_player() # Still in progress : just minmax for the moment
        self.setup_player()
        self.restart()


    def choice_player2(self) -> None:
        """
        Create a player 1 object of the right type
        Input : Choice for player1
        """
        options = self.playerchoice2.get()
        if options == 0:
            self.player2 = player.HumanPlayer()
        elif options == 1:
            self.player2 = player.RandomPlayer()
        else :
            self.player2 = player.DensityMinMax(depth = 3) # Still in progress : just minmax for the moment
        self.setup_player()
        self.restart()


    def display_tkinter(self) -> None:
        """
        Tkinter loop
        """
        if not self.game.game_over() : # If we are still playing, it will show the result on the screen
            self.windows.geometry('%dx%d+%d+%d' % (self.size * 9, self.size * 9, 0, 0))
            self.windows.mainloop()
    
    def restart(self) -> None:
        """
        Restart a new othello game (rest inital variable)
        """
        self.__init_variables()
        self.game.tkinter_board_init(self.canva, self.size)
        self.game.update_color(self.canva)
        try :
            self.winner.destroy() # Del winner label
        except :
            pass

    def mouse_click(self) -> None:
        """
        Get user click on the windows
        """
        self.moves = self.game.possible_moves(self.side) # Get legal moves
        self.game.display_legal_moves(self.moves, self.canva) # Display legal moves on 
        self.canva.bind("<Button-1>", self.player_manager) # Get User click
        self.canva.pack()

    def start_and_stop(self):
        """
        Pause the game
        """
        self.stop = False if self.stop else True

        if not self.stop :
            if self.human :
                if self.players[0].auto :
                    self.play_turn()
                    self.moves = self.game.possible_moves(self.side) # show legal move for next player
                    self.game.display_legal_moves(self.moves, self.canva)
                self.mouse_click()
            else :
                self.init_play()


    def player_manager(self, event = None) -> None :
        """
        
        """
        if not self.players[0 if self.side == 1 else 1].auto :
            self.x,self.y = self.players[0 if self.side == 1 else 1].move_from_tkinter(self.game, self.side, event, self.size)
            if self.x != -1 :
                self.play_turn()
                self.game.hide_legal_moves(self.moves, self.canva)
                if self.players[0 if self.side == 1 else 1].auto :
                    self.windows.after(10,self.player_manager)
                else :
                    self.moves = self.game.possible_moves(self.side) # show legal move for next player
                    self.game.display_legal_moves(self.moves, self.canva)
        else :
            self.game.hide_legal_moves(self.moves, self.canva)
            self.play_turn()
            self.moves = self.game.possible_moves(self.side) # show legal move for next player
            self.game.display_legal_moves(self.moves, self.canva)

    def init_play(self) -> None :
        """
        Play until the end with a latency of 100 ms between each turn
        """
        if not self.game.game_over() and not self.stop:
            self.play_turn()
            self.windows.after(10,self.init_play)

    def play_turn(self) -> None :
        """
        Method to play a turn
        """
        self.moves = self.game.possible_moves(self.side)
        if self.players[0 if self.side == 1 else 1].auto :
            self.x,self.y = self.players[0 if self.side == 1 else 1].pick_move(self)
        self.game.play_move(self.x,self.y,self.side) # Update the board
        self.game.update_color(self.canva) # Update Tkinter objects
        self.side = - self.side
        if not self.game.possible_moves(self.side) :
            self.side = - self.side
            if not self.players[0 if self.side == 1 else 1].auto and not self.game.game_over(): # Informe User about the change if he is human
                messagebox.showwarning(title=None, message=("Black" if self.side == -1 else "white") + " can not play" + "\n" + \
                ("White" if self.side == -1 else "Black") + " still playing")
        if self.game.game_over() or not self.game.possible_moves(self.side) and not self.done: # if it is the end
            self.done = True
            winner_statement = 'Equality !' if sum(sum(self.game.board)) == 0 else 'Player ' + ('white' if sum(sum(self.game.board)) < 0 else 'black') + ' won the game !'
            self.winner = Label(self.windows, text=winner_statement, font=("Arial 17 bold"))
            self.winner.pack()

if __name__ == '__main__':
    game_manager()
   
