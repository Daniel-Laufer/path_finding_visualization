from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from typing import *
import math
import random

from box import Box


class PygameWindow():
    """
    A class to create a pygame window.
    Also deals with initial creation of all the box objects and drawing them to the screen.

    Public Attributes:
    ===========
    colors: a dictionary that maps color names to their rgb values
    button_row_height: the height of the frame that hold the button
    screen_width: the width of the pygame window
    screen_height: the height of the pygame window 
    num_boxes_horizontally: number of boxes in each row
    num_boxes_vertically: number of boxes in each column
    box_width: the width of each box
    box_height: the height of each box
    starting_point_coords: a tuple of which stores position of the starting coord (row, col)
    end_point_coords: a tuple of which stores position of the end point coord (row, col)
    button_coords: dictionary with keys being names of buttons, and their values being the (row, col) of the uppermost left corner of that button
    button_colors: dictionary with keys being names of buttons, and their values being the (r,g,b) color value of each button
    button_width: width of all buttons in this window
    button_height: height of all buttons in this window
    game_status: can either be '' (waiting for inputs), 'start', 'pause', 'reset'
    running: true if the game is running, false otherwise
    font: the font used in this window
    boxes: A list storing all the Box objects in this window.
    row_coords: list to store y positions of the top left corner of the 0th box in each row of grid
    last_dragged_box: the last box to be wall-toggled by mouse-dragging
    """
    colors: Dict[str, Tuple[int, int]]
    button_row_height: int
    screen_width: int
    screen_height: int
    num_boxes_horizontally: int
    num_boxes_vertically: int
    box_width: int
    box_height: int
    starting_point_coords: Tuple[int, int]
    end_point_coords: Tuple[int, int]
    button_coords: Dict[str, Tuple[int, int]]
    button_colors: Dict[str, Tuple[int, int, int]]
    button_width: int
    button_height: int
    game_status: str
    running: bool
    font: pygame.font
    boxes: List[List[Box]]  # should be List[List[Box,...],...] but typing module throws error when I do it that way
    row_coords: List[int] # should be List[int,...] but typing module throws error when I do it that way
    last_dragged_box: Optional[Box]
    

    def __init__(self, num_boxes_horizontally: int, num_boxes_vertically: int,  algorithm:str):
        pygame.init()
        self.COLORS = {'black': (0, 0, 0), 'white': (255, 255, 255), 'green': (0, 255, )}
        self.button_row_height = 50
        self.screen_width = 500
        self.screen_height = 500
        self.num_boxes_horizontally = num_boxes_horizontally
        self.num_boxes_vertically = num_boxes_vertically
        self.box_width = math.floor(self.screen_width / self.num_boxes_horizontally)
        self.box_height = math.floor(self.screen_height / self.num_boxes_vertically)
        self.starting_point_coords = None
        self.end_point_coords = None
        self.button_coords = {'start': (-1, -1), 'pause': (-1, -1), 'reset': (-1, -1)} 
        self.button_colors = {'start': (0, 255, 0), 'pause': (255, 165, 0), 'reset': (255, 0, 0)}
        self.button_width = 100
        self.button_height = 45
        self.game_status = "" 
        self.running = True
        self.font = pygame.font.SysFont("arialroundedboldttf", 12)
        self.boxes = []
        self.row_coords = []
        self.algorithm = algorithm
        self.last_dragged_box = None


    def initialize_screen(self) -> None:
        """"
        Initialize the pygame window to width <self.screen_width> and height <self.screen_height> + <self.button_row_heightt>.
        """
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height + self.button_row_height])


    def setup_grid(self) -> None:
        """
        Create all the boxes and store them in <self.boxes>.
        Also populate the <self.row_coords> list as well as calling
        the set_neighbors_of_each_box function.
        """
        curr_x = 0
        curr_y = 0

        # index in 'boxes' list
        boxes_i = 0

        # drawing the grid layer by layer
        while (curr_y + self.box_height) < self.screen_height :
            curr_x = 0
            self.boxes.append([])
            while (curr_x + self.box_width) < self.screen_width:
                self.boxes[boxes_i].append(Box(curr_x, curr_y, self.box_width, self.box_height, len(self.boxes) - 1, len(self.boxes[boxes_i]) ))
                curr_x += self.box_width

            self.row_coords.append(curr_y)
            curr_y += self.box_height
            boxes_i += 1

        # build up the adjacency list
        self.set_neighbors_of_each_box()


    def set_neighbors_of_each_box(self):
        """
        Fill each boxes "neighbors" list attribute with references to all of its neighbors' corresponding box objects.
        This is essentially populating our adjacency list which we will use in our path findin algorithms.
        """
        for i, row in enumerate(self.boxes):
            for j, box in enumerate(row):
                if i > 0:
                    box.neighbors.append(self.boxes[i - 1][j]) # top
                    if j > 0:
                        box.neighbors.append(self.boxes[i - 1][j - 1]) # top left
                    if j < len(row) - 1:
                        box.neighbors.append(self.boxes[i - 1][j + 1]) # top right
                if j > 0:
                    box.neighbors.append(self.boxes[i][j - 1]) # left
                if i < len(self.boxes) - 1:
                    box.neighbors.append(self.boxes[i + 1][j]) # bottom
                    if j > 0:
                        box.neighbors.append(self.boxes[i + 1][j - 1]) # bottom left
                    if j < len(row) - 1:
                        box.neighbors.append(self.boxes[i + 1][j + 1]) # bottom right
                if j < len(row) - 1:
                    box.neighbors.append(self.boxes[i][j + 1]) # right


    def generate_random_walls(self) -> None:
        """
        Populates the grid with walls in random locations.
        """
        for row in self.boxes:
            for box in row:
                if random.random() > 0.5:
                    box.toggle_wall_status()
    

    def draw_grid(self) -> None:
        """
        Draw each box in <self.boxes> to the screen.
        """
        for row in self.boxes:
            for box in row:
                if box.status == 'EMPTY':
                    pygame.draw.rect(self.screen, self.COLORS['black'],(box.x, box.y, box.width, box.height), 1)
                else:
                    pygame.draw.rect(self.screen, box.color ,(box.x, box.y, box.width, box.height), 0)


    def get_which_row_clicked(self, pos: Tuple[int, int]):
        """
        Return the index of the row that was clicked by the user.
        """
        for i, y in enumerate(self.row_coords):

            if y >= pos[1]:

                return i - 1

        return len(self.row_coords) - 1

    def draw_buttons(self):
        horiz_margin = 10
        vert_margin = 0
        self.button_coords['start'] = (horiz_margin, vert_margin + self.screen_height, vert_margin + self.screen_height)
        self.button_coords['pause'] = (horiz_margin * 2 + self.button_width, vert_margin + self.screen_height)
        self.button_coords['reset'] = ((horiz_margin * 3 + self.button_width * 2), vert_margin + self.screen_height)

        for button in self.button_coords:
            text = self.font.render(button.title(), True, (0, 0, 0))
            horiz_button_padding = (self.button_width - text.get_width()) // 2
            vert_button_padding = (self.button_height - text.get_height()) // 2
            pygame.draw.rect(self.screen, self.button_colors[button],(self.button_coords[button][0], self.button_coords[button][1], self.button_width, self.button_height))
            self.screen.blit(text, (self.button_coords[button][0] + horiz_button_padding , self.button_coords[button][1] + vert_button_padding))