from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QColor
from numpy import uint

class Palette(QObject):
    changed = pyqtSignal(uint, uint, QColor)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.rows = 2
        self.columns = 4
        self.colors = [
            [QColor("#fff15f5f"), QColor("#ff3380f2"), QColor("#ffa033f1"), QColor("#ff3380f2")],
            [QColor("#fff0e564"), QColor("#ff5fd642"), QColor("#fffff133"), QColor("#ff07bbbe")]
        ]

    def set_color(self, row: uint, column: uint, color):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            self.colors[row][column] = QColor(color)
            self.changed.emit(row, column, QColor(color))

    def get_colors(self):
        return self.colors