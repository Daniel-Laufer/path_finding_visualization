from os import environ
from pygame_window import PygameWindow
from box import Box, STATUS_COLORS
from heapq import *
from algorithm import Algorithm
from typing import *
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


class AStarAlgorithm(Algorithm):
    """
    An implementation of the A* search algorithm.
    ===========
    q: a list which will act as a min-heap which stores boxes the algorithm still needs to explore
    """
    q: list

    def __init__(self, window: PygameWindow):
        super().__init__(window)
        self.q = []

    def run(self, window: PygameWindow):
        if not self.window.game_status:
            return
        elif self.window.game_status == 'start':

            # check if start and end points exist
            if not all([window.starting_point_coords, window.end_point_coords]):
                return

            # initialize our algorithm if this is the very first iteration through it
            if not self.started:
                self.starting_box = window.boxes[window.starting_point_coords[0]][window.starting_point_coords[1]]
                self.end_box = window.boxes[window.end_point_coords[0]][window.end_point_coords[1]]
                self.started = True

                # push the starting box onto the min-heap with a priority of 0
                #   (because it takes 0 'cost' to go from the starting box to itself)
                self.starting_box.cost = 0
                heappush(self.q, (0, self.starting_box))

            # there is no path from the start to the end. So simply don't go any further in the algorithm
            if not self.q:
                return

            # u is the box with current lowest priority.
            #   i.e the box that will take us the closest to our destination compared to all the other boxes already in
            #   the queue
            u = heappop(self.q)[1]

            # reached the destination so back track to the start
            if u == self.end_box:
                while self.q:
                    heappop(self.q)
                super().highlight_path(self.end_box)
                return

            for neighbor in u.neighbors:

                # the cost of going from vertex 'u' to 'neighbor'
                alt_cost = u.cost + Algorithm.compute_distance(u, neighbor)

                # check to see if we need to update the neighbor's cost to alt_cost (if it doesn't
                # have a cost or alt_cost < neighbor.cost)
                # and check to see if the neighbor is something other than the start node or wall nodes
                if (neighbor.cost is None or alt_cost < neighbor.cost) and neighbor.color not in [STATUS_COLORS["START"], STATUS_COLORS["WALL"]]:

                    # mark this node as "encountered" if we haven't already
                    if neighbor.color == STATUS_COLORS["EMPTY"]:
                        neighbor.color = STATUS_COLORS["ENCOUNTERED"]

                    neighbor.cost = alt_cost
                    priority = alt_cost + self.calc_heuristic(self.end_box, neighbor)
                    neighbor.parent = u  # will attribute will be used for back-tracking later
                    heappush(self.q, (priority, neighbor))

                if u.color not in [STATUS_COLORS["START"], STATUS_COLORS["WALL"]]:
                    u.color = STATUS_COLORS["EXPLORED"]

        elif window.game_status == "reset":
            self.reset_algorithm(window)

    # calculating how far box is from other if we disregard walls
    @staticmethod
    def calc_heuristic(box: Box, other: Box):
        return abs(box.x - other.x) + abs(box.y - other.y)
