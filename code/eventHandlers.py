import pygame
from box import Box
from pygame_window import PygameWindow


class EventHanlder():
    """
    A class which contains methods to handle all events induced by the user.
    These include:
        * clicking one of the "start", "pause", "reset" buttons
        * left clicking on a box to make it a wall
        * right clicking on a box to make it a starting point
        * right clicking + pressing shift on a box to make it an end point
        * holding down left-click and dragging to draw/delete walls
    """

    def handleMouseButtonDown(self, window: PygameWindow, event: pygame.event):
        """
        Handles the following events:
            * clicking one of the "start", "pause", "reset" buttons
            * left clicking on a box to make it a wall
            * right clicking on a box to make it a starting point
            * right clicking + pressing shift on a box to make it an end point
        """
        if event.button == 3 and pygame.key.get_mods() == 1:
            # mouse position
            pos = pygame.mouse.get_pos()

            # determine which row was clicked to prevent checking boxes
            # in other rows
            row_clicked = window.get_which_row_clicked(pos)

            # current index of the box examined in row row_clicked
            boxes_i = 0
            while isinstance(row_clicked, int) and boxes_i < len(window.boxes[row_clicked]):

                # found the box
                if window.boxes[row_clicked][boxes_i].x >= pos[0] - window.box_width:

                    # if there already is a starting point, get rid of it
                    if window.end_point_coords:
                        window.boxes[window.end_point_coords[0]][window.end_point_coords[1]].toggle_end_status()

                    # make this box the end point
                    window.boxes[row_clicked][boxes_i].toggle_end_status()
                    window.end_point_coords = (row_clicked, boxes_i)
                    if (row_clicked, boxes_i) ==  window.starting_point_coords:
                        window.starting_point_coords = None

                    # end the while loop
                    boxes_i = len(window.boxes[row_clicked])

                # continue looking at each box in the row
                boxes_i += 1

        # # right mouse button was pressed
        elif event.button == 3:
            # mouse position
            pos = pygame.mouse.get_pos()

            # determine which row was clicked to prevent checking boxes
            # in other rows
            row_clicked = window.get_which_row_clicked(pos)

            # current index of the box examined in row row_clicked
            boxes_i = 0

            # find the box that was clicked
            while isinstance(row_clicked, int) and boxes_i < len(window.boxes[row_clicked]):

                # found the box
                if window.boxes[row_clicked][boxes_i].x >= pos[0] - window.box_width:
                    # reset the old start/stop points if one already exists
                    # if there already is a starting point, get rid of it
                    if window.starting_point_coords:
                        window.boxes[window.starting_point_coords[0]][window.starting_point_coords[1]].toggle_start_status()

                    window.boxes[row_clicked][boxes_i].toggle_start_status()

                    # if the end point was clicked, reset it so that
                    # it can be the starting point
                    if (row_clicked, boxes_i) ==  window.end_point_coords:
                        window.end_point_coords = None

                    # make that box the starting point!
                    window.starting_point_coords = (row_clicked, boxes_i)

                    # stop the while loop
                    boxes_i = len(window.boxes[row_clicked])

                # continue looking at each box in the row
                boxes_i += 1

        # one of the buttons was pressed
        elif event.button == 1 and pygame.mouse.get_pos()[1] >= window.screen_height:
            # position of the mouse
            pos = pygame.mouse.get_pos()

            button_names = list(window.button_coords.keys())

            # current index of the box examined in row row_clicked
            button_i = 0

            # find the button that was clicked
            while button_i < len(button_names):
                # found the button!
                if window.button_coords[button_names[button_i]][0] >= pos[0] - window.button_width:
                    # update the game status
                    window.game_status = button_names[button_i]

                    # stop the while loop
                    button_i = len(button_names)

                # continue looking at each button
                button_i += 1

        elif event.button == 1:
            # mouse position
            pos = pygame.mouse.get_pos()

            # determine which row was clicked to prevent checking boxes
            # in other rows
            row_clicked = window.get_which_row_clicked(pos)


            # current index of the box examined in row row_clicked
            boxes_i = 0

            # find the box that was clicked
            while isinstance(row_clicked, int) and boxes_i < len(window.boxes[row_clicked]):
                # found the box!
                if window.boxes[row_clicked][boxes_i].x >= pos[0] - window.box_width:
                    # reset the old start/stop points if one already exists
                    if (row_clicked, boxes_i) ==  window.starting_point_coords:
                        window.starting_point_coords = None
                    if (row_clicked, boxes_i) ==  window.end_point_coords:
                        window.end_point_coords = None

                    # make that box a wall
                    window.boxes[row_clicked][boxes_i].toggle_wall_status()

                    # stop the while loop
                    boxes_i = len(window.boxes[row_clicked])
                # continue looking at each box in the row
                boxes_i += 1


    def handleMouseMotion(self, window: PygameWindow, event: pygame.event):
        """
        Allows for users to drag and draw/remove walls on the screen.
        """
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            row_clicked = window.get_which_row_clicked(pos)
            boxes_i = 0
            while isinstance(row_clicked, int) and boxes_i < len(window.boxes[row_clicked]):
                if window.boxes[row_clicked][boxes_i].x >= pos[0] - window.box_width:

                    # ensure that that you once you drag over a box,
                    # it won't instantly 'unclick' it because we didn't
                    # drag over it fast enough.
                    # so what this does it it requires another box to be
                    # dragged over before the most recent one can be altered
                    # by dragging again.
                    if not window.last_dragged_box or window.last_dragged_box != window.boxes[row_clicked][boxes_i]:
                        if (row_clicked, boxes_i) ==  window.starting_point_coords:
                            window.starting_point_coords = None
                        if (row_clicked, boxes_i) ==  window.end_point_coords:
                            window.end_point_coords = None
                        window.last_dragged_box = window.boxes[row_clicked][boxes_i]
                        window.boxes[row_clicked][boxes_i].toggle_wall_status()

                    # stop the while loop
                    boxes_i = len(window.boxes[row_clicked])

                # continue looking at each box in the row
                boxes_i += 1
