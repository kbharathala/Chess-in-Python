import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import sys
import piece


class Chess(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.tiles = []
        for each in range(0, 8):
            self.tiles.append([])

        self.pieceGrid = []
        for i in range(0, 8):
            self.pieceGrid.append([])
            for j in range(0, 8):
                self.pieceGrid[i].append(None)

        self.firstClick = True
        self.curr = 'A1'
        self.gridLocation = (0, 0)
        self.turnColor = "white"
        self.moveList = []
        self.moveNumber = 1
        self.movingPiece = 'k'
        self.captureTurn = False
        self.possible = []

        master.title("Chess")
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
        r = 0
        c = 0
        for number in reversed(self.numbers):
            for letter in self.letters:
                if (r+c) % 2 == 1:
                    bg = "black"
                else:
                    bg = "white"
                pos = letter+number
                cmd = lambda pos = pos: self.buttonClick(pos)
                button = Button(master, command=cmd, width=6,
                                height=3, bg=bg, relief="flat")
                button.grid(row=r, column=c)
                self.tiles[r].append(button)
                c += 1
            r += 1
            c = 0
        self.initializeBoard()

    def tileColor(self, x, y):
        if (x+y) % 2 == 1:
            return "white"
        else:
            return "black"

    def initializeBoard(self):
        backRow = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        frontRow = ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']

        for i in range(0, 8):
            self.tiles[0][i].config(text=backRow[i], fg=self.tileColor(0, i))
            self.tiles[1][i].config(text=frontRow[i], fg=self.tileColor(1, i))
            self.tiles[7][i].config(text=backRow[i].upper(),
                                    fg=self.tileColor(7, i))
            self.tiles[6][i].config(text=frontRow[i].upper(),
                                    fg=self.tileColor(6, i))

        self.pieceGrid[0][0] = piece.Rook("black")
        self.pieceGrid[0][1] = piece.Knight("black")
        self.pieceGrid[0][2] = piece.Bishop("black")
        self.pieceGrid[0][3] = piece.Queen("black")
        self.pieceGrid[0][4] = piece.King("black")
        self.pieceGrid[0][5] = piece.Bishop("black")
        self.pieceGrid[0][6] = piece.Knight("black")
        self.pieceGrid[0][7] = piece.Rook("black")
        for i in range(0, 8):
            self.pieceGrid[1][i] = piece.Pawn("black")

        self.pieceGrid[7][0] = piece.Rook("white")
        self.pieceGrid[7][1] = piece.Knight("white")
        self.pieceGrid[7][2] = piece.Bishop("white")
        self.pieceGrid[7][3] = piece.Queen("white")
        self.pieceGrid[7][4] = piece.King("white")
        self.pieceGrid[7][5] = piece.Bishop("white")
        self.pieceGrid[7][6] = piece.Knight("white")
        self.pieceGrid[7][7] = piece.Rook("white")
        for i in range(0, 8):
            self.pieceGrid[6][i] = piece.Pawn("white")

    def getProtectedSquares(self, color):
        protected = []
        for x in range(0, 8):
            for y in range(0, 8):
                piece = self.pieceGrid[x][y]
                if piece is not None and piece.color != color:
                    pos = (x, y)
                    protected += piece.protected(moveFrom=pos,
                                                 pieceGrid=self.pieceGrid)
        return protected

    def isCheckMate(self, color):
        total = 0
        for x in range(0, 8):
            for y in range(0, 8):
                piece = self.pieceGrid[x][y]
                if piece is not None and piece.color == self.turnColor:
                    total += len(self.get_possible(piece=piece, moveTo=(x, y)))
        if total == 0:
            sys.stdout.write("CHECKMATE")
            sys.stdout.flush()
        return

    def getKingPosition(self, color):
        for x in range(0, 8):
            for y in range(0, 8):
                piece = self.pieceGrid[x][y]
                if (piece is not None and piece.color == color and
                        self.tiles[x][y].config('text')[-1].lower() == 'k'):
                    return (x, y)

    def get_possible(self, piece, moveTo):
        possible = piece.possible_moves(moveFrom=moveTo,
                                        pieceGrid=self.pieceGrid)
        remove = []
        x, y = moveTo[0], moveTo[1]
        for move in possible:
            x1, y1 = move[0], move[1]
            piece1 = self.pieceGrid[x1][y1]
            self.pieceGrid[x][y] = None
            self.pieceGrid[x1][y1] = piece
            if self.tiles[x][y].config('text')[-1].lower() == 'k':
                if move in self.getProtectedSquares(self.turnColor):
                    remove.append(move)
            else:
                if (self.getKingPosition(self.turnColor) in
                        self.getProtectedSquares(self.turnColor)):
                    remove.append(move)
            self.pieceGrid[x][y] = piece
            self.pieceGrid[x1][y1] = piece1
        for move in remove:
            possible.remove(move)
        return possible

    def buttonClick(self, pos):
        x = 8-int(pos[1])
        y = self.letters.index(pos[0])
        moveTo = (x, y)
        if(self.firstClick):
            piece = self.pieceGrid[x][y]
            if(piece is not None and piece.color == self.turnColor):
                self.possible = self.get_possible(piece, moveTo)
                for move in self.possible:
                    self.tiles[move[0]][move[1]].config(bg="blue")
                if len(self.possible) != 0:
                    curr_tile = self.tiles[x][y]
                    curr_tile.config(bg="red")
                    self.movingPiece = curr_tile.config('text')[-1].upper()
                    if self.movingPiece == 'P':
                        self.movingPiece = ''
                    self.curr = pos  # this stores notation
                    self.gridLocation = moveTo  # this stores grid location
                    self.firstClick = not(self.firstClick)
        else:
            x1 = self.gridLocation[0]
            y1 = self.gridLocation[1]
            if(pos != self.curr and self.tiles[x][y].cget('bg') == "blue"):
                piece = self.pieceGrid[x1][y1]
                if self.pieceGrid[x][y] is not None:
                    self.captureTurn = True
                text = self.tiles[x1][y1].config('text')[-1]
                self.tiles[x][y].config(text=text, fg=self.tileColor(x, y))
                self.tiles[x1][y1].config(text='')
                self.pieceGrid[x][y] = piece
                self.pieceGrid[x1][y1] = None
                if self.captureTurn:
                    if self.movingPiece == '':
                        self.movingPiece = self.curr[0]
                    self.moveList.append(self.movingPiece + "x" + pos)
                    gap = " "
                else:
                    self.moveList.append(self.movingPiece + pos)
                    gap = "  "
                if self.movingPiece == '':
                    gap = gap + " "
                if self.turnColor == "white":
                    sys.stdout.write(str(self.moveNumber) + ". ")
                    sys.stdout.write(self.moveList[2*self.moveNumber-2] + gap)
                    self.turnColor = "black"
                else:
                    sys.stdout.write(self.moveList[2*self.moveNumber-1] + '\n')
                    self.moveNumber = self.moveNumber + 1
                    self.turnColor = "white"
                self.captureTurn = False
                sys.stdout.flush()
                self.isCheckMate(self.turnColor)
            self.firstClick = not(self.firstClick)
            bg = self.tileColor(x1, y1+1)
            self.tiles[x1][y1].config(bg=bg)
            for move in self.possible:
                bg = self.tileColor(move[0], move[1]+1)
                self.tiles[move[0]][move[1]].config(bg=bg)


def chess_main():
    root = Tk()
    app = Chess(master=root)
    app.mainloop()

if __name__ == '__main__':
    chess_main()
