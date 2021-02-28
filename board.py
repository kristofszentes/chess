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

    def white_is_checked(self):
        for i in range(8):
            for j in range(8):
                if 
        return False
