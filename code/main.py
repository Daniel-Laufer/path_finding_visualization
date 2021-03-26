import pygame
from initialization import initialize_screen
import math
from box import Box
from typing import Tuple
from a_star_algorithm import A_Star
import random


COLORS = {'black': (0, 0, 0), 'white': (255, 255, 255), 'green': (0, 255, )}
button_row_height = 50
screen_width = 500
screen_height = 500
num_boxes_horizontally = 80
num_boxes_vertically = 80
box_width = math.floor(screen_width / num_boxes_horizontally)
box_height = math.floor(screen_height / num_boxes_vertically)

a_star = None

# Tuple that has the form of: (row: int, column: int)
starting_point_coords = None
# Tuple that has the form of: (row: int, column: int)
end_point_coords = None

button_coords = {'start': None, 'pause': None, 'reset': None} # each value is
# either None or is a tuple of form (int, int)
button_colors = {'start': (0, 255, 0), 'pause': (255, 165, 0), 'reset': (255, 0, 0)}
button_width = 100
button_height = 45

game_status = None # can either be None (waiting for inputs), 'start', 'pause', 'reset'


running, screen = initialize_screen(screen_width, screen_height + button_row_height)
font = pygame.font.SysFont("arialroundedboldttf", 12)

# list to stores a reference to each 'box' in the grid
# ex.
# >>> boxes[1][0]  # the 0th box from the 1st row
# {coords: (0, 100), ref: ADDRESS OF BOX OBJECT } where (0, 100)
#       refers to the top left corner of the box
boxes = []


# list to stores y pos of the top left corner of the 0th box in each row of grid
row_coords = []


def setup_grid(w: int, h: int) -> None:
    # coords to keep track of where each box is being drawn
    global boxes
    global row_coords
    global a_star

    boxes = []
    row_coords = []
    curr_x = 0
    curr_y = 0
    # index in 'boxes' list
    boxes_i = 0

    # drawing the grid layer by layer
    while (curr_y + box_height) < h :
        curr_x = 0
        boxes.append([])
        while (curr_x + box_width) < w:
            boxes[boxes_i].append(Box(curr_x, curr_y, box_width, box_height, len(boxes) - 1, len(boxes[boxes_i]) ))
            curr_x += box_width
        row_coords.append(curr_y)
        curr_y += box_height
        boxes_i += 1
    set_neighbors_of_each_box()

def generate_random_walls() -> None:
    for row in boxes:
        for box in row:
            if random.random() > 0.5:
                box.toggle_wall_status()

def set_neighbors_of_each_box():
    global boxes
    global num_boxes_vertically
    global num_boxes_horizontally

    for i, row in enumerate(boxes):
        for j, box in enumerate(row):
            if i > 0:
                box.neighbors.append(boxes[i - 1][j]) # top
                if j > 0:
                    box.neighbors.append(boxes[i - 1][j - 1]) # top left
                if j < len(row) - 1:
                    box.neighbors.append(boxes[i - 1][j + 1]) # top right
            if j > 0:
                box.neighbors.append(boxes[i][j - 1]) # left
            if i < len(boxes) - 1:
                box.neighbors.append(boxes[i + 1][j]) # bottom
                if j > 0:
                    box.neighbors.append(boxes[i + 1][j - 1]) # bottom left
                if j < len(row) - 1:
                    box.neighbors.append(boxes[i + 1][j + 1]) # bottom right
            if j < len(row) - 1:
                box.neighbors.append(boxes[i][j + 1]) # right



def draw_grid():
    for row in boxes:
        for box in row:
            if box.status == 'EMPTY':
                pygame.draw.rect(screen, COLORS['black'],(box.x, box.y, box.width, box.height), 1)
            else:
                pygame.draw.rect(screen, box.color ,(box.x, box.y, box.width, box.height), 0)


def get_which_row_clicked(pos: Tuple[int, int]):

    for i, y in enumerate(row_coords):

        if y >= pos[1]:

            return i - 1

    return len(row_coords) - 1


def draw_buttons():
    horiz_margin = 10
    vert_margin = 0
    button_coords['start'] = (horiz_margin, vert_margin + screen_height, vert_margin + screen_height)
    button_coords['pause'] = (horiz_margin * 2 + button_width, vert_margin + screen_height)
    button_coords['reset'] = ((horiz_margin * 3 + button_width * 2), vert_margin + screen_height)

    for button in button_coords:
        text = font.render(button.title(), True, (0, 0, 0))
        horiz_button_padding = (button_width - text.get_width()) // 2
        vert_button_padding = (button_height - text.get_height()) // 2
        pygame.draw.rect(screen, button_colors[button],(button_coords[button][0], button_coords[button][1], button_width, button_height))
        screen.blit(text, (button_coords[button][0] + horiz_button_padding , button_coords[button][1] + vert_button_padding))


def dijkstra_alg():
    global game_status
    global last_dragged_box
    global starting_point_coords
    global end_point_coords

    if not game_status:
        return
    elif game_status == 'start':
        # check if start and end points exist
        if not all([starting_point_coords, end_point_coords]):
            return
        # continue doing the alg

    elif game_status == 'pause':
        # do nothing
        return
    elif game_status == 'reset':
        setup_grid(screen_width, screen_height)
        last_dragged_box, game_status, starting_point_coords, end_point_coords = None, None, None, None



def calc_heuristic(neighbor, end_node):
    return (neighbor.row - end_node.row) ** 2 + (neighbor.col - end_node.col) ** 2



def highlight_path(node) -> None:
    if not node or not node.parent:
        return
    if (node.row, node.col) != starting_point_coords and (node.row, node.col) != end_point_coords:
        node.color = (0, 0, 255)
    highlight_path(node.parent)

def a_star_alg():
    global game_status
    global last_dragged_box
    global starting_point_coords
    global end_point_coords
    global a_star

    if not game_status:
        return
    elif game_status == 'start':
        # check if start and end points exist
        if not all([starting_point_coords, end_point_coords]):
            return

        if not a_star:
            a_star = A_Star()
            a_star.starting_node = boxes[starting_point_coords[0]][starting_point_coords[1]]
            a_star.open_set.append(a_star.starting_node)

        if not a_star.open_set: # open set is empty
            return

        for node in a_star.closed_set:
            if (node.row, node.col) != starting_point_coords and (node.row, node.col) != end_point_coords:
                node.toggle_processed()

        for node in a_star.open_set:
            if (node.row, node.col) != starting_point_coords and (node.row, node.col) != end_point_coords:
                node.toggle_to_process()

        lowest_f_cost_index = 0
        for i, node in enumerate(a_star.open_set):
            if node.f_cost < a_star.open_set[lowest_f_cost_index].f_cost:
                lowest_f_cost_index = i

        current = a_star.open_set[lowest_f_cost_index]
        if (current.row, current.col) == end_point_coords:
            highlight_path(current)
            game_status = "pause"
            return

        # add to closed set
        node_to_add_to_closed = a_star.open_set.pop(lowest_f_cost_index)
        # node_to_add_to_closed.toggle_processed()
        a_star.closed_set.append(node_to_add_to_closed)

        for i, neighbor in enumerate(current.neighbors):
            if neighbor not in a_star.closed_set and neighbor.status != 'WALL':
                temp_g_cost = current.g_cost + 1 # neighbor is one away from the current node!
                if neighbor in a_star.open_set:
                    # if the neighbor's g cost was already evaluated previously, check to see if
                    # its g_cost in this path is lower, if it is, then update the g_cost
                    # tldr we found a better path to this neighbor than in a previous attempt
                    if temp_g_cost < neighbor.g_cost:
                        neighbor.g_cost = temp_g_cost
                else:
                    neighbor.g_cost = temp_g_cost
                    # neighbor.toggle_to_process()
                    a_star.open_set.append(neighbor)

                neighbor.h_cost = calc_heuristic(neighbor, boxes[end_point_coords[0]][end_point_coords[1]])
                neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                neighbor.parent = current

    elif game_status == 'pause':
        # do nothing
        return
    elif game_status == 'reset':
        setup_grid(screen_width, screen_height)
        a_star = None
        last_dragged_box, game_status, starting_point_coords, end_point_coords = None, None, None, None


setup_grid(screen_width, screen_height)
generate_random_walls()
last_dragged_box = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # a mouse button was pressed
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 3 and pygame.key.get_mods() == 1:
                # mouse position
                pos = pygame.mouse.get_pos()

                # determine which row was clicked to prevent checking boxes
                # in other rows
                row_clicked = get_which_row_clicked(pos)

                # current index of the box examined in row row_clicked
                boxes_i = 0
                while isinstance(row_clicked, int) and boxes_i < len(boxes[row_clicked]):

                    # found the box!
                    if boxes[row_clicked][boxes_i].x >= pos[0] - box_width:

                        # if there already is a starting point, get rid of it
                        if end_point_coords:
                            boxes[end_point_coords[0]][end_point_coords[1]].toggle_end_status()

                        # make this box the end point!
                        boxes[row_clicked][boxes_i].toggle_end_status()
                        end_point_coords = (row_clicked, boxes_i)
                        if (row_clicked, boxes_i) ==  starting_point_coords:
                            starting_point_coords = None

                        # end the while loop
                        boxes_i = len(boxes[row_clicked])

                    # continue looking at each box in the row
                    boxes_i += 1

            # right mouse button was pressed
            elif event.button == 3:
                # mouse position
                pos = pygame.mouse.get_pos()

                # determine which row was clicked to prevent checking boxes
                # in other rows
                row_clicked = get_which_row_clicked(pos)

                # current index of the box examined in row row_clicked
                boxes_i = 0

                # find the box that was clicked
                while isinstance(row_clicked, int) and boxes_i < len(boxes[row_clicked]):
                    # found the box!
                    if boxes[row_clicked][boxes_i].x >= pos[0] - box_width:
                        # reset the old start/stop points if one already exists
                        # if there already is a starting point, get rid of it!
                        if starting_point_coords:
                            boxes[starting_point_coords[0]][starting_point_coords[1]].toggle_start_status()
                        boxes[row_clicked][boxes_i].toggle_start_status()

                        # if the end point was clicked, reset it so that
                        # it can be the starting point
                        if (row_clicked, boxes_i) ==  end_point_coords:
                            end_point_coords = None

                        # make that box the starting point!
                        starting_point_coords = (row_clicked, boxes_i)

                        # stop the while loop
                        boxes_i = len(boxes[row_clicked])

                    # continue looking at each box in the row
                    boxes_i += 1

            # one of the buttons was pressed
            elif event.button == 1 and pygame.mouse.get_pos()[1] >= screen_height:
                # position of the mouse
                pos = pygame.mouse.get_pos()

                button_names = list(button_coords.keys())

                # current index of the box examined in row row_clicked
                button_i = 0

                # find the button that was clicked
                while button_i < len(button_names):
                    # found the button!
                    if button_coords[button_names[button_i]][0] >= pos[0] - button_width:
                        # update the game status
                        game_status = button_names[button_i]
                        # stop the while loop
                        button_i = len(button_names)
                    # continue looking at each button
                    button_i += 1

            elif event.button == 1:
                # mouse position
                pos = pygame.mouse.get_pos()

                # determine which row was clicked to prevent checking boxes
                # in other rows
                row_clicked = get_which_row_clicked(pos)


                # current index of the box examined in row row_clicked
                boxes_i = 0

                # find the box that was clicked
                while isinstance(row_clicked, int) and boxes_i < len(boxes[row_clicked]):
                    # found the box!
                    if boxes[row_clicked][boxes_i].x >= pos[0] - box_width:
                        # reset the old start/stop points if one already exists
                        if (row_clicked, boxes_i) ==  starting_point_coords:
                            starting_point_coords = None
                        if (row_clicked, boxes_i) ==  end_point_coords:
                            end_point_coords = None

                        # make that box a wall!
                        boxes[row_clicked][boxes_i].toggle_wall_status()

                        # stop the while loop
                        boxes_i = len(boxes[row_clicked])
                    # continue looking at each box in the row
                    boxes_i += 1

        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row_clicked = get_which_row_clicked(pos)
                boxes_i = 0
                while isinstance(row_clicked, int) and boxes_i < len(boxes[row_clicked]):
                    if boxes[row_clicked][boxes_i].x >= pos[0] - box_width:
                        # ensure that that you once you drag over a box,
                        # it won't instantly 'unclick' it because we didn't
                        # drag over it fast enough.
                        # so what this does it it requires another box to be
                        # dragged over before the most recent one can be altered
                        # by dragging again.
                        if not last_dragged_box or last_dragged_box != boxes[row_clicked][boxes_i]:
                            if (row_clicked, boxes_i) ==  starting_point_coords:
                                starting_point_coords = None
                            if (row_clicked, boxes_i) ==  end_point_coords:
                                end_point_coords = None
                            last_dragged_box = boxes[row_clicked][boxes_i]
                            boxes[row_clicked][boxes_i].toggle_wall_status()
                        # stop the while loop
                        boxes_i = len(boxes[row_clicked])
                    # continue looking at each box in the row
                    boxes_i += 1

    screen.fill((255, 255, 255))
    draw_grid()
    draw_buttons()
    # dijkstra_alg()
    a_star_alg()
    pygame.display.flip()


pygame.quit()
