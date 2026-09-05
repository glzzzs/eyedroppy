from PyQt6.QtGui import QColor
from numpy import uint

class Palette:
    def __init__(self):
        self.rows = 2
        self.columns = 2
        self.colors = [
            [QColor("#fff15f5f"), QColor("#ff3380f2")],
            [QColor("#fff0e564"), QColor("#ff5fd642")]
        ]

    def set_color(self, row: uint, column: uint, color):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            self.colors[row][column] = QColor(color)

    def get_colors(self):
        return self.colors