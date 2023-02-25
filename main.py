
import pygame
import time
import sys

from classes.Board import Board

pygame.init()

WIDTH = 900
HEIGHT = 1000

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
board = Board(WIDTH, HEIGHT)

def draw(win):    
    board.update_display(win)
    pygame.display.update()



def main(WIN, WIDTH):

    while True:
        pygame.time.delay(50) ##stops cpu dying

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            """This quits the program if the player closes the window"""

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                board.handle_click(pos)

        draw(WIN)
        if board.is_inCheck(board.current_turn) and board.isCheckMated():
            print("Check mate!! Red wins" if board.current_turn=='b' else 'Black wins')
            pygame.quit()
            sys.exit()

main(WIN, WIDTH)