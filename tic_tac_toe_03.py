###########################################################################
#
# tic_tac_toe_03.py
#
# CS-043-T001 Part 2 - Unit 6 - Final Collaborative Project: 1-3
#
# Play against the computer
# Make it to use class.
# Make it to play against another person or the computer.
# Added playing on a graphical table.
#
# The base copied fom: Sweigart, Al.
# Invent Your Own Computer Games with Python, 4E (p. 123). No Starch Press.
#
###########################################################################
#
# Tic-Tac-Toe

import sys
import time  # sleep(seconds)

import inspect
def ln() -> str:
    return f'{inspect.currentframe().f_back.f_lineno:3d}'
def fl() -> str:
    f = inspect.currentframe().f_back
    return f'{f.f_code.co_name} {f.f_lineno:3d}'

import random as ran

import tkinter as tk  # It has radio buttons, pygame does not
import tkinter.font as font
from tkinter import ttk  # Use the newer widgets

canvasW = canvasH = 500  # canvas starts as a square, keeps the size between games.
gameIsPlaying = True

class TicTacToe:

    def __init__(self):
        global canvasW, canvasH
        # [Re]set the board.
        self.theBoard = [' '] * 9  # theBoard[0] is not used
        self.inputAgainstComputerOrOtherPerson()  # Sets self.next
        self.setMarkLetters()  # Sets self.mark
        self.turn = self.whoGoesFirst()  # Can be the Computer

        # Set up the playing board
        self.root = tk.Tk()
        # No way to modify the appearance of the title text.
        self.root.title('Welcome to Tic-Tac_Toe!')
        self.root.columnconfigure(0, weight=1)  # Get part of the extra space
        self.root.rowconfigure(0, weight=1)
        self.root.resizable(True, True)
        if self.turn == 'Computer':
            disp = 'The Computer went first'
        else:
            disp = f'{self.turn} goes first'

        self.label = tk.Label(self.root, text=disp, font='Times 16 bold', padx=5, pady=5)
        # self.label.grid(column=0, row=0, sticky=(tk.W))
        self.label.pack(fill=tk.NONE, expand=tk.NO, side=tk.TOP, anchor=tk.NW)

        # Canvas does not have geometry()
        self.canvas = tk.Canvas(self.root, bd=0, bg='#00C000', relief=tk.FLAT,
                    highlightthickness=0, insertwidth=0,
                    height=canvasH, width=canvasW)
        # self.canvas.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.canvas.pack(fill=tk.BOTH, expand=1)

        # It is enough to keep only these two bindings
        self.root.bind("<Configure>",         self.r_configure)  # The widget changed size
        self.root.bind("<ButtonRelease-1>",   self.r_buttonRelease_1)  # Left mouse clicked

        # print(f"{fl()} {self.root.geometry()=}")

        canvasW -= 1  # Triggers the line drawing

        self.alreadyAsked = False

        if self.turn == 'Computer':
            self.computerTurn()  # "theBoard" updated, nothing else, it will be displayed
            # in r_configure(), which will be called by tkinit

        # print(f"{fl()} BEF root.mainloop()")
        # breakpoint()  ###################################

        self.root.mainloop()
        # print(f"{fl()} AFT root.mainloop()")
    # END OF __init__() ===================================

    def cont(self, root, ans):
        global gameIsPlaying
        gameIsPlaying = ans
        # print(f'{fl()} {ans=} {gameIsPlaying=}')
        # Both roots will be destroyed.
        root.destroy()
        self.root.destroy()

    def askCont(self):  # If the buttons are in root, they can't be seen
        # print(f'{fl()} Start')
        r = tk.Tk()
        # r.geometry('300x100') Let the widgets fill up the place
        r.title('Welcome to Tic-Tac_Toe!')
        f = ttk.Frame(r)  # Try to use Frame()
        f.grid()
        l = ttk.Label(f, text = 'Do you want another game?', font = ("Courier", 14))
        # Don't use row, column, widgets will be arranged nicely
        l.grid(padx = 10, pady = 8)
        by = ttk.Button(f, text = 'YES', default = 'active',
                        command = lambda: self.cont(r, True))
        by.grid()  # Will be placed between Label and NO Button
        bn = ttk.Button(f, text = 'NO',
                        command = lambda: self.cont(r, False))
        bn.grid(pady = 12)
        r.update()  # Get the Widget parameters updated
        # print(f'{fl()} {l.winfo_geometry()=}')
        # print(f'{fl()} {by.winfo_geometry()=}')
        # print(f'{fl()} {bn.winfo_geometry()=}')
        # print(f'{fl()} BEF r.mainloop()')
        r.mainloop()
        # print(f'{fl()} AFT r.mainloop()')


    # At start, without doing anything, this was called:
    # 1. event.widget.winfo_name = 'tk'
    # 2. event.widget.winfo_name = '!label'
    # 3. event.widget.winfo_name = '!canvas'

    # After clicking on Canvas:
    # 1. event.widget.winfo_name = 'tk'
    # 2. r_buttnRelease_1 called event.widget.winfo_name = '!canvas'

    # This is called after a Canvas <Configure> was called; we don't have it here
    def r_configure(self, event):
        global canvasW, canvasH
        global gameIsPlaying

        # print(f'{fl()} {event.widget.winfo_name()=}  {gameIsPlaying=}')
        if gameIsPlaying == False and event.widget.winfo_name() == '!label':
            if self.alreadyAsked == False:
                self.alreadyAsked = True
                # print(f'{fl()} BEF root.after()')
                self.root.after(8000, self.askCont)
                # print(f'{fl()} AFT root.after()')

        # print(f'{fl()} {event.widget.winfo_name()=}  {event.width=}  {event.height=}')
        if event.widget.winfo_name() != '!canvas':
            # print()
            return
        if self.root.children['!label'].winfo_height() < 5:
            # print(f"{fl()} {self.root.children['!label'].winfo_height()=}\n")
            return  # It is NOT set, yet

        # breakpoint()
        w = event.width ; h = event.height
        # print(f'{fl()} {canvasW=} {canvasH=} {w=} {h=}')
        if canvasW == w and canvasH == h:
            return  # Nothing changed >>>>

        canvasW = w ; canvasH = h
        self.canvas.delete('all')

        bw = int(w/28); bh = int(h/28)
        sw = int((w-2*bw)/3); sh = int((h-2*bh)/3)
        lineW = max(int(min(w, h) / 64), 2)
        for i in (1, 2):  #     vertical                    horizontal
            for x in ((bw+i*sw, bh, bw+i*sw, h-bh), (bw, bh+i*sh, w-bw, bh+i*sh)):
                # print(f'{fl()} {x=}')
                self.canvas.create_line(x, width=lineW)  # No weight= parameter here

        # Set up the midpoints                    0  1  2
        self.mps = []  # List of tuples of (x,y)  3  4  5
        for j in (0,1,2):  #                      6  7  8
            for i in (0,1,2):
                self.mps.append((int(bw+sw/2+i*sw), int(bh+sh/2+j*sh)))

        """
        for xy in self.mps:
            print(f'{fl()} {xy=}')
        """

        # Reprint the Board
        for i in range(len(self.theBoard)):
            char = self.theBoard[i]
            if char == " ":
                continue
            x, y = self.mps[i]
            self.canvas.create_text(x, y, text=char,
                                font=f"Arial {int(min(canvasW,canvasH)/5)} bold")

        """
        for c in self.root.children:
            print(f'{fl()} root.children[{c}]={self.root.children[c]}')
            print(f'{fl()} root.children[{c}].winfo_geometry()='
                  f'{self.root.children[c].winfo_geometry()}')
            print(f'{fl()} root.children[{c}].winfo_height()='
                  f'{self.root.children[c].winfo_height()}')
            print(f'{fl()} root.children[{c}].winfo_width()='
                  f'{self.root.children[c].winfo_width()}')

        print(f'{fl()} {event.x=}  {event.y=}')
        print(f"{fl()} {self.root.geometry()=}")
        print(f"{fl()} {self.canvas['height']=}  {self.canvas['width']=}")
        print(f"{fl()} {self.canvas.winfo_geometry()=}\n")
        pass # To set breakpoint
        # breakpoint()
        """


    # After clicking on Canvas:
    # 1. r_configure called event.widget.winfo_name = 'tk'
    # 2. this is called event.widget.winfo_name = '!canvas'
    def r_buttonRelease_1(self, event):
        global canvasW, canvasH
        global gameIsPlaying

        # print(f'{fl()} {event.widget.winfo_name()=} {event.x=}  {event.y=}')
        # breakpoint()

        if event.widget.winfo_name() != '!canvas':
            if gameIsPlaying:
                self.label.configure(text = "Please, click on the board.")
            return

        # To which middle point it is closer?
        D = max(canvasW, canvasH)**2 ; X = event.x ; Y = event.y
        for i in range(len(self.mps)):
            x, y = self.mps[i]
            d = (X-x)**2 + (Y-y)**2
            if d < D:
                I = i ; D = d

        # Was it an empty place?
        if self.theBoard[I] != ' ':
            if gameIsPlaying:
                self.label.configure(text="Please, choose an empty place.")
            return

        char = self.mark[self.turn]
        self.theBoard[I] = char
        # print(f"{fl()} {I=} {self.mps[I]=}")
        x, y = self.mps[I]
        self.canvas.create_text(x, y, text = char,
                                font = f"Arial {int(min(canvasW,canvasH)/5)} bold")

        if self.isWinner(self.theBoard, char):
            # breakpoint()
            self.label.configure(text = f'The {self.turn} won.')
            gameIsPlaying = False
            return

        if self.isBoardFull(self.theBoard):
            gameIsPlaying = False
            self.label.configure(text='The game is a tie.')
            return

        # Switch to the other player, if it is the Computer, make its move
        self.turn = self.next[self.turn]
        if self.turn == 'Computer':
            field = self.computerTurn()  # It switches self.turn !
            if field != None:
                char = self.mark['Computer']
                # print(f"{fl()} {char=} {field=} {self.mps[field]=}")
                x, y = self.mps[field]
                self.canvas.create_text(x, y, text = char,
                                        font = f"Arial {int(min(canvasW, canvasH) / 5)} bold")
            return

        self.label.configure(text = f'{self.turn} turn ({self.mark[self.turn]})')

        # print(f"{fl()} {self.theBoard=}")
        # pass # To set breakpoint
        # breakpoint()
    # END OF r_buttonRelease_1(self, event)


    def __del__(self):  # destructor
        # print(f"{fl()} {gameIsPlaying=} {self.theBoard=}")
        # print(f"{fl()} Anything to do here?")
        pass  # Anything to here?


    def getchoice(self, root, v):
        if v == 1:
            self.next = {'Computer':'Player', 'Player':'Computer'}
        else:
            self.next = {'Player 1':'Player 2', 'Player 2':'Player 1'}
        root.destroy()


    def inputAgainstComputerOrOtherPerson(self):
        # Drow radio buttoms for the choice
        root = tk.Tk()
        root.geometry('300x100')
        root.title('Welcome to Tic-Tac_Toe!')
        v = tk.IntVar()
        label = ttk.Label(root, text = 'Choose playing against:', font = ("Courier", 14))
        label.grid(padx = 9)
        ttk.Radiobutton(root, text = 'Computer', variable=v,
                       command = lambda: self.getchoice(root, 1)
                       ).grid(column=0, sticky = (tk.W), padx=9)
        ttk.Radiobutton(root, text = 'Anoter person', variable=v,
                       command = lambda: self.getchoice(root, 2)
                       ).grid(column=0, sticky = (tk.W), padx=9)

        root.mainloop()


    def getletter(self, root, v):
        # breakpoint()
        k = self.player
        l = 'X' if v == 1 else 'O'
        self.mark = {k:l, self.next[k]:{'O':'X','X':'O'}[l]}
        root.destroy()


    def setMarkLetters(self):
        # breakpoint()
        while True:
            for k in self.next.keys():
                if ran.randint(0, 1) == 0:
                    break
            # According to the Python doc, this is legal, to use a loop variable AFTER the loop
            if k != 'Computer':
               break

        # Lets pick letter
        t = f'{k}, do you want to be?' if k != 'Player' else 'Do you want to be?'
        self.player = k
        # Drow radio buttoms for the choice
        root = tk.Tk()
        root.geometry('360x100')
        root.title('Welcome to Tic-Tac_Toe!')
        v = tk.IntVar()
        label = tk.Label(root)
        label.config(text=t, font=("Courier", 14), anchor=tk.N)
        label.pack(anchor=tk.W)
        tk.Radiobutton(root, text='X', padx=10, variable=v, value=1,
                       command = lambda: self.getletter(root, 1)
                       ).pack(anchor=tk.W)
        tk.Radiobutton(root, text='O', padx=10, variable=v, value=2,
                       command = lambda: self.getletter(root, 2)
                       ).pack(anchor=tk.W)
        root.mainloop()
        # breakpoint()


    def whoGoesFirst(self) -> str:
        # Randomly choose who goes first.
        for k in self.next.keys():
            if ran.randint(0, 1) == 0:
                break
        return k
    #                                     0  1  2
    #                                     3  4  5
    def isWinner(self, board, letter):  # 6  7  8
        # breakpoint()
        # Given a board and a player's letter, this function returns True if that player has won.
        l = ((0,1,2), (3,4,5), (6,7,8),
             (0,3,6), (1,4,7), (2,5,8),
             (0,4,8), (2,4,6))         # Lines
        for i in l:
            for j in i:
                if board[j] != letter:
                    break
            else:  # It is executed if all letters matched
                return True  # A line is found
        return False


    def isSpaceFree(self, board, move):
        # Return True if the passed move is free on the passed board.
        return board[move] == ' '


    def chooseRandomMoveFromTuple(self, board, movesTuple):
        # Returns a valid move from the passed tuple on the passed board.
        # Returns None if there is no valid move.
        possibleMoves = []
        for i in movesTuple:
            if self.isSpaceFree(board, i):
                possibleMoves.append(i)

        return ran.choice(possibleMoves) if len(possibleMoves) != 0 else None


    def getComputerMove(self, board, computerLetter):
        # Given a board and the computer's letter, determine where to move and return that move.
        playerLetter = 'O' if computerLetter == 'X' else 'X'

        # Here is the algorithm for our Tic-Tac-Toe AI:
        # First, check if we can win in the next move.
        for i in range(9):
            boardCopy = board.copy()
            if self.isSpaceFree(boardCopy, i):
                boardCopy[i] = computerLetter
                if self.isWinner(boardCopy, computerLetter):
                    return i

        # Check if the player could win on their next move and block them.
        for i in range(9):
            boardCopy = board.copy()
            if self.isSpaceFree(boardCopy, i):
                boardCopy[i] = playerLetter
                if self.isWinner(boardCopy, playerLetter):
                    return i

        # Try to take one of the corners, if they are free.
        move = self.chooseRandomMoveFromTuple(board, (0, 2, 6, 8))  # Corners
        if move != None:
            return move

        # Try to take the center, if it is free.
        if self.isSpaceFree(board, 4):
            return 4

        # Move on one of the sides.
        # breakpoint()
        return self.chooseRandomMoveFromTuple(board, (1, 3, 5, 7))


    def isBoardFull(self, board) -> bool:
        # Return True if every space on the board has been taken. Otherwise, return False.
        for i in range(9):
            if self.isSpaceFree(board, i):
                return False
        return True


    # It updates only "theBoard"
    def computerTurn(self):  # Returns the field number or None, if the game is over
        global gameIsPlaying
        char = self.mark['Computer']
        if self.isBoardFull(self.theBoard):
            gameIsPlaying = False

            if self.isWinner(self.theBoard, char):
                self.label.configure(text='The computer won.')
            else:
                self.label.configure(text = 'The game is a tie.')

            # print(f"{fl()} {gameIsPlaying=} {self.theBoard=}")
            return None

        field = self.getComputerMove(self.theBoard, char)
        self.theBoard[field] = char
        # print(f"{fl()} {char=} {field=} {self.theBoard=}")

        if self.isWinner(self.theBoard, char):
            # breakpoint()
            self.label.configure(text = 'The computer won.')
            gameIsPlaying = False
        else:
            # breakpoint()
            if self.isBoardFull(self.theBoard):
                self.label.configure(text = 'The game is a tie.')
                gameIsPlaying = False
            else:
                self.turn = self.next[self.turn]  # The next player

        return field

# class TicTacToe ENDS here ============================

while True:
    # print(f'{fl()} BEF t = TicTacToe()')
    t = TicTacToe()
    # print(f'{fl()} {gameIsPlaying=} AFT t = TicTacToe()')

    if gameIsPlaying == False:
        break

# print(f'{fl()} AFT "while True" loop')
# breakpoint()
