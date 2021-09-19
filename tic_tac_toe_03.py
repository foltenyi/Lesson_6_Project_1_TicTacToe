###########################################################################
#
# tic_tac_toe_00.py
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
import pygame
from pygame.locals import *

import inspect
def ln() -> str:
    return f'{inspect.currentframe().f_back.f_lineno:3d}'

import random

pygame.init()  # Don't fordet pygame.quit()

import tkinter as tk  # It has radio buttons, pygame does not
import tkinter.font as font
from tkinter import ttk  # Use the newer widgets

# Starting

class TicTacToe:

    def __init__(self):
        # Reset the board.
        self.theBoard = [' '] * 10  # theBoard[0] is not used
        self.inputAgainstComputerOrOtherPerson()  # Sets self.next
        self.setMarkLetters()  # Sets self.mark
        self.turn = self.whoGoesFirst()

    def drawBoard(self, disp):
        breakpoint()
        self.root = tk.Tk()
        self.root.title('Welcome to Tic-Tac_Toe!')
        frame = ttk.Frame(self.root, padding='4 4 12 12')  # In pixels, how much extra space
        frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.root.columnconfigure(0, weight=1)  # weight=1 get 1/4th of the extra space
        self.root.rowconfigure(0, weight=1)
        ttk.Label(frame, text=disp).grid(column=1, row=1, sticky=(tk.W, tk.E))
        print(f'{ln()} {self.root.winfo_width()=}')
        print(f'{ln()} {frame.winfo_width()=}')



        self.root.mainloop()

        """
        # This function prints out the board that it was passed.
        # "board" is a list of 10 strings representing the board (ignore index 0).
        b = self.theBoard
        print(b[7] + '|' + b[8] + '|' + b[9])
        print('-+-+-')
        print(b[4] + '|' + b[5] + '|' + b[6])
        print('-+-+-')
        print(b[1] + '|' + b[2] + '|' + b[3])
        """

    def getchoice(self, root, v):
        # breakpoint()
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
        label = tk.Label(root)
        label.config(text='Choose playing against:',
                     font=("Courier",14), anchor=tk.W)
        label.pack(anchor=tk.N)

        tk.Radiobutton(root, text='Computer', padx=10, variable=v, value=1,
                       command = lambda: self.getchoice(root, 1)
                       ).pack(anchor=tk.W)
        tk.Radiobutton(root, text='Anoter person', padx=10, variable=v, value=2,
                       command = lambda: self.getchoice(root, 2)
                       ).pack(anchor=tk.W)
        root.mainloop()

    def getletter(self, root, v):
        k = self.player
        l = 'X' if v == 1 else 'O'
        self.mark = {k:l, self.next[k]:{'O':'X','X':'O'}[l]}
        root.destroy()
        # breakpoint()

    def setMarkLetters(self):
        while True:
            for k in self.next.keys():
                if random.randint(0, 1) == 0:
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
            if random.randint(0, 1) == 0:
                break
        return k

    def isWinner(self, board, letter):
        # Given a board and a player's letter, this function returns True if that player has won.
        l = ((7,8,9), (4,5,6), (1,2,3), (7,4,1), (8,5,2), (9,6,3), (7,5,3), (9,5,1))  # Lines
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

    def getPlayerMove(self, board, player):
        # Let the player enter their move.
        _move = ' '
        while _move not in '1 2 3 4 5 6 7 8 9'.split() or not self.isSpaceFree(board, int(_move)):
            if player == 'Player':
                print('What is your next move? (1-9)')
            else:
                print(f'{player}, please enter your next move? (1-9)')
            _move = input()
            if not _move.isdigit():
                print(f"Enter a digit (not '{_move}')")
                continue
            if not self.isSpaceFree(board, int(_move)):
                print(f'board[{int(_move)}] is not free')

        return int(_move)

    def chooseRandomMoveFromTuple(self, board, movesTuple):
        # Returns a valid move from the passed tuple on the passed board.
        # Returns None if there is no valid move.
        possibleMoves = []
        for i in movesTuple:
            if self.isSpaceFree(board, i):
                possibleMoves.append(i)

        return random.choice(possibleMoves) if len(possibleMoves) != 0 else None

    def getComputerMove(self, board, computerLetter):
        # Given a board and the computer's letter, determine where to move and return that move.
        playerLetter = 'O' if computerLetter == 'X' else 'X'

        # Here is the algorithm for our Tic-Tac-Toe AI:
        # First, check if we can win in the next move.
        for i in range(1, 10):
            boardCopy = board.copy()
            if self.isSpaceFree(boardCopy, i):
                boardCopy[i] = computerLetter
                if self.isWinner(boardCopy, computerLetter):
                    return i

        # Check if the player could win on their next move and block them.
        for i in range(1, 10):
            boardCopy = board.copy()
            if self.isSpaceFree(boardCopy, i):
                boardCopy[i] = playerLetter
                if self.isWinner(boardCopy, playerLetter):
                    return i

        # Try to take one of the corners, if they are free.
        move = self.chooseRandomMoveFromTuple(board, (1, 3, 7, 9))
        if move != None:
            return move

        # Try to take the center, if it is free.
        if self.isSpaceFree(board, 5):
            return 5

        # Move on one of the sides.
        return self.chooseRandomMoveFromTuple(board, (2, 4, 6, 8))

    def isBoardFull(self, board) -> bool:
        # Return True if every space on the board has been taken. Otherwise, return False.
        for i in range(1, 10):
            if self.isSpaceFree(board, i):
                return False
        return True

    def playerTurn(self, player) -> bool:  # The gameIsPlaying new value
        t = f"{self.turn}, p" if self.turn != "Player" else 'P'
        t += 'lease click on a square.'
        self.drawBoard(t)
        _move = self.getPlayerMove(self.theBoard, player)
        self.theBoard[ _move] = self.mark[player]

        if self.isWinner(self.theBoard, self.mark[player]):
            self.drawBoard('You have won the game!')
            return False
        else:
            if self.isBoardFull(self.theBoard):
                self.drawBoard('The game is a tie!')
                return False
            else:
                self.turn = self.next[self.turn]

        return True

    def computerTurn(self) -> bool:  # The gameIsPlaying new value:
        _cLetter = self.mark['Computer']
        _move = self.getComputerMove(self.theBoard, _cLetter)
        self.theBoard[_move] = _cLetter

        if self.isWinner(self.theBoard, _cLetter):
            self.drawBoard('The computer won.')
            return False
        else:
            if self.isBoardFull(self.theBoard):
                self.drawBoard('The game is a tie.')
                return False
            else:
                self.turn = self.next[self.turn]

        return True

# class TicTacToe ENDS here ============================

while True:
    t = TicTacToe()
    gameIsPlaying = True

    while gameIsPlaying:
        if t.turn != 'Computer':
            gameIsPlaying = t.playerTurn(t.turn)
        else:
            gameIsPlaying = t.computerTurn()

    print('Do you want to play again? (yes or no)')
    if not input().lower().startswith('y'):
        break
