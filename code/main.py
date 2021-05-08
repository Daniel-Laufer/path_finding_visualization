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
from algorithms import *


def get_commandline_args():
    if len(sys.argv) != 3  or not sys.argv[1].isdigit() or sys.argv[2] not in ['a_star', 'dij', 'bfs']:
        print("\nUsage: <number of columns> <algorithm name>\n\tWhere algorithm name can be any of the following:\n\t\t\"a_star\"\n\t\t\"dij\"\n\t\t\"bfs (note that for simplicity, we are assuming that diagonal distances are equivalent to adjacent distances between squares in the grid) \"")
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
    elif window.algorithm == "bfs":
        alg = BFS()

    while window.running:
        window.screen.fill((255, 255, 255))
        window.draw_grid()
        window.draw_buttons()
        pygame.display.flip()
        if window.frame_count % 1 == 0:
            alg.run(window)
        window.frame_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                eventHandler.handleMouseButtonDown(window, event)
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    eventHandler.handleMouseMotion(window, event)




