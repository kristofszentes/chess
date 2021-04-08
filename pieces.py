import pygame
import os

class Piece():

    def __init__(self, position, white, board):
        self.line = position[0]
        self.column = position[1]
        self.white = white
        self.board = board

    def is_on_board(self, x, y):
        return x <= 7 and x >= 0 and y <= 7 and y >= 0

    def move(self, x ,y):
        self.board.board[x][y] = self
        self.board.board[self.line][self.column] = None
        self.line = x
        self.column = y

class Pawn(Piece):

    def __init__(self, position, white, board):
        Piece.__init__(self, position, white, board)
        self.hasMoved = False
        
        #Loading the sprite
        if self.white:
            self.surface = pygame.image.load(os.path.join("sprites","white_pawn.png"))
        else:
            self.surface = pygame.image.load(os.path.join("sprites", "black_pawn.png"))
        
        #resizing it
        self.surface = pygame.transform.scale(self.surface, (80,80))

    def can_move_to(self):
        moves = []
        att_moves = []
        if self.white:
            if self.is_on_board(self.line -1, self.column):
                moves.append((self.line - 1, self.column))
            if not self.hasMoved:
                moves.append((self.line - 2, self.column))
            if self.is_on_board(self.line - 1, self.column - 1) and self.board.board[self.line - 1][self.column - 1] is not None:
                if self.board.board[self.line - 1][self.column - 1].white != self.white:
                    att_moves.append((self.line - 1, self.column - 1))
            if self.is_on_board(self.line - 1, self.column + 1) and self.board.board[self.line - 1][self.column + 1] is not None:
                if self.board.board[self.line - 1][self.column + 1].white != self.white:
                    att_moves.append((self.line - 1, self.column + 1))
        else:
            if self.is_on_board(self.line + 1, self.column):
                moves.append((self.line + 1, self.column))
            if not self.hasMoved:
                moves.append((self.line + 2, self.column))
            if self.is_on_board(self.line + 1, self.column - 1) and self.board.board[self.line + 1][self.column - 1] is not None:
                if self.board.board[self.line + 1][self.column - 1].white != self.white:
                    att_moves.append((self.line + 1, self.column - 1))
            if self.is_on_board(self.line + 1, self.column + 1) and self.board.board[self.line + 1][self.column + 1] is not None:
                if self.board.board[self.line + 1][self.column + 1].white != self.white:
                    att_moves.append((self.line + 1, self.column + 1))

        return [move for move in moves if self.board.board[move[0]][move[1]] is None] + att_moves

    def is_attacking(self):
        att_moves = []
        if self.white:
            if self.is_on_board(self.line - 1, self.column - 1):
                att_moves.append((self.line - 1, self.column - 1))
            if self.is_on_board(self.line - 1, self.column + 1):
                att_moves.append((self.line - 1, self.column + 1))
        else:
            if self.is_on_board(self.line + 1, self.column - 1):
                att_moves.append((self.line + 1, self.column - 1))
            if self.is_on_board(self.line + 1, self.column + 1):
                att_moves.append((self.line + 1, self.column + 1))
        return att_moves

class Knight(Piece):

    def __init__(self, position, white, board):
        Piece.__init__(self, position, white, board)
        
        #Loading the sprite
        if self.white:
            self.surface = pygame.image.load("sprites/white_knight.png")
        else:
            self.surface = pygame.image.load(os.path.join("sprites", "black_knight.png"))
        
        #resizing it
        self.surface = pygame.transform.scale(self.surface, (80,80))

    def can_move_to(self):

        poss_moves = self.is_attacking()

        return [move for move in poss_moves if self.board.board[move[0]][move[1]] is None or self.board.board[move[0]][move[1]].white != self.white]

    def is_attacking(self):
        moves = []

        for i in [1, -1]:
            moves.append((self.line + 2, self.column + i))
            moves.append((self.line - 2, self.column + i))

            moves.append((self.line + i, self.column + 2))
            moves.append((self.line + i, self.column - 2))

        poss_moves = [move for move in moves if self.is_on_board(move[0], move[1])]

        return poss_moves

class Bishop(Piece):

    def __init__(self, position, white, board):
        Piece.__init__(self, position, white, board)
        
        #Loading the sprite
        if self.white:
            self.surface = pygame.image.load("sprites/white_bishop.png")
        else:
            self.surface = pygame.image.load(os.path.join("sprites", "black_bishop.png"))
        
        #resizing it
        self.surface = pygame.transform.scale(self.surface, (80,80))

    def can_move_to(self):
        
        moves = self.is_attacking()

        return [move for move in moves if self.board.board[move[0]][move[1]] is None or self.board.board[move[0]][move[1]].white != self.white]

    def is_attacking(self):
        moves = []

        for i in [1, -1]:
            
            j = 0

            while j == 0 or (self.is_on_board(self.line + j, self.column - j) and self.board.board[self.line + j][self.column - j] is None):
                moves.append((self.line + j, self.column - j))
                j += i

            if self.is_on_board(self.line + j, self.column - j):
                moves.append((self.line + j, self.column - j))
            
            j = 0

            while j == 0 or (self.is_on_board(self.line + j, self.column + j) and self.board.board[self.line + j][self.column + j] is None ):
                moves.append((self.line + j, self.column + j))
                j += i

            if self.is_on_board(self.line + j, self.column + j):
                moves.append((self.line + j, self.column + j))

        return [move for move in moves if move != (self.line, self.column)]


class King(Piece):

    def __init__(self, position, white, board):
        Piece.__init__(self, position, white, board)
        self.hasMoved = False
        
        #Loading the sprite
        if self.white:
            self.surface = pygame.image.load("sprites/white_king.png")
        else:
            self.surface = pygame.image.load(os.path.join("sprites", "black_king.png"))
        
        #resizing it
        self.surface = pygame.transform.scale(self.surface, (80,80))

    def can_move_to(self):
        
        moves = self.is_attacking()
        final_moves = [move for move in moves if self.board.board[move[0]][move[1]] is None or self.board.board[move[0]][move[1]].white != self.white]

        if self.can_small_rock():
            final_moves.append((self.line, self.column + 2))
        
        if self.can_big_rock():
            final_moves.append((self.line, self.column - 2))

        return final_moves

    def is_attacking(self):
        moves = []

        for i in [-1, 1]:
            if self.is_on_board(self.line + i, self.column):
                moves.append((self.line + i, self.column))
            if self.is_on_board(self.line, self.column + i):
                moves.append((self.line, self.column + i))
            if self.is_on_board(self.line + i, self.column + i):
                moves.append((self.line + i, self.column + i))
            if self.is_on_board(self.line + i, self.column - i):
                moves.append((self.line + i, self.column - i))

        return moves

    def can_small_rock(self):
        #Checking if pieces block the rock or if rook is still there
        if self.white:
            if self.board.board[7][7] == None or self.board.board[7][6] != None or self.board.board[7][5] != None:
                return False
        else:
            if self.board.board[0][7] == None or self.board.board[0][6] != None or self.board.board[0][5] != None:
                return False

        #Checking if the king or the rook have already moved
        if self.white:
            if self.hasMoved or self.board.board[7][7].hasMoved:
                return False
        else:
            if self.hasMoved or self.board.board[0][7].hasMoved:
                return False

        #Checking if the king goes through a check position
        col = 'white' if self.white else 'black'
        for i in [5,6]:
            new_board = self.board.copy()
            new_board.board[self.line][self.column] = None
            new_board.board[self.line][i] = self

            if new_board.is_checked(col):
                return False

        return True

    def can_big_rock(self):
        #Checking if pieces block the rock or if rook is still there
        if self.white:
            if self.board.board[7][0] == None or self.board.board[7][1] != None or self.board.board[7][2] != None or self.board.board[7][3] != None:
                return False
        else:
            if self.board.board[0][7] == None or self.board.board[0][1] != None or self.board.board[0][2] != None or self.board.board[0][3] != None:
                return False

        #Checking if the king or the rook have already moved
        if self.white:
            if self.hasMoved or self.board.board[7][7].hasMoved:
                return False
        else:
            if self.hasMoved or self.board.board[0][7].hasMoved:
                return False

        #Checking if the king goes through a check position
        col = 'white' if self.white else 'black'
        for i in [2,3]:
            new_board = self.board.copy()
            new_board.board[self.line][self.column] = None
            new_board.board[self.line][i] = self

            if new_board.is_checked(col):
                return False
        
        return True


class Rook(Piece):

    def __init__(self, position, white, board):
        Piece.__init__(self, position, white, board)
        self.hasMoved = False
        
        #Loading the sprite
        if self.white:
            self.surface = pygame.image.load("sprites/white_rook.png")
        else:
            self.surface = pygame.image.load(os.path.join("sprites", "black_rook.png"))
        
        #resizing it
        self.surface = pygame.transform.scale(self.surface, (80,80))

    def can_move_to(self):
        
        moves = self.is_attacking()

        return [move for move in moves if self.board.board[move[0]][move[1]] is None or self.board.board[move[0]][move[1]].white != self.white]

    def is_attacking(self):
        moves = []
        
        for i in [1, -1]:
            
            j = 0

            while j == 0 or (self.is_on_board(self.line + j, self.column) and self.board.board[self.line + j][self.column] is None):
                moves.append((self.line + j, self.column))
                j += i

            if self.line + j <= 7 and self.line + j >= 0:
                moves.append((self.line + j, self.column))
            
            j = 0

            while j == 0 or (self.is_on_board(self.line, self.column + j) and self.board.board[self.line][self.column + j] is None):
                moves.append((self.line, self.column + j))
                j += i

            if self.column + j <= 7 and self.column + j >= 0:
                moves.append((self.line, self.column + j))

        return [move for move in moves if move != (self.line, self.column)]


class Queen(Piece):

    def __init__(self, position, white, board):
        Piece.__init__(self, position, white, board)
        
        #Loading the sprite
        if self.white:
            self.surface = pygame.image.load("sprites/white_queen.png")
        else:
            self.surface = pygame.image.load(os.path.join("sprites", "black_queen.png"))
        
        #resizing it
        self.surface = pygame.transform.scale(self.surface, (80,80))

    def can_move_to(self):
        
        moves = self.is_attacking()

        return [move for move in moves if self.board.board[move[0]][move[1]] is None or self.board.board[move[0]][move[1]].white != self.white]

    def is_attacking(self):
        moves = []
        
        #Rook moves
        for i in [1, -1]:
            
            j = 0

            while j == 0 or (self.line + j <= 7 and self.line + j >= 0 and self.board.board[self.line + j][self.column] is None):
                moves.append((self.line + j, self.column))
                j += i

            if self.line + j <= 7 and self.line + j >= 0:
                moves.append((self.line + j, self.column))
            
            j = 0

            while j == 0 or (self.column + j <= 7 and self.column + j >= 0 and self.board.board[self.line][self.column + j] is None ):
                moves.append((self.line, self.column + j))
                j += i

            if self.column + j <= 7 and self.column + j >= 0:
                moves.append((self.line, self.column + j))

        #Bishop moves
        for i in [1, -1]:
            
            j = 0

            while j == 0 or (self.is_on_board(self.line + j, self.column - j) and self.board.board[self.line + j][self.column - j] is None):
                moves.append((self.line + j, self.column - j))
                j += i

            if self.is_on_board(self.line + j, self.column - j):
                moves.append((self.line + j, self.column - j))
            
            j = 0

            while j == 0 or (self.is_on_board(self.line + j, self.column + j) and self.board.board[self.line + j][self.column + j] is None ):
                moves.append((self.line + j, self.column + j))
                j += i

            if self.is_on_board(self.line + j, self.column + j):
                moves.append((self.line + j, self.column + j))

        return [move for move in moves if move != (self.line, self.column)]
