from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame_window import PygameWindow
from box import Box, STATUS_COLORS
import time
from ADTs import Queue
from heapq import *


class Algorithm():
    """
    An abstract parent class for various algorithms.
    """
    def __init__(self, window: PygameWindow):
        self.window = window
        self.started = False

    def run(self, window:PygameWindow):
        raise NotImplementedError

    def reset_algorithm(self, window: PygameWindow):
        self.__init__(window)
        window.frame_count = 0
        window.boxes, window.row_coords = [], []
        window.setup_grid()
        window.last_dragged_box, window.game_status, window.starting_point_coords, window.end_point_coords = None, None, None, None


class A_Star_algorithm(Algorithm):
    def __init__(self, window: PygameWindow):
        super().__init__(window)
        self.closed_set = []
        self.open_set = []

    def run(self, window: PygameWindow):
        pass


class Dijkstras_algorithm(Algorithm):
    def __init__(self, window: PygameWindow):
        super().__init__(window)


class BFS_weighted(Algorithm):

    def __init__(self, window: PygameWindow):
        super().__init__(window)
        self.q = []
        self.starting_box = None
        self.end_box = None

    def run(self, window: PygameWindow):
        if not window.game_status:
            return
        elif window.game_status == 'start':
            # check if start and end points exist
            if not all([window.starting_point_coords, window.end_point_coords]):
                return
            if not self.started:
                self.starting_box = window.boxes[window.starting_point_coords[0]][window.starting_point_coords[1]]
                self.end_box = window.boxes[window.end_point_coords[0]][window.end_point_coords[1]]
                heappush(self.q, (0, self.starting_box))
                self.started = True
                self.starting_box.cost = 0

            if len(self.q) == 0:
                return

            u = heappop(self.q)[1]
            if u == self.end_box:
                while self.q:
                    heappop(self.q)
                self.highlight_path(self.end_box)
                return

            for neighbor in u.neighbors:
                distance_to_neighbor = 1
                if abs(neighbor.row - u.row) + abs(neighbor.col - u.col) == 2:
                    distance_to_neighbor += 0.4
                new_cost = u.cost + distance_to_neighbor

                if (neighbor.cost is None or new_cost < neighbor.cost) and neighbor.color not in [STATUS_COLORS["START"], STATUS_COLORS["WALL"]]:
                    if neighbor.color == STATUS_COLORS["EMPTY"]:
                        neighbor.color = STATUS_COLORS["ENCOUNTERED"]
                    neighbor.cost = new_cost
                    neighbor.parent = u
                    heappush(self.q, (new_cost, neighbor))
                if u.color not in [STATUS_COLORS["START"], STATUS_COLORS["WALL"]]:
                    u.color = STATUS_COLORS["EXPLORED"]



        elif window.game_status == "reset":
            self.reset_algorithm(window)

    def highlight_path(self, box: Box) -> None:
        if box.parent is None:
            return
        if box != self.starting_box and box != self.end_box:
            box.color = STATUS_COLORS["PATH"]
        self.highlight_path(box.parent)



class BFS(Algorithm):

    def __init__(self, window: PygameWindow):
        super().__init__(window)
        self.q = Queue()
        self.starting_box = None
        self.end_box = None

    def run(self, window: PygameWindow):
        if not window.game_status:
            return
        elif window.game_status == 'start':
            # check if start and end points exist
            if not all([window.starting_point_coords, window.end_point_coords]):
                return
            if not self.started:
                self.starting_box = window.boxes[window.starting_point_coords[0]][window.starting_point_coords[1]]
                self.end_box = window.boxes[window.end_point_coords[0]][window.end_point_coords[1]]
                self.q.enqueue(self.starting_box)
                self.started = True

            if self.q.is_empty():
                self.highlight_path(self.end_box)
                return

            u = self.q.dequeue()
            for neighbor in u.neighbors:
                if neighbor.color in [STATUS_COLORS["EMPTY"], STATUS_COLORS["END"]]:
                    if neighbor.color ==  STATUS_COLORS["END"]:
                        neighbor.parent = u
                        self.highlight_path(neighbor)
                        self.q.empty_queue()
                        return

                    neighbor.color = STATUS_COLORS["ENCOUNTERED"]
                    neighbor.parent = u
                    self.q.enqueue(neighbor)

            if u.color != STATUS_COLORS["START"]:
                u.color = STATUS_COLORS["EXPLORED"]
        elif window.game_status == "reset":
            self.reset_algorithm(window)

    def highlight_path(self, box: Box) -> None:
        if box.parent is None:
            return
        if box != self.starting_box and box != self.end_box:
            box.color = STATUS_COLORS["PATH"]
        self.highlight_path(box.parent)















