from os import environ
from pygame_window import PygameWindow
from box import  STATUS_COLORS
from algorithm import Algorithm
from queue import Queue
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


class BFS(Algorithm):
    """
    The Breadth-first search path finding algorithm.
    This algorithm treats all movement costs as equivalent.
    i.e moving diagonally covers the same distance as moving to an adjacent box.
    So this isn't necessarily a "shortest path" in this use case because the algorithm treats
    the grid like an unweighted graph whereas in reality it is a weighted graph, but I
    still wanted to visualize it and compare it to the other ones :)
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

            # initialize everything needed for the algorithm if this is the very first iteration through it
            if not self.started:
                self.starting_box = window.boxes[window.starting_point_coords[0]][window.starting_point_coords[1]]
                self.end_box = window.boxes[window.end_point_coords[0]][window.end_point_coords[1]]
                self.q.put(self.starting_box)
                self.started = True

            # no path exists from the start to the end box
            if self.q.empty():
                return

            u = self.q.get()

            # reached the destination so back track to the start
            if u == self.end_box:
                super().highlight_path(self.end_box)
                return

            for neighbor in u.neighbors:
                # check to see if we haven't visited this neighbor yet
                if neighbor.color in [STATUS_COLORS["EMPTY"], STATUS_COLORS["END"]]:

                    # found the end/destination box so perform an early exit
                    if neighbor.color == STATUS_COLORS["END"]:
                        neighbor.parent = u
                        self.highlight_path(neighbor)

                        # empty the queue to stop future iterations of the algorithm from running
                        while not self.q.empty():
                            self.q.get()

                        return

                    neighbor.color = STATUS_COLORS["ENCOUNTERED"]
                    neighbor.parent = u
                    self.q.put(neighbor)

            if u.color != STATUS_COLORS["START"]:
                u.color = STATUS_COLORS["EXPLORED"]

        elif window.game_status == "reset":
            self.reset_algorithm(window)
