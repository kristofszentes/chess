import pygame
import socket, select, pickle
from board import Board
from pieces import King
from network import Network
from _thread import *

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

#Network options:
IP = "localhost"
PORT = 50000

class Game():

    def __init__(self, window_size):
        self.network = Network(IP, PORT)
        self.size = window_size
        self.screen = None
        self.white = True if self.network.id == 'True' else False
        self.playerColor = 'white' if self.white else 'black'
        self.isWhiteChecked = False
        self.isBlackChecked = False
        self.isWhiteMated = False
        self.isBlackMated = False
        self.board = Board()
        self.selected = None
        self.marked = []
        self.board.init_game()
        self.your_turn = self.white

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
                pygame.draw.rect(self.screen, RED, (55 + 80*square[1], 55 + 80*square[0], 30, 30))
        else:
            for square in self.marked:
                pygame.draw.rect(self.screen, RED, (615 - 80*square[1], 615 - 80*square[0], 30, 30))
        
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

        if self.white:
            numbers.reverse()
        else:
            letters.reverse()
        
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

        if not self.your_turn:
            start_new_thread(self.wait_for_move,())
            print('thread started')

        while cont:
            pygame.time.delay(2)

            #Closing the window
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    cont = False

            if self.your_turn and not self.isBlackMated and not self.isWhiteMated:
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
                            move_to_send = ((self.selected.line,self.selected.column), (board_x, board_y))
                            self.selected.move(board_x, board_y)
                            #When rocking, we also need to move the rook
                            if isinstance(self.selected, King) and not self.selected.hasMoved and board_y in [2,6]:
                                if board_y == 6:
                                    rook = self.board.board[self.selected.line][7]
                                    rook.move(self.selected.line, 5)
                                    rook.hasMoved = True
                                else:
                                    rook = self.board.board[self.selected.line][0]
                                    rook.move(self.selected.line,3)
                                    rook.hasMoved = True
                            
                            if type(self.selected).__name__ in ['Pawn', 'Rook', 'King']:
                                self.selected.hasMoved = True

                            self.board.check_pawn_to_queen()
                            self.updating_checked()

                            #sending data to network
                            self.network.send(move_to_send)

                            self.selected = None
                            self.marked = []
                            self.your_turn = False
                            start_new_thread(self.wait_for_move,())

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
            self.upda('white')
                        
        if self.board.is_checked('black'):
            self.isBlackChecked = True
            print('black checked')

        elif self.isBlackChecked and not self.board.is_checked('black'):
            self.isBlackChecked = False
            print('black no more checked')

        if self.isBlackChecked:
            self.updating_check_mate('black')

    def is_check_mated(self, col):
        white = True if col == 'white' else False
        ally_pieces = self.board.get_white_pieces() if white else self.board.get_black_pieces()
        for piece in ally_pieces:
            moves = piece.can_move_to()
            for move in moves:
                new_board = self.board.copy()
                new_board.board[piece.line][piece.column] = None
                new_board.board[move[0]][move[1]] = piece

                if not new_board.is_checked(col):
                    return False
        return True

    def updating_check_mate(self, col):
        if self.is_check_mated(col):
            if col == 'white':
                print('Black won')
                self.isWhiteMated = True
            else:
                print('White won')
                self.isBlackMated = True

    def white_to_board_coord(self, x ,y):
        new_x = (x-30) // 80
        new_y = (y-30) // 80
        return new_y, new_x

    def black_to_board_coord(self, x ,y):
        new_x = (x-30) // 80
        new_y = (y-30) // 80
        return 7 - new_y, 7 - new_x

    def applying_received_move(self, move):
        piece = self.board.board[move[0][0]][move[0][1]]
        if isinstance(piece, King) and not piece.hasMoved and move[1][1] in [2, 6]:
            if move[1][1] == 6:
                rook = self.board.board[move[0][0]][7]
                rook.move(move[0][0], 5)
                rook.hasMoved = True
            else:
                rook = self.board.board[move[0][0]][0]
                rook.move(move[0][0], 3)
                rook.hasMoved = True

        piece.move(move[1][0], move[1][1])

    def wait_for_move(self):
        enn_move = self.network.wait_for_data()
        print('data received: ', enn_move)
        self.your_turn = True
        self.applying_received_move(enn_move)
        
if __name__ == "__main__":
    game = Game(SIZE)
    game.run()