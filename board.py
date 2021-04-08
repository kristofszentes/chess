from pieces import *

class Board():

    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.white_in_check = False
        self.black_in_check = False

    def init_game(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]

        #Placing the pieces
        self.placement()

    #Placing the initial pieces
    def placement(self):
        #Placing pawns
        for i in range(8):
            self.board[1][i] = Pawn((1, i), False, self)

            self.board[6][i] = Pawn((6, i), True, self)

        self.board[0][0] = Rook((0, 0), False, self)
        self.board[0][1] = Knight((0, 1), False, self)
        self.board[0][2] = Bishop((0, 2), False, self)
        self.board[0][3] = Queen((0, 3), False, self)
        self.board[0][4] = King((0, 4), False, self)
        self.board[0][5] = Bishop((0, 5), False, self)
        self.board[0][6] = Knight((0, 6), False, self)
        self.board[0][7] = Rook((0, 7), False, self)
        
        #other white pieces
        self.board[7][0] = Rook((7, 0), True, self)
        self.board[7][1] = Knight((7, 1), True, self)
        self.board[7][2] = Bishop((7, 2), True, self)
        self.board[7][3] = Queen((7, 3), True, self)
        self.board[7][4] = King((7, 4), True, self)
        self.board[7][5] = Bishop((7, 5), True, self)
        self.board[7][6] = Knight((7, 6), True, self)
        self.board[7][7] = Rook((7, 7), True, self)

    def get_black_pieces(self):
        pieces = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece != None and not piece.white:
                    pieces.append(piece)
        return pieces

    def get_white_pieces(self):
        pieces = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece != None and piece.white:
                    pieces.append(piece)
        return pieces

    #returns the coords of a king, color can be 'white' or 'black'
    def get_king_coord(self, color):
        col = True if color == 'white' else False
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece!= None and piece.white == col and isinstance(piece,King):
                    return (i,j)

    def check_pawn_to_queen(self):
        for i in [0,7]:
            for j in range(8):
                piece = self.board[i][j]
                if piece != None and isinstance(piece,Pawn):
                    new_queen = Queen((i,j), piece.white, self)
                    self.board[i][j] = new_queen

    #tells if a player is checked, color can be 'white' or 'black'
    def is_checked(self, color):
        col = True if color == 'white' else False
        k_coord = self.get_king_coord(color)
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece != None and piece.white != col:
                    if k_coord in piece.is_attacking():
                        return True
        return False

    def is_mated(self, color):
        col = True if color == 'white' else False

    def copy(self):
        new_board = Board()
        for i in range(8):
            for j in range(8):
                new_board.board[i][j] = self.board[i][j]

        return new_board
