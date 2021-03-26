import pygame


def initialize_screen(width: int, height: int) -> bool:
    """"
    Initialize the pygame window to width width and height height.
    """
    pygame.init()
    screen = pygame.display.set_mode([width, height])
    return True, screen
