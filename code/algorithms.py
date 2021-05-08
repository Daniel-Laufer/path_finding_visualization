from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame_window import PygameWindow
from box import Box, STATUS_COLORS
import time
from ADTs import Queue


class Algorithm():
    """
    An abstract parent class for various algorithms.
    """
    def __init__(self):
        self.started = False

    def run(self, window:PygameWindow):
        raise NotImplementedError

    def reset_algorithm(self, window: PygameWindow):
        self.__init__()
        window.frame_count = 0
        window.boxes, window.row_coords = [], []
        window.setup_grid()
        window.last_dragged_box, window.game_status, window.starting_point_coords, window.end_point_coords = None, None, None, None


class A_Star_algorithm(Algorithm):
    def __init__(self) -> None:
        self.closed_set = []
        self.open_set = []

    def run(self, window: PygameWindow):
        pass


class BFS(Algorithm):

    def __init__(self):
        super().__init__()
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















