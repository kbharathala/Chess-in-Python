from chess import Chess


class Piece(object):

    def __init__(self, color):
        self.color = color

    def possible_moves(self, moveFrom, pieceGrid):
        raise NotImplementedError  # overridden in all of the subclasses

    def protected(self, moveFrom, pieceGrid):
        raise NotImplementedError  # overridden in all of the subclasses


class Pawn(Piece):

    def __init__(self, color):
        super(Pawn, self).__init__(color)

    def possible_moves(self, moveFrom, pieceGrid):
        moves = []
        x1, y1 = moveFrom[0], moveFrom[1]
        if(self.color == "white"):
            if(pieceGrid[x1-1][y1] is None):
                moves.append((x1-1, y1))
            if(x1 == 6 and pieceGrid[x1-2][y1] is None):
                moves.append((x1-2, y1))
            if(y1 != 7 and pieceGrid[x1-1][y1+1] is not None and
                    pieceGrid[x1-1][y1+1].color == "black"):
                moves.append((x1-1, y1+1))
            if(y1 != 0 and pieceGrid[x1-1][y1-1] is not None and
                    pieceGrid[x1-1][y1-1].color == "black"):
                moves.append((x1-1, y1-1))
        else:
            if(pieceGrid[x1+1][y1] is None):
                moves.append((x1+1, y1))
            if(x1 == 1 and pieceGrid[x1+2][y1] is None):
                moves.append((x1+2, y1))
            if(y1 != 7 and pieceGrid[x1+1][y1+1] is not None and
                    pieceGrid[x1+1][y1+1].color == "white"):
                moves.append((x1+1, y1+1))
            if(y1 != 0 and pieceGrid[x1+1][y1-1] is not None and
                    pieceGrid[x1+1][y1-1].color == "white"):
                moves.append((x1+1, y1-1))
        return moves

    def protected(self, moveFrom, pieceGrid):
        x1, y1 = moveFrom[0], moveFrom[1]
        protected = []
        if self.color == "white":
            protected.append((x1-1, y1+1))
            protected.append((x1-1, y1-1))
        else:
            protected.append((x1+1, y1+1))
            protected.append((x1+1, y1-1))
        return protected


class Knight(Piece):

    def __init__(self, color):
        super(Knight, self).__init__(color)

    def possible_moves(self, moveFrom, pieceGrid):
        x1, y1 = moveFrom[0], moveFrom[1]
        moves = []
        act_moves = []
        moves.append((x1+2, y1+1))
        moves.append((x1+2, y1-1))
        moves.append((x1-2, y1+1))
        moves.append((x1-2, y1-1))
        moves.append((x1+1, y1+2))
        moves.append((x1+1, y1-2))
        moves.append((x1-1, y1+2))
        moves.append((x1-1, y1-2))
        for move in moves:
            x, y = move[0], move[1]
            if x >= 0 and x <= 7 and y >= 0 and y <= 7:
                if(pieceGrid[move[0]][move[1]] is None or
                        pieceGrid[move[0]][move[1]].color != self.color):
                    act_moves.append(move)
        return act_moves

    def protected(self, moveFrom, pieceGrid):
        x1, y1 = moveFrom[0], moveFrom[1]
        moves = []
        moves.append((x1+2, y1+1))
        moves.append((x1+2, y1-1))
        moves.append((x1-2, y1+1))
        moves.append((x1-2, y1-1))
        moves.append((x1+1, y1+2))
        moves.append((x1+1, y1-2))
        moves.append((x1-1, y1+2))
        moves.append((x1-1, y1-2))
        return moves


class Rook(Piece):

    def __init__(self, color):
        super(Rook, self).__init__(color)

    def possible_moves(self, moveFrom, pieceGrid):
        x1, y1 = moveFrom[0], moveFrom[1]
        moves = []
        for i in range(1, 8):
            if x1+i > 7 or pieceGrid[x1+i][y1] is not None:
                if x1+i <= 7 and pieceGrid[x1+i][y1].color != self.color:
                    moves.append((x1+i, y1))
                break
            moves.append((x1+i, y1))
        for i in range(1, 8):
            if x1-i < 0 or pieceGrid[x1-i][y1] is not None:
                if x1-i >= 0 and pieceGrid[x1-i][y1].color != self.color:
                    moves.append((x1-i, y1))
                break
            moves.append((x1-i, y1))
        for i in range(1, 8):
            if y1+i > 7 or pieceGrid[x1][y1+i] is not None:
                if y1+i <= 7 and pieceGrid[x1][y1+i].color != self.color:
                    moves.append((x1, y1+i))
                break
            moves.append((x1, y1+i))
        for i in range(1, 8):
            if y1-i < 0 or pieceGrid[x1][y1-i] is not None:
                if y1-i >= 0 and pieceGrid[x1][y1-i].color != self.color:
                    moves.append((x1, y1-i))
                break
            moves.append((x1, y1-i))
        return moves

    def protected(self, moveFrom, pieceGrid):
        x1, y1 = moveFrom[0], moveFrom[1]
        moves = []
        for i in range(1, 8):
            if x1+i > 7 or pieceGrid[x1+i][y1] is not None:
                if x1+i <= 7:
                    moves.append((x1+i, y1))
                break
            moves.append((x1+i, y1))
        for i in range(1, 8):
            if x1-i < 0 or pieceGrid[x1-i][y1] is not None:
                if x1-i >= 0:
                    moves.append((x1-i, y1))
                break
            moves.append((x1-i, y1))
        for i in range(1, 8):
            if y1+i > 7 or pieceGrid[x1][y1+i] is not None:
                if y1+i <= 7:
                    moves.append((x1, y1+i))
                break
            moves.append((x1, y1+i))
        for i in range(1, 8):
            if y1-i < 0 or pieceGrid[x1][y1-i] is not None:
                if y1-i >= 0:
                    moves.append((x1, y1-i))
                break
            moves.append((x1, y1-i))
        return moves


class Bishop(Piece):

    def __init__(self, color):
        super(Bishop, self).__init__(color)

    def possible_moves(self, moveFrom, pieceGrid):
        x1, y1 = moveFrom[0], moveFrom[1]
        moves = []
        for i in range(1, 8):
            if x1+i > 7 or y1+i > 7 or pieceGrid[x1+i][y1+i] is not None:
                if x1+i <= 7 and y1+i <= 7:
                    if(pieceGrid[x1+i][y1+i].color != self.color):
                        moves.append((x1+i, y1+i))
                break
            moves.append((x1+i, y1+i))
        for i in range(1, 8):
            if x1-i < 0 or y1-i < 0 or pieceGrid[x1-i][y1-i] is not None:
                if x1-i >= 0 and y1-i >= 0:
                    if(pieceGrid[x1-i][y1-i].color != self.color):
                        moves.append((x1-i, y1-i))
                break
            moves.append((x1-i, y1-i))
        for i in range(1, 8):
            if x1-i < 0 or y1+i > 7 or pieceGrid[x1-i][y1+i] is not None:
                if x1-i >= 0 and y1+i <= 7:
                    if(pieceGrid[x1-i][y1+i].color != self.color):
                        moves.append((x1-i, y1+i))
                break
            moves.append((x1-i, y1+i))
        for i in range(1, 8):
            if x1+i > 7 or y1-i < 0 or pieceGrid[x1+i][y1-i] is not None:
                if x1+i <= 7 and y1-i >= 0:
                    if(pieceGrid[x1+i][y1-i].color != self.color):
                        moves.append((x1+i, y1-i))
                break
            moves.append((x1+i, y1-i))
        return moves

    def protected(self, moveFrom, pieceGrid):
        x1, y1 = moveFrom[0], moveFrom[1]
        moves = []
        for i in range(1, 8):
            if x1+i > 7 or y1+i > 7 or pieceGrid[x1+i][y1+i] is not None:
                if x1+i <= 7 and y1+i <= 7:
                    moves.append((x1+i, y1+i))
                break
            moves.append((x1+i, y1+i))
        for i in range(1, 8):
            if x1-i < 0 or y1-i < 0 or pieceGrid[x1-i][y1-i] is not None:
                if x1-i >= 0 and y1-i >= 0:
                    moves.append((x1-i, y1-i))
                break
            moves.append((x1-i, y1-i))
        for i in range(1, 8):
            if x1-i < 0 or y1+i > 7 or pieceGrid[x1-i][y1+i] is not None:
                if x1-i >= 0 and y1+i <= 7:
                    moves.append((x1-i, y1+i))
                break
            moves.append((x1-i, y1+i))
        for i in range(1, 8):
            if x1+i > 7 or y1-i < 0 or pieceGrid[x1+i][y1-i] is not None:
                if x1+i <= 7 and y1-i >= 0:
                    moves.append((x1+i, y1-i))
                break
            moves.append((x1+i, y1-i))
        return moves


class Queen(Piece):

    def __init__(self, color):
        super(Queen, self).__init__(color)

    def possible_moves(self, moveFrom, pieceGrid):
        rook = Rook(color=self.color)
        bishop = Bishop(color=self.color)
        r_moves = rook.possible_moves(moveFrom=moveFrom, pieceGrid=pieceGrid)
        b_moves = bishop.possible_moves(moveFrom=moveFrom, pieceGrid=pieceGrid)
        return r_moves + b_moves

    def protected(self, moveFrom, pieceGrid):
        rook = Rook(color=self.color)
        bishop = Bishop(color=self.color)
        r_moves = rook.protected(moveFrom=moveFrom, pieceGrid=pieceGrid)
        b_moves = bishop.protected(moveFrom=moveFrom, pieceGrid=pieceGrid)
        return r_moves + b_moves


class King(Piece):

    def __init__(self, color):
        super(King, self).__init__(color)

    def possible_moves(self, moveFrom, pieceGrid):
        x1, y1 = moveFrom[0], moveFrom[1]
        moves = []
        act_moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                moves.append((x1+i, y1+j))
        for move in moves:
            x, y = move[0], move[1]
            if x >= 0 and x <= 7 and y >= 0 and y <= 7:
                if(pieceGrid[move[0]][move[1]] is None or
                        pieceGrid[move[0]][move[1]].color != self.color):
                    act_moves.append(move)
        return act_moves

    def protected(self, moveFrom, pieceGrid):
        x1, y1 = moveFrom[0], moveFrom[1]
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                moves.append((x1+i, y1+j))
        return moves
