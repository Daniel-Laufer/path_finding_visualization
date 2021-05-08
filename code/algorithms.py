from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame_window import PygameWindow
from box import Box

class A_Star_algorithm():
    def __init__(self) -> None:
        self.closed_set = []
        self.starting_node = None
        self.open_set = []
        self.current_node = None
        self.started = False

    def run(self, window: PygameWindow):

        if not window.game_status:
            return
        elif window.game_status == 'start':
            # check if start and end points exist
            if not all([window.starting_point_coords, window.end_point_coords]):
                return
            elif not self.started:
                self.starting_node = window.boxes[window.starting_point_coords[0]][window.starting_point_coords[1]]
                self.open_set.append(self.starting_node)
                self.started = True

            if len(self.open_set) == 0:
                return


            for node in self.closed_set:
                if (node.row, node.col) != window.starting_point_coords and (node.row, node.col) != window.end_point_coords:
                    node.toggle_visisted()

            for node in self.open_set:
                if (node.row, node.col) != window.starting_point_coords and (node.row, node.col) != window.end_point_coords:
                    node.toggle_to_visit()

            lowest_f_cost_index = 0
            for i, node in enumerate(self.open_set):
                if node.f_cost < self.open_set[lowest_f_cost_index].f_cost:
                    lowest_f_cost_index = i

            current = self.open_set[lowest_f_cost_index]
            if (current.row, current.col) == window.end_point_coords:
                self.highlight_path(window, current)
                window.game_status = "pause"
                return

            # add to closed set
            node_to_add_to_closed = self.open_set.pop(lowest_f_cost_index)
            # node_to_add_to_closed.toggle_processed()
            self.closed_set.append(node_to_add_to_closed)

            for i, neighbor in enumerate(current.neighbors):
                if neighbor not in self.closed_set and neighbor.status != 'WALL':
                    temp_g_cost = current.g_cost + 1 # neighbor is one away from the current node!
                    if neighbor in self.open_set:
                        # if the neighbor's g cost was already evaluated previously, check to see if
                        # its g_cost in this path is lower, if it is, then update the g_cost
                        # tldr we found a better path to this neighbor than in a previous attempt
                        if temp_g_cost < neighbor.g_cost:
                            neighbor.g_cost = temp_g_cost
                    else:
                        neighbor.g_cost = temp_g_cost
                        # neighbor.toggle_to_process()
                        self.open_set.append(neighbor)

                    neighbor.h_cost = self.calc_heuristic(neighbor, window.boxes[window.end_point_coords[0]][window.end_point_coords[1]])
                    neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                    neighbor.parent = current

        elif window.game_status == 'pause':
            # do nothing
            return
        elif window.game_status == 'reset':
            self.__init__()
            window.boxes = []
            window.row_coords = []
            window.setup_grid()
            window.last_dragged_box, window.game_status, window.starting_point_coords, window.end_point_coords = None, None, None, None

    def calc_heuristic(self, neighbor: Box, end_node: Box):
        return (neighbor.row - end_node.row) ** 2 + (neighbor.col - end_node.col) ** 2

    def highlight_path(self, window: PygameWindow, box: Box) -> None:
        if not box or not box.parent:
            return
        if (box.row, box.col) != window.starting_point_coords and (box.row, box.col) != window.end_point_coords:
            box.color = (0, 0, 255)
        self.highlight_path(window, box.parent)