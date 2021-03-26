from datetime import datetime

STATUS_COLORS = {"EMPTY": (255, 255, 255), "WALL": (0, 0, 0), "START": (50, 205, 50), "END": (255, 0, 0), 'PROCESSED': (255, 0, 255), 'TO_PROCESS': (128, 0, 255)}
class Box:
    def __init__(self, x: int, y: int, width: int, height: int, row: int, col: int) -> None:
        self.color = (255, 255, 255)
        self.status = "EMPTY"
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.f_cost = 0
        self.g_cost = 0
        self.h_cost = 0
        self.row = row
        self.col = col
        self.neighbors = []
        self.parent = None

    def toggle_wall_status(self) -> None:
        if self.status != "WALL":
            self.status = "WALL"
            self.color = STATUS_COLORS['WALL']
            return
        self.status = "EMPTY"
        self.color = STATUS_COLORS['EMPTY']

    def toggle_start_status(self) -> None:
        if self.status != "START":
            self.status = "START"
            self.color = STATUS_COLORS['START']
            return
        self.status = "EMPTY"
        self.color = STATUS_COLORS['EMPTY']

    def toggle_end_status(self) -> None:
        if self.status != "END":
            self.status = "END"
            self.color = STATUS_COLORS['END']
            return
        self.status = "EMPTY"
        self.color = STATUS_COLORS['EMPTY']

    def toggle_processed(self) -> None:
        self.status = 'PROCESSED'
        self.color = STATUS_COLORS['PROCESSED']

    def toggle_to_process(self) -> None:
        self.status == 'TO_PROCESS'
        self.color = STATUS_COLORS['TO_PROCESS']


    def __eq__(self, other):
        return self.row == other.row and self.col == other.col


    def __repr__(self) -> str:
        return '({}, {})'.format(self.row, self.col)




