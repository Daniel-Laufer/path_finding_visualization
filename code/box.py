from __future__ import annotations
from datetime import datetime


STATUS_COLORS = {
    "EMPTY": (255, 255, 255),
    "WALL": (0, 0, 0),
    "START": (0, 255, 0),
    "END": (255, 0, 0),
    'VISITED': (255, 0, 255),
    'TO_VISIT': (128, 0, 255),
    'ENCOUNTERED': (255, 251, 0),
    'EXPLORED': (43, 79, 207),
    'PATH': (225, 0, 255)
}

class Box:
    """
    An individual box on the screen.
    """
    def __init__(self, x: int, y: int, width: int, height: int, row: int, col: int) -> None:
        self.color = (255, 255, 255)
        self.status = "EMPTY"
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.row = row
        self.col = col
        self.neighbors = []
        self.parent = None

        # attributes used in A* search algorithm
        self.f_cost = 0
        self.g_cost = 0
        self.h_cost = 0

        #attributes used for BFS
        self.cost = None



    def toggle_wall_status(self) -> None:
        """
        If this box is currently a wall vertex, make it an empty vertex.
        If this box is currently an empty vertex, make it a wall vertex.
        """
        if self.status != "WALL":
            self.status = "WALL"
            self.color = STATUS_COLORS['WALL']
            return
        self.status = "EMPTY"
        self.color = STATUS_COLORS['EMPTY']

    def toggle_start_status(self) -> None:
        """
        If this box is currently a start vertex, make it an empty vertex.
        If this box is currently an empty vertex, make it a start vertex.
        """
        if self.status != "START":
            self.status = "START"
            self.color = STATUS_COLORS['START']
            return
        self.status = "EMPTY"
        self.color = STATUS_COLORS['EMPTY']

    def toggle_end_status(self) -> None:
        """
        If this box is currently an end vertex, make it an empty vertex.
        If this box is currently an empty vertex, make it an end vertex.
        """
        if self.status != "END":
            self.status = "END"
            self.color = STATUS_COLORS['END']
            return
        self.status = "EMPTY"
        self.color = STATUS_COLORS['EMPTY']

    def toggle_visisted(self) -> None:
        """
        Mark this box as 'visited' meaning our algorithm has dealt with this.
        """
        self.status = ''
        self.color = STATUS_COLORS['VISITED']

    def toggle_to_visit(self) -> None:
        """
        Mark this box as 'to_visit' meaning our algorithm is going to visit this box.
        """
        self.status == 'TO_VISIT'
        self.color = STATUS_COLORS['TO_VISIT']


    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __lt__(self, other: Box):
        return True



    def __repr__(self) -> str:
        return '({}, {})'.format(self.row, self.col)


