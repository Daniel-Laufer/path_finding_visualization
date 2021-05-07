import pygame
import math
from typing import *
import random
import sys

from box import Box
from pygame_window import PygameWindow
from eventHandlers import EventHanlder




if __name__ == "__main__":
    window = PygameWindow()
    window.setup_grid()
    window.initialize_screen()
    window.generate_random_walls()
    eventHandler = EventHanlder(window)

    while window.running:
        window.screen.fill((255, 255, 255))
        window.draw_grid()
        window.draw_buttons()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                eventHandler.handleMouseButtonDown(event)
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    eventHandler.handleMouseMotion(event)



