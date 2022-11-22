#au final il faudra créer une classe partie qui hérite du jeu othello et des joueurs... pas une fonction 
from othello import Othello 
import player 
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import datetime

class simulation():

    def __init__(self, player1, player2) :
        self.players = [player1, player2]
        self.tour = 0
        self.currentPlayer = 0
        self.side = 1
        self.game = Othello()

    def play(self):
        while (not self.game.game_over() and self.game.possible_moves(self.side) != []):
            x, y = self.players[self.currentPlayer].pick_move(self.game, self.side) #get choice
            self.game.play_move(x, y,self.side) # Update the board
            self.tour += 1 # update tunr
            self.currentPlayer = 1 - self.currentPlayer # Change player
            self.side = - self.side
            if not self.game.possible_moves(self.side) :
                self.currentPlayer = 1 - self.currentPlayer # Change player
                self.side = - self.side
        return (sum(sum(self.game.board)))
        

class playing_with_tkinter_interface():

    def __init__(self) :

        self.windows = Tk() # Init tkinter windows
        self.joueur1 = player.HumanPlayer() # By default players are humans
        self.joueur2 = player.HumanPlayer()

        # Labels
        Label(self.windows, text = "Othello Board", font = "Helvetica 16 bold")
        self.windows.title("Othello")

        # Create a Canva
        self.canva = Canvas(self.windows, width = 8 * 100, height = 8 * 100, bg = 'white')
        self.canva.pack(padx = 10, pady = 10)

        # get screen width and height
        self.ws = self.windows.winfo_screenwidth() # width of the screen
        self.hs = self.windows.winfo_screenheight() # height of the screen
        # Possibility to get an othello more responsive to user screen by using this dimension

        # setup_interface
        self.setup_interface()

        # Show intial board
        self.__init_variables()
        self.game.tkinter_board_init(self.canva)
        self.game.update_color(self.canva)

        self.display_tkinter()

    def setup_player(self):
        self.human = False
        if not self.joueur1.auto or not self.joueur2.auto :
            self.human = True
        self.joueurs = [self.joueur1, self.joueur2]

    def __init_variables(self):
        self.setup_player()
        self.tour = 0
        self.currentPlayer = 0
        self.side = 1
        self.stop = True
        self.game = Othello()

    def setup_interface(self):

        # init windows
        self.welcome = Toplevel(self.windows)

        Label(self.welcome, text = "Setup Interface", font = "Helvetica 16 bold")
        self.welcome.title("Setup Interface")

        # List choices :
        CHOICE = ["Human", "Random", "MinMax", "Alpha-Beta", "MCTS"]
        SIMULATION = [10, 20, 30, 40, 50]

        # PLAYER
        ### PLayer 1
        lplayer = Label(self.welcome, text="Players", font=("Arial 17 bold"))
        lplayer.grid(column = 0, row = 0)

        lplayer1 = Label(self.welcome, text="1 :")
        lplayer1.grid(column = 0, row = 1)

        self.playerchoice1 = IntVar() #IntVar()
        for i, rb_label in enumerate(CHOICE):
            rb_player1 = ttk.Radiobutton(self.welcome, text=rb_label, value=i, variable=self.playerchoice1, command=self.choice_player1)
            rb_player1.grid(column = i + 1, row = 1)

        ### PLayer 2
        lplayer2 = Label(self.welcome, text="2 :")
        lplayer2.grid(column=0, row=2)        

        self.playerchoice2 = IntVar()
        for i, rb_label in enumerate(CHOICE):
            rb_player2 = ttk.Radiobutton(self.welcome, text=rb_label, value=i, variable = self.playerchoice2, command=self.choice_player2)
            rb_player2.grid(column = i + 1, row = 2)

        # BUTTON

        ### PAUSE
        bouton_pause = Button(self.welcome, text="Start/Stop", command = self.start_and_stop, bg = 'green', fg = 'white', font = "Helvetica 9 bold")
        bouton_pause.grid(column=0, row = 10, columnspan=1)

        ### RESTART
        bouton_restart = Button(self.welcome, text="Restart", command = self.restart, bg = 'orange', fg = 'white')
        bouton_restart.grid(column=3, row = 10, columnspan=1)

        ### EXIT
        bouton_close = Button(self.welcome, text="Exit", command = self.close_tkinter, bg = "red", fg = 'white')
        bouton_close.grid(column=6, row = 10, columnspan=1)

        Label(self.welcome, text=" ", font=("Arial 17 bold")).grid(column = 0, row = 11)

        # SIMULATION
        ### PLayer 1
        lplayer = Label(self.welcome, text="Simulation", font=("Arial 17 bold"))
        lplayer.grid(column = 0, row = 12)

        self.nb_simu = IntVar() #IntVar()
        for i, rb_label in enumerate(SIMULATION):
            rb_simu = ttk.Radiobutton(self.welcome, text=rb_label, value=rb_label, variable=self.nb_simu, command=self.get_simu)
            rb_simu.grid(column = i + 1, row = 13)
        
        Label(self.welcome, text=" ", font=("Arial 17 bold")).grid(column = 0, row = 14)


        # LOCALISATION
        self.welcome.geometry('%dx%d+%d+%d' % (570, 300, self.ws, 0))

    def get_simu(self):
        self.now = datetime.datetime.now()
        options = self.nb_simu.get()
        cpt_black = 0
        cpt_white = 0
        equality = 0
        if self.joueur1.auto and self.joueur2.auto :
            while options :
                result = simulation(self.joueur1, self.joueur2).play()
                if result > 0:
                    cpt_black += 1
                elif result < 0:
                    cpt_white += 1
                else :
                    equality += 0
                Label(self.welcome, text=cpt_black, font=("Arial 9 bold")).grid(column=1, row=15)
                Label(self.welcome, text=equality, font=("Arial 9 bold")).grid(column=3, row=15)
                Label(self.welcome, text=cpt_white, font=("Arial 9 bold")).grid(column=5, row=15)
                Label(self.welcome, text="Player 1", font=("Arial 9 bold")).grid(column=1, row=16)
                Label(self.welcome, text="Equality", font=("Arial 9 bold")).grid(column=3, row=16)
                Label(self.welcome, text="Player 2", font=("Arial 9 bold")).grid(column=5, row=16)
                print("TIME INITIAL", datetime.datetime.now() - self.now)
                options -= 1
            # if  cpt_black > cpt_white :
            #     statement = 'Player 1 won ' + str(cpt_black) + ' VS ' + str(cpt_white) + ' (equality = ' + str(equality) + ')'
            # elif cpt_black < cpt_white :
            #     statement = 'Player 2 won ' + str(cpt_white) + ' VS ' + str(cpt_black) + ' (equality = ' + str(equality) + ')'
            # else :
            #     statement = 'Equality ' + str(cpt_black) + ' VS ' + str(cpt_white) 
            # messagebox.showwarning(title=None, message=statement)
            # self.lsimu = Label(self.welcome, text=statement, font=("Arial 9 bold"))
            # self.lsimu.grid(row = 14)

                
    def choice_player1(self):
        options = self.playerchoice1.get()
        if options == 0:
            self.joueur1 = player.HumanPlayer()
        elif options == 1:
            self.joueur1 = player.RandomPlayer()
        else :
            self.joueur1 = player.IAplayer(Jside= -1)
        self.setup_player()
        self.restart()


    def choice_player2(self):
        options = self.playerchoice2.get()
        if options == 0:
            self.joueur2 = player.HumanPlayer()
        elif options == 1:
            self.joueur2 = player.RandomPlayer()
        else :
            self.joueur2 = player.IAplayer(Jside= -1)
        self.setup_player()
        self.restart()


    def display_tkinter(self):
        """
        Tkinter loop
        """
        if not self.game.game_over() : # If we are still playing, it will show the result on the screen
            self.windows.geometry('%dx%d+%d+%d' % (820, 860, 0, 0))
            self.windows.mainloop()
    
    def restart(self):
        self.__init_variables()
        self.game.tkinter_board_init(self.canva)
        self.game.update_color(self.canva)
        try :
            self.winner.destroy()
        except :
            pass

    def close_tkinter(self):
        """
        Close the tkinter windows
        """
        self.windows.destroy()

    def mouse_click(self):
        self.posi = self.game.possible_moves(self.side)
        self.game.display_legal_moves(self.posi, self.canva)
        self.canva.bind("<Button-1>", self.player_manager)
        self.canva.pack()

    def player_manager(self, event = None):
        if not self.joueurs[self.currentPlayer].auto :
            self.x,self.y = self.joueurs[self.currentPlayer].move_from_tkinter(self.game, self.side, event)
            if self.x != -1 :
                self.play_turn()
                self.game.hide_legal_moves(self.posi, self.canva)
                if self.joueurs[self.currentPlayer].auto :
                    self.windows.after(10,self.player_manager)
                else :
                    self.posi = self.game.possible_moves(self.side) # show legal move for next player
                    self.game.display_legal_moves(self.posi, self.canva)

        else :
            self.game.hide_legal_moves(self.posi, self.canva)
            self.play_turn()
            self.posi = self.game.possible_moves(self.side) # show legal move for next player
            self.game.display_legal_moves(self.posi, self.canva)

    def start_and_stop(self):
        """
        Pause the game
        """
        self.stop = False if self.stop else True

        if not self.stop :
            if self.human :
                if not self.joueurs[0].auto :
                    self.mouse_click()
                else :
                    self.play_turn()
                    self.posi = self.game.possible_moves(self.side) # show legal move for next player
                    self.game.display_legal_moves(self.posi, self.canva)
                    self.mouse_click()
            else :
                self.init_play()

    def init_play(self):
        """
        Play until the end with a latency of 100 ms between each turn
        """
	    # Reprise du mouvement
        if not self.game.game_over() and not self.stop:
            self.play_turn()
            self.windows.after(100,self.init_play)

    def play_turn(self, event = None) :
        """
        Method to play a turn
        """
        self.posi = self.game.possible_moves(self.side)
        if self.posi != []: # Check if there is at least one valid move
            if self.joueurs[self.currentPlayer].auto :
                self.x,self.y = self.joueurs[self.currentPlayer].pick_move(self.game, self.side)
            self.game.play_move(self.x,self.y,self.side) # Update the board
            self.game.update_color(self.canva) # Update Tkinter objects
            self.tour += 1
            self.currentPlayer = 1 - self.currentPlayer # Change player
            self.side = - self.side
            if not self.game.possible_moves(self.side) :
                self.currentPlayer = 1 - self.currentPlayer # Change player
                self.side = - self.side
                if not self.joueurs[self.currentPlayer].auto : # Informe User about the change if he is human
                    messagebox.showwarning(title=None, message=("Black" if self.currentPlayer == 1 else "white") + " can not play" + "\n" + \
                    ("White" if self.currentPlayer == 1 else "Black") + " still playing")
        else: # If player cann't play, change player
            self.currentPlayer = 1 - self.currentPlayer 
            self.side = - self.side
        if self.game.game_over() or not self.game.possible_moves(self.side): # if it is the end
            winner_statement = 'Equality !' if sum(sum(self.game.board)) == 0 else 'Player ' + ('white' if sum(sum(self.game.board)) < 0 else 'black') + ' won the game !'
            self.winner = Label(self.windows, text=winner_statement, font=("Arial 17 bold"))
            self.winner.pack()

if __name__ == '__main__':
    # joueur1 = player.HumanPlayer()
    # joueur1 = player.RandomPlayer()
    # joueur2 = player.IAplayer(Jside= -1)
    # joueur2 = player.HumanPlayer()
    # game = Othello()
    # play_game(Othello,joueur1,joueur2)
    # tkinter_gestion(game,joueur1, joueur2)
    playing_with_tkinter_interface()
   
