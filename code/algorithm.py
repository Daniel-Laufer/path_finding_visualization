from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame_window import PygameWindow
from box import Box, STATUS_COLORS
from heapq import *
from typing import *


class Algorithm:
    """
    An abstract parent class for various algorithms.

    Public Attributes
    =================
    window: the pygame window that this algorithm is running on
    started: is true if the algorithm has been initialized and has started to run, false otherwise
    """
    window: PygameWindow
    started: bool

    def __init__(self, window: PygameWindow):
        self.window = window
        self.started = False
        self.starting_box = None
        self.end_box = None

    def run(self, window:PygameWindow):
        raise NotImplementedError

    def reset_algorithm(self, window: PygameWindow):
        self.__init__(window)
        window.frame_count = 0
        window.boxes, window.row_coords = [], []
        window.setup_grid()
        window.last_dragged_box, window.game_status, window.starting_point_coords, window.end_point_coords = None, None, None, None

    @staticmethod
    def compute_distance(box: Box, other: Box) -> int:
        """
        Return the approximate distance between <box> and <other>.
        Precondition:
            - Box box and Box other need to directly touching each other either
            by being on top/bottom of the other, to the left/right of the other, on their corners are touching
            diagonally.
        """
        distance_to_neighbor = 1

        # other and box MUST be positioned diagonally from each due to the precondition.
        if abs(other.row - box.row) + abs(other.col - box.col) == 2:
            distance_to_neighbor += 0.4
        return distance_to_neighbor

    def highlight_path(self, box: Box) -> None:
        if box.parent is None:
            return
        if box != self.starting_box and box != self.end_box:
            box.color = STATUS_COLORS["PATH"]
        self.highlight_path(box.parent)











