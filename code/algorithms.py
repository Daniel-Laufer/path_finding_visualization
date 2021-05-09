from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame_window import PygameWindow
from box import Box, STATUS_COLORS
import time
from ADTs import Queue
from heapq import *
from typing import *
from more_heapq import MoreHeapQ


class Algorithm():
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
        """
        distance_to_neighbor = 1
        if abs(other.row - box.row) + abs(other.col - box.col) == 2:
            distance_to_neighbor += 0.4
        return distance_to_neighbor

    def highlight_path(self, box: Box) -> None:
        if box.parent is None:
            return
        if box != self.starting_box and box != self.end_box:
            box.color = STATUS_COLORS["PATH"]
        self.highlight_path(box.parent)


class AStarAlgorithm(Algorithm):
    """
    An implementation of Dijkstra's algorithm.
    ===========
    q: a list which will act as a min-heap which stores boxes the algorithm still needs to explore
    """
    q: list

    def __init__(self, window: PygameWindow):
        super().__init__(window)
        self.closed_set = []
        self.open_set = []

    def run(self, window: PygameWindow):
        pass


class DijkstrasAlgorithm(Algorithm):
    """
    An implementation of Dijkstra's algorithm.
    ===========
    q: a list which will act as a min-heap which stores boxes the algorithm still needs to explore

    """
    q: MoreHeapQ

    def __init__(self, window: PygameWindow):
        super().__init__(window)
        self.q = MoreHeapQ()

    def run(self, window: PygameWindow):
        if not self.window.game_status:
            return
        elif self.window.game_status == 'start':
            # check if start and end points exist
            if not all([window.starting_point_coords, window.end_point_coords]):
                return

            # starting up the algorithm (basically doing the setup for it before entering main while loop)
            if not self.started:
                self.starting_box = window.boxes[window.starting_point_coords[0]][window.starting_point_coords[1]]
                self.end_box = window.boxes[window.end_point_coords[0]][window.end_point_coords[1]]
                self.started = True
                self.starting_box.cost = 0

                for row in window.boxes:
                    for box in row:
                        if box != self.starting_box:
                            box.cost = float("inf")
                        to_push = (box.row, box.col)
                        self.q.add_task(to_push, box.cost)

            if self.q.size == 0:
                return

            popped_off_coords = self.q.pop_task()
            u = self.window.boxes[popped_off_coords[0]][popped_off_coords[1]]

            if u == self.end_box:
                while self.q.size > 0:
                    self.q.pop_task()
                super().highlight_path(self.end_box)
                return

            for neighbor in u.neighbors:
                alt_cost = u.cost + Algorithm.compute_distance(u, neighbor)
                if (neighbor.cost is None or alt_cost < neighbor.cost) \
                        and neighbor.color not in [STATUS_COLORS["START"], STATUS_COLORS["WALL"]]:
                    if neighbor.color == STATUS_COLORS["EMPTY"]:
                        neighbor.color = STATUS_COLORS["ENCOUNTERED"]

                    neighbor.cost = alt_cost
                    neighbor.parent = u
                    to_push = (neighbor.row, neighbor.col)

                    # decreasing priority of this key
                    self.q.remove_task(to_push)
                    self.q.add_task(to_push, alt_cost)

                if u.color not in [STATUS_COLORS["START"], STATUS_COLORS["WALL"]]:
                    u.color = STATUS_COLORS["EXPLORED"]

        elif window.game_status == "reset":
            self.reset_algorithm(window)


class BFSWeighted(Algorithm):
    """
    The Breadth-first search path finding algorithm.
    ===========
    q: a list which will act as a min-heap which stores boxes the algorithm still needs to explore
    """
    q: list
    starting_box: Optional[Box]
    end_box: Optional[Box]

    def __init__(self, window: PygameWindow):
        super().__init__(window)
        self.q = []

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
                super().highlight_path(self.end_box)
                return

            for neighbor in u.neighbors:
                new_cost = u.cost + Algorithm.compute_distance(u, neighbor)

                if (neighbor.cost is None or new_cost < neighbor.cost)\
                        and neighbor.color not in [STATUS_COLORS["START"], STATUS_COLORS["WALL"]]:
                    if neighbor.color == STATUS_COLORS["EMPTY"]:
                        neighbor.color = STATUS_COLORS["ENCOUNTERED"]
                    neighbor.cost = new_cost
                    neighbor.parent = u
                    heappush(self.q, (new_cost, neighbor))
                if u.color not in [STATUS_COLORS["START"], STATUS_COLORS["WALL"]]:
                    u.color = STATUS_COLORS["EXPLORED"]

        elif window.game_status == "reset":
            self.reset_algorithm(window)


class BFS(Algorithm):
    """
    The Breadth-first search path finding algorithm.
    This implementation of the algorithm will treat all movement costs as equivalent.
    i.e moving diagonally covers the same distance as moving to an adjacent box.
    Public Attributes:
    ===========
    q: a list which will act as a queue for boxes the algorithm still needs to explore
    starting_box: the starting point of our algorithm
    end_box: the destination this algorithm wants to reach.
    """
    q: Queue

    def __init__(self, window: PygameWindow):
        super().__init__(window)
        self.q = Queue()

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
                super().highlight_path(self.end_box)
                return

            u = self.q.dequeue()
            for neighbor in u.neighbors:
                if neighbor.color in [STATUS_COLORS["EMPTY"], STATUS_COLORS["END"]]:
                    if neighbor.color == STATUS_COLORS["END"]:
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
