from PyQt6.QtGui import QColor
from numpy import uint

class Palette:
    def __init__(self, rows=4, columns=4):
        self.rows = rows
        self.columns = columns
        self.colors = [[QColor("#ebedf0") for _ in range(self.columns)] for _ in range(self.rows)]

    def set_color(self, row: uint, column: uint, color):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            self.colors[row][column] = QColor(color)

    def get_colors(self):
        return self.colors