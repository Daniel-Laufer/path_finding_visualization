from os import environ
import pygame
import sys
from eventHandlers import EventHanlder
from a_star import AStarAlgorithm
from bfs import BFS
from dijkstra import DijkstrasAlgorithm
from pygame_window import PygameWindow
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


def get_commandline_args():
    out = """ Usage: python3 main.py <number of columns> <algorithm name> <slowness>
        Explanations: 
            number of columns: 
                say n=number of columns, then a n x n grid will be drawn on the screen.
            algorithm name: 
                the name of the pathfinding algorithm you'd like to run
            slowness:
                a positive integer that dictates how slow your chosen algorithm will run. 
                Say slowness = n,  then your algorithm will run every n frame(s) of the overall frame rate of 
                the visualization.
                So the higher the input is, the slower then algorithm will run.
               
        Restrictions:
            number of columns >= 2
            algorithm name can be any of the following strings:
                \"a_star\" (the A* search algorithm)
                \"dij\" (Dijkstra's algorithm)
                \"bfs\" (Breadth-first search (weighted variant))
            slowness > 0
          """

    all_good = False
    if len(sys.argv) == 4:
        num_cols_check = sys.argv[1].isdigit() and int(sys.argv[1]) >= 2
        name_check = sys.argv[2] in ['a_star', 'dij', 'bfs']
        slowness_check = sys.argv[3].isdigit() and int(sys.argv[3]) > 0
        all_good = all([num_cols_check, name_check, slowness_check])

    if len(sys.argv) != 4 or not all_good:
        print(out)
        exit(1)

    return int(sys.argv[1]), sys.argv[2], int(sys.argv[3])


if __name__ == "__main__":

    requested_num_cols, requested_alg, requested_slowness = get_commandline_args()
    window = PygameWindow(requested_num_cols, requested_num_cols, requested_alg, requested_slowness)
    window.setup_grid()

    window.initialize_screen()
    window.generate_random_walls()
    eventHandler = EventHanlder()
    alg = None
    if window.algorithm == "a_star":
        alg = AStarAlgorithm(window)
    elif window.algorithm == "dij":
        alg = DijkstrasAlgorithm(window)
    elif window.algorithm == "bfs":
        alg = BFS(window)

    # main "game" loop
    while window.running:
        window.screen.fill((255, 255, 255))
        window.draw_grid()
        window.draw_buttons()
        pygame.display.flip()
        if window.frame_count % window.slowness == 0:
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




