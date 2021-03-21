import pygame
from board import Board

pygame.init()

#Size of the window
SIZE = 700

#Defining the color constants in RGB
WHITE = (255, 255, 255)
GREY = (135, 135, 135)
BLACK = (0, 0, 0)
OLIVE = (81, 76, 30)
RED = (255, 0, 0)

#Defining the font
FONT = pygame.font.SysFont("monospace",20,True)


class Game():

    def __init__(self, window_size, white):
        self.size = window_size
        self.screen = None
        self.white = white
        self.playerColor = 'white' if self.white else 'black'
        self.isWhiteChecked = False
        self.isBlackChecked = False
        self.isWhiteMated = False
        self.isBlackMated = False
        self.board = Board()
        self.selected = None
        self.marked = []
        
        self.board.init_game()

    def update_screen(self):
        
        #Drawing the background
        self.screen.fill(GREY)

        self.draw_board()

        #Drawing the pieces
        if self.white:
            for i in range(len(self.board.board)):
                for j in range(len(self.board.board[i])):
                    if self.board.board[i][j] != None:
                        self.screen.blit(self.board.board[i][j].surface, (30 + 80*j, 30 + 80*i))
        else:
            for i in range(len(self.board.board)):
                for j in range(len(self.board.board[i])):
                    if self.board.board[i][j] != None:
                        self.screen.blit(self.board.board[i][j].surface, (590 - 80*j, 590 - 80*i))

        #Drawing the places where you can move
        if self.white:
            for square in self.marked:
                pygame.draw.rect(self.screen, RED, (30 + 80*square[1], 30 + 80*square[0], 30, 30))
        else:
            for square in self.marked:
                pygame.draw.rect(self.screen, RED, (590 - 80*square[1], 590 - 80*square[0], 30, 30))
        
        pygame.display.update()

    def draw_board(self):
        #Drawing the board
        for i in range(8):
            for j in range(8):
                if (i+j) % 2 == 0:
                    color = WHITE
                else:
                    color = OLIVE
                pygame.draw.rect(self.screen, color, (30 + 80*i, 30 + 80*j, 80, 80))

        #Writing letters and numbers on the side
        numbers = list(range(1,9))
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        if not self.white:
            letters.reverse()
            numbers.reverse()
        
        for i in range(8):
            #letters
            letter = FONT.render(letters[i], 1, BLACK)
            self.screen.blit(letter, (65 + 80*i, 670))

            #numbers
            number = FONT.render(str(numbers[i]), 1, BLACK)
            self.screen.blit(number, (10, 60 + 80*i))

    def run(self):
        self.screen = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Simple Chess")

        cont = True

        while cont:
            pygame.time.delay(2)

            #Closing the window
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    cont = False

            if not self.isBlackMated and not self.isWhiteMated:
                #Checking mouse input
                if pygame.mouse.get_pressed()[0]:
                    
                    x,y = pygame.mouse.get_pos()
                    
                    if x >= 30 and x <= 670 and y >= 30 and y <= 670:
                        
                        if self.white:
                            board_x, board_y = self.white_to_board_coord(x, y)
                        else:
                            board_x, board_y = self.black_to_board_coord(x, y)

                        piece = self.board.board[board_x][board_y]
                        
                        #We check if the selected square has a piece and if the piece is of the player's color
                        if piece is not None and piece.white == self.white:
                            self.marked = []
                            self.selected = self.board.board[board_x][board_y]
                            self.marked.extend(self.selected.can_move_to())
                            self.marked = [move for move in self.marked if type(self.board.board[move[0]][move[1]]).__name__ != 'King']

                        #Moving
                        elif (board_x, board_y) in self.marked:
                            self.selected.move(board_x, board_y)
                            
                            if type(self.selected).__name__ in ['Pawn', 'Rook', 'King']:
                                self.selected.hasMoved = True

                            self.updating_checked()

                            self.selected = None
                            self.marked = []

            self.update_screen()

    def updating_checked(self):
        #Checking if someone is checked
        if not self.isWhiteChecked and self.board.is_checked('white'):
            self.isWhiteChecked = True
            print('white checked here')

        elif self.isWhiteChecked and not self.board.is_checked('white'):
            self.isWhiteChecked = False
            print('white no more checked')
        
        if self.isWhiteChecked:
            self.is_check_mated('white')
                        
        if not self.isBlackChecked and self.board.is_checked('black'):
            self.isBlackChecked = True
            print('black checked')
            self.updating_check_mate('black')

        elif self.isBlackChecked and not self.board.is_checked('black'):
            self.isBlackChecked = False
            print('black no more checked')

        if self.isWhiteChecked:
            self.is_check_mated('black')

    def is_check_mated(self, col):
        white = True if col == 'white' else False
        ally_pieces = self.board.get_white_pieces() if white else self.board.get_black_pieces()
        for piece in ally_pieces:
            moves = piece.can_move_to()
            print(piece, moves)
            for move in moves:
                new_board = self.board.copy()
                new_board.board[piece.line][piece.column] = None
                new_board.board[move[0]][move[1]] = piece

                if not new_board.is_checked(col):
                    print(move)
                    return False
        return True

    def updating_check_mate(self, col):
        if self.is_check_mated(col):
            if col == 'white':
                print('white is mated')
                self.isWhiteMated = True
            else:
                print('black is mated')
                self.isBlackMated = True

    def white_to_board_coord(self, x ,y):
        new_x = (x-30) // 80
        new_y = (y-30) // 80
        return new_y, new_x

    def black_to_board_coord(self, x ,y):
        new_x = (x-30) // 80
        new_y = (y-30) // 80
        return 7 - new_y, 7 - new_x
        
if __name__ == "__main__":
    game = Game(SIZE, True)
    game.run()