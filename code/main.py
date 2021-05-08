from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import math
from typing import *
import random
import sys
from box import Box
from pygame_window import PygameWindow
from eventHandlers import EventHanlder
from algorithms import A_Star_algorithm


def get_commandline_args():
    if len(sys.argv) != 3  or not sys.argv[1].isdigit() or sys.argv[2] not in ['a_star', 'dij']:
        print("\nUsage: <number of columns> <algorithm name>\n\tWhere number of columns is a positive integer, and the algorithm name is either \"a_star\" or \"dij\"\n")
        exit(1)
    
    return int(sys.argv[1]), sys.argv[2]
    



if __name__ == "__main__":
    requested_num_cols, requested_alg = get_commandline_args()
    window = PygameWindow(requested_num_cols, requested_num_cols, requested_alg)
    window.setup_grid()
    window.initialize_screen()
    window.generate_random_walls()
    eventHandler = EventHanlder()
    alg = None
    if window.algorithm == "a_star":
        alg = A_Star_algorithm()
    elif window.algorithm == "dij":
        alg = A_Star_algorithm()

    while window.running:
        window.screen.fill((255, 255, 255))
        window.draw_grid()
        window.draw_buttons()
        pygame.display.flip()
        alg.run(window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                eventHandler.handleMouseButtonDown(window, event)
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    eventHandler.handleMouseMotion(window, event)
        



