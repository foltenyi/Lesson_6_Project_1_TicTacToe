###########################################################################
#
# tic_tac_toe_00.py
#
# CS-043-T001 Part 2 - Unit 6 - Final Collaborative Project: 1-3
#
# Play against the computer
# Make it to use class.
# Make it to play against another person or the computer.
#
# The base copied fom: Sweigart, Al.
# Invent Your Own Computer Games with Python, 4E (p. 123). No Starch Press.
#
###########################################################################
#
# Tic-Tac-Toe

from os import path
import inspect
def ln() -> str:
    return f'{inspect.currentframe().f_back.f_lineno:3d}'
def fl() -> str:
    return (f'{path.basename(inspect.stack()[1].filename)} '
            f'{inspect.currentframe().f_back.f_lineno:3d}')

import random


class TicTacToe:

    def __init__(self):
        # Reset the board.
        self.theBoard = [' '] * 10  # theBoard[0] is not used
        self.inputAgainstComputerOrOtherPerson()  # Sets self.next
        self.setMarkLetters()  # Sets self.mark
        self.turn = self.whoGoesFirst()
        print('The ' + self.turn + ' will go first.')

    def drawBoard(self):
        # This function prints out the board that it was passed.
        # "board" is a list of 10 strings representing the board (ignore index 0).
        b = self.theBoard
        print(b[7] + '|' + b[8] + '|' + b[9])
        print('-+-+-')
        print(b[4] + '|' + b[5] + '|' + b[6])
        print('-+-+-')
        print(b[1] + '|' + b[2] + '|' + b[3])

    def inputAgainstComputerOrOtherPerson(self):
        _l = ''
        while not _l in ('C', 'P'):
            print("Do you want to play against computer, 'C' or other person, 'P'?")
            _l = input().upper()

        if _l == 'C':
            self.next = {'Computer':'Player', 'Player':'Computer'}
        else:
            self.next = {'Player 1':'Player 2', 'Player 2':'Player 1'}

    def setMarkLetters(self):
        while True:
            for k in self.next.keys():
                if random.randint(0, 1) == 0:
                    break

            # According to the Python doc, this is legal, to use a loop variable AFTER the loop
            if k != 'Computer':
               break

        # Lets the player type which letter they want to be.
        _l = ''
        while not (_l == 'X' or _l == 'O'):
            if k == 'Player':
                print('Do you want to be X or O?')
            else:
                print(f'{k}, do you want to be X or O?')
            _l = input().upper()

        self.mark = {k:_l, self.next[k]:{'O':'X','X':'O'}[_l]}

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
        self.drawBoard()
        _move = self.getPlayerMove(self.theBoard, player)
        self.theBoard[ _move] = self.mark[player]

        if self.isWinner(self.theBoard, self.mark[player]):
            self.drawBoard()
            print('Hooray! You have won the game!')
            return False
        else:
            if self.isBoardFull(self.theBoard):
                self.drawBoard()
                print('The game is a tie!')
                return False
            else:
                self.turn = self.next[self.turn]

        return True

    def computerTurn(self) -> bool:  # The gameIsPlaying new value:
        _cLetter = self.mark['Computer']
        _move = self.getComputerMove(self.theBoard, _cLetter)
        self.theBoard[_move] = _cLetter

        if self.isWinner(self.theBoard, _cLetter):
            self.drawBoard()
            print('The computer has beaten you! You lose.')
            return False
        else:
            if self.isBoardFull(self.theBoard):
                self.drawBoard()
                print('The game is a tie!')
                return False
            else:
                self.turn = self.next[self.turn]

        return True

# class TicTacToe ENDS here ============================

print('Welcome to Tic-Tac-Toe!')

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
