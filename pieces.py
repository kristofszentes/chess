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
        test = [-1,1]
        for x in test:
            for y in test:
                if self.is_on_board(self.line + x, self.column + y):
                    att_moves.append((self.line + x, self.column + y))
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

        return [move for move in moves if self.is_on_board(move[0],move[1])]

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
        moves = []

        for i in [1, -1]:
            
            j = 0

            while j == 0 or (self.is_on_board(self.line + j, self.column - j) and self.board.board[self.line + j][self.column - j] is None):
                moves.append((self.line + j, self.column - j))
                j += i

            if self.is_on_board(self.line + j, self.column - j) and self.board.board[self.line + j][self.column - j].white != self.white:
                moves.append((self.line + j, self.column - j))
            
            j = 0

            while j == 0 or (self.is_on_board(self.line + j, self.column + j) and self.board.board[self.line + j][self.column + j] is None ):
                moves.append((self.line + j, self.column + j))
                j += i

            if self.is_on_board(self.line + j, self.column + j) and self.board.board[self.line + j][self.column + j].white != self.white:
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

        #Taking out occupied positions
        moves = [move for move in moves if self.board.board[move[0]][move[1]] is None or self.board.board[move[0]][move[1]].white != self.white]
        
        #Taking out the moves in which he is checked
        '''poss_moves = []
        col = 'white' if self.white else 'black'
        for move in moves:
            new_board = self.board.copy()
            new_board.board[self.line][self.column] = None
            new_board.board[move[0]][move[1]] = self

            if not new_board.is_checked(col):
                poss_moves.append(move)'''
        return moves

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
        moves = []
        
        for i in [1, -1]:
            
            j = 0

            while j == 0 or (self.line + j <= 7 and self.line + j >= 0 and self.board.board[self.line + j][self.column] is None):
                moves.append((self.line + j, self.column))
                j += i

            if self.line + j <= 7 and self.line + j >= 0 and self.board.board[self.line + j][self.column].white != self.white:
                moves.append((self.line + j, self.column))
            
            j = 0

            while j == 0 or (self.column + j <= 7 and self.column + j >= 0 and self.board.board[self.line][self.column + j] is None ):
                moves.append((self.line, self.column + j))
                j += i

            if self.column + j <= 7 and self.column + j >= 0 and self.board.board[self.line][self.column + j].white != self.white:
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
        moves = []
        
        #Rook moves
        for i in [1, -1]:
            
            j = 0

            while j == 0 or (self.line + j <= 7 and self.line + j >= 0 and self.board.board[self.line + j][self.column] is None):
                moves.append((self.line + j, self.column))
                j += i

            if self.line + j <= 7 and self.line + j >= 0 and self.board.board[self.line + j][self.column].white != self.white:
                moves.append((self.line + j, self.column))
            
            j = 0

            while j == 0 or (self.column + j <= 7 and self.column + j >= 0 and self.board.board[self.line][self.column + j] is None ):
                moves.append((self.line, self.column + j))
                j += i

            if self.column + j <= 7 and self.column + j >= 0 and self.board.board[self.line][self.column + j].white != self.white:
                moves.append((self.line, self.column + j))

        #Bishop moves
        for i in [1, -1]:
            
            j = 0

            while j == 0 or (self.is_on_board(self.line + j, self.column - j) and self.board.board[self.line + j][self.column - j] is None):
                moves.append((self.line + j, self.column - j))
                j += i

            if self.is_on_board(self.line + j, self.column - j) and self.board.board[self.line + j][self.column - j].white != self.white:
                moves.append((self.line + j, self.column - j))
            
            j = 0

            while j == 0 or (self.is_on_board(self.line + j, self.column + j) and self.board.board[self.line + j][self.column + j] is None ):
                moves.append((self.line + j, self.column + j))
                j += i

            if self.is_on_board(self.line + j, self.column + j) and self.board.board[self.line + j][self.column + j].white != self.white:
                moves.append((self.line + j, self.column + j))

        return [move for move in moves if move != (self.line, self.column)]
