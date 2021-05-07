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

    Public Attributes:
    ===========
    window: the pygame window
    """
    window: PygameWindow

    def __init__(self, window: PygameWindow):
        self.window = window

    def handleMouseButtonDown(self, event: pygame.event):
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
            row_clicked = self.window.get_which_row_clicked(pos)

            # current index of the box examined in row row_clicked
            boxes_i = 0
            while isinstance(row_clicked, int) and boxes_i < len(self.window.boxes[row_clicked]):

                # found the box
                if self.window.boxes[row_clicked][boxes_i].x >= pos[0] - self.window.box_width:

                    # if there already is a starting point, get rid of it
                    if self.window.end_point_coords:
                        self.window.boxes[self.window.end_point_coords[0]][self.window.end_point_coords[1]].toggle_end_status()

                    # make this box the end point
                    self.window.boxes[row_clicked][boxes_i].toggle_end_status()
                    self.window.end_point_coords = (row_clicked, boxes_i)
                    if (row_clicked, boxes_i) ==  self.window.starting_point_coords:
                        self.window.starting_point_coords = None

                    # end the while loop
                    boxes_i = len(self.window.boxes[row_clicked])

                # continue looking at each box in the row
                boxes_i += 1

        # # right mouse button was pressed
        elif event.button == 3:
            # mouse position
            pos = pygame.mouse.get_pos()

            # determine which row was clicked to prevent checking boxes
            # in other rows
            row_clicked = self.window.get_which_row_clicked(pos)

            # current index of the box examined in row row_clicked
            boxes_i = 0

            # find the box that was clicked
            while isinstance(row_clicked, int) and boxes_i < len(self.window.boxes[row_clicked]):

                # found the box
                if self.window.boxes[row_clicked][boxes_i].x >= pos[0] - self.window.box_width:
                    # reset the old start/stop points if one already exists
                    # if there already is a starting point, get rid of it
                    if self.window.starting_point_coords:
                        self.window.boxes[self.window.starting_point_coords[0]][self.window.starting_point_coords[1]].toggle_start_status()

                    self.window.boxes[row_clicked][boxes_i].toggle_start_status()

                    # if the end point was clicked, reset it so that
                    # it can be the starting point
                    if (row_clicked, boxes_i) ==  self.window.end_point_coords:
                        self.window.end_point_coords = None

                    # make that box the starting point!
                    self.window.starting_point_coords = (row_clicked, boxes_i)

                    # stop the while loop
                    boxes_i = len(self.window.boxes[row_clicked])

                # continue looking at each box in the row
                boxes_i += 1

        # one of the buttons was pressed
        elif event.button == 1 and pygame.mouse.get_pos()[1] >= self.window.screen_height:
            # position of the mouse
            pos = pygame.mouse.get_pos()

            button_names = list(self.window.button_coords.keys())

            # current index of the box examined in row row_clicked
            button_i = 0

            # find the button that was clicked
            while button_i < len(button_names):
                # found the button!
                if self.window.button_coords[button_names[button_i]][0] >= pos[0] - self.window.button_width:
                    # update the game status
                    self.window.game_status = button_names[button_i]

                    # stop the while loop
                    button_i = len(button_names)

                # continue looking at each button
                button_i += 1

        elif event.button == 1:
            # mouse position
            pos = pygame.mouse.get_pos()

            # determine which row was clicked to prevent checking boxes
            # in other rows
            row_clicked = self.window.get_which_row_clicked(pos)


            # current index of the box examined in row row_clicked
            boxes_i = 0

            # find the box that was clicked
            while isinstance(row_clicked, int) and boxes_i < len(self.window.boxes[row_clicked]):
                # found the box!
                if self.window.boxes[row_clicked][boxes_i].x >= pos[0] - self.window.box_width:
                    # reset the old start/stop points if one already exists
                    if (row_clicked, boxes_i) ==  self.window.starting_point_coords:
                        self.window.starting_point_coords = None
                    if (row_clicked, boxes_i) ==  self.window.end_point_coords:
                        self.window.end_point_coords = None

                    # make that box a wall
                    self.window.boxes[row_clicked][boxes_i].toggle_wall_status()

                    # stop the while loop
                    boxes_i = len(self.window.boxes[row_clicked])
                # continue looking at each box in the row
                boxes_i += 1


    def handleMouseMotion(self, even: pygame.event):
        """
        Allows for users to drag and draw/remove walls on the screen. 
        """
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            row_clicked = self.window.get_which_row_clicked(pos)
            boxes_i = 0
            while isinstance(row_clicked, int) and boxes_i < len(self.window.boxes[row_clicked]):
                if self.window.boxes[row_clicked][boxes_i].x >= pos[0] - self.window.box_width:

                    # ensure that that you once you drag over a box,
                    # it won't instantly 'unclick' it because we didn't
                    # drag over it fast enough.
                    # so what this does it it requires another box to be
                    # dragged over before the most recent one can be altered
                    # by dragging again.
                    if not self.window.last_dragged_box or self.window.last_dragged_box != self.window.boxes[row_clicked][boxes_i]:
                        if (row_clicked, boxes_i) ==  self.window.starting_point_coords:
                            self.window.starting_point_coords = None
                        if (row_clicked, boxes_i) ==  self.window.end_point_coords:
                            self.window.end_point_coords = None
                        self.window.last_dragged_box = self.window.boxes[row_clicked][boxes_i]
                        self.window.boxes[row_clicked][boxes_i].toggle_wall_status()
                        
                    # stop the while loop
                    boxes_i = len(self.window.boxes[row_clicked])

                # continue looking at each box in the row
                boxes_i += 1