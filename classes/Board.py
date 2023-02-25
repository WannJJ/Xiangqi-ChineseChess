import pygame

from classes.Piece import Piece
from classes.Chariot import Chariot
from classes.Horse import Horse
from classes.King import King
from classes.Cannon import Cannon
from classes.Soldier import Soldier
from classes.Advisor import Advisor
from classes.Elephant import Elephant



class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = width //9
        self.current_turn = 'r'
        self.selected_piece = None
        self.selected_pos = []
        self.possible_moves = []

        self.config = [[None for i in range(9)] for i in range(10)]
        self.setup_new_board()
    
    def setup_new_board(self):
    
        self.config[0] = [Chariot((0,0), 'b', self), Horse((0,1), 'b', self), Elephant((0,2), 'b', self), \
                Advisor((0,3), 'b', self), King((0,4), 'b', self), Advisor((0,5), 'b', self), \
                    Elephant((0,6), 'b', self), Horse((0,7), 'b', self), Chariot((0,8), 'b', self)]
        self.config[2] = [None, Cannon((2,1), 'b', self), None, None, None, None, None, Cannon((2,7), 'b', self), None]

        self.config[9] = [Chariot((9,0), 'r', self), Horse((9,1), 'r', self), Elephant((9,2), 'r', self), \
                Advisor((9,3), 'r', self), King((9,4), 'r', self), Advisor((9,5), 'r', self), \
                    Elephant((9,6), 'r', self), Horse((9,7), 'r', self), Chariot((9,8), 'r', self)]
        self.config[7] = [None, Cannon((7, 1), 'r', self), None, None, None, None, None, Cannon((7, 7), 'r', self), None]    

        for i in range(0,9,2):
            self.config[3][i] = Soldier((3, i), 'b', self)
            self.config[6][i] = Soldier((6, i), 'r', self)
    
    def get_piece(self, pos:tuple)->Piece:
        return self.config[pos[0]][pos[1]]
    
    def set_piece(self, pos:tuple, piece:Piece):
        self.config[pos[0]][pos[1]] = piece
    
    def on_board(self, position:tuple)->bool:
        if position[0] > -1 and position[1] > -1 and position[0] < 10 and position[1] < 9:
            return True

    def is_inCheck(self, team: str) ->bool:
        if team!=self.current_turn:
            return False
        king_pos = self.find_King(team)
        #opponent's all possible moves:
        for row in self.config:
            for piece in row:
                if(piece and piece.team!=team):
                    if king_pos in piece.get_possible_moves(self):
                        return True     
        return False
    def isCheckMated(self):
        for row in self.config:
            for piece in row:
                if(piece and piece.team==self.current_turn):
                    if(piece.get_valid_moves(self)):
                        return False
        return True

    def find_King(self, team:str):
        for i in range(10):
            for j in range(9):
                piece = self.config[i][j]
                if(piece and piece.team==team and piece.type=='k'):
                    return (i, j)

    def king_face_each_other(self) ->bool:
        red_king_pos = self.find_King('r')
        black_king_pos = self.find_King('b')
        if red_king_pos[1] != black_king_pos[1]:
            return False
        return all(not self.config[x][red_king_pos[1]] for x in range(black_king_pos[0]+1, red_king_pos[0]))

        
    

    def handle_click(self, pos: tuple):
        my, mx = pos
        y = my // self.tile_width
        x = mx // self.tile_width
        
        if (x, y) in self.possible_moves and self.selected_pos:
            # performing a valid move
            row, col = self.selected_pos ## coords of the chess piece we picked up
            chessPiece = self.config[row][col]

            chessPiece.move(self, (x,y))  
            self.selected_pos = []
            self.possible_moves = []
            self.current_turn = 'b' if self.current_turn=='r' else 'r'

            print(self.convert_to_readable())
        
        elif(self.config[x][y] and self.config[x][y].team==self.current_turn):                    
            self.possible_moves = self.config[x][y].get_valid_moves(self)
            if self.possible_moves:
                self.selected_pos = x,y
        else:
                self.selected_pos = []
                self.possible_moves = []
                print('Can\'t select')

    def convert_to_readable(self):
        output = ''
        for i in self.config:
            for j in i:
                try:
                    output += j.team + j.type + ', '
                except:
                    output +=  '  , '
            output += '\n'
        return output

    def update_display(self, win):
        gap = self.tile_width
        YELLOW = (204, 204, 0)
        RED = (200, 100, 100)
        BLUE = (50, 255, 255)
        BLACK = (0, 0, 0)
        win.fill((255,165,0))

        for i in range(10):
            for j in range(9):
                
                if (i, j) in self.possible_moves:
                    pygame.draw.rect(win, BLUE, (j*gap, i*gap, gap, gap))
                if self.selected_pos:
                    pygame.draw.rect(win, YELLOW, (self.selected_pos[1]*gap, self.selected_pos[0]*gap, gap, gap))
        if self.is_inCheck(self.current_turn):
            for i in range(10):
                for j in range(9):
                    piece = self.config[i][j]
                    if(piece and piece.team==self.current_turn and piece.type=='k'):
                        pygame.draw.rect(win, RED, (j*gap, i*gap, gap, gap))

        
        for i in range(10):
            for j in range(9):            
                if self.config[i][j]:
                    win.blit(self.config[i][j].image, (j*gap, i*gap))

            """
            The squares are all white so this we need to draw the grey lines that separate all the chess tiles
            from each other and that is what this function does"""
            for i in range(10):
                pygame.draw.line(win, BLACK, (0.5 * gap, (i+0.5) * gap), (8.5 * gap, (i+0.5) * gap))
            for j in range(9):
                pygame.draw.line(win, BLACK, ((j+0.5) * gap, 0.5 * gap), ((j+0.5) * gap, 4.5 * gap))
                pygame.draw.line(win, BLACK, ((j+0.5) * gap, 5.5 * gap), ((j+0.5) * gap, 9.5 * gap))
            pygame.draw.line(win, BLACK, (3.5 * gap, 0.5 * gap), (5.5 * gap, 2.5 * gap))
            pygame.draw.line(win, BLACK, (5.5 * gap, 0.5 * gap), (3.5 * gap, 2.5 * gap))
            pygame.draw.line(win, BLACK, (3.5 * gap, 9.5 * gap), (5.5 * gap, 7.5 * gap))
            pygame.draw.line(win, BLACK, (5.5 * gap, 9.5 * gap), (3.5 * gap, 7.5 * gap))





