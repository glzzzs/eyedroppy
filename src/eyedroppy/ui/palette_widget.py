from PyQt6.QtCore import Qt, QRectF, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget

from eyedroppy.core.palette import Palette

class PaletteWidget(QWidget):
    tile_clicked = pyqtSignal(int, int)

    def __init__(self, palette=None, parent=None):
        super().__init__(parent)
        self.palette = palette if palette is not None else Palette(rows=4, columns=4)
        self.tile_size = 32
        self.tile_spacing = 4
        self.margin = 10
        self.selected_tile = None
        self.setMinimumSize(200, 200)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        colors = self.palette.get_colors()
        for row in range(self.palette.rows):
            for col in range(self.palette.columns):
                x = self.margin + col * (self.tile_size + self.tile_spacing)
                y = self.margin + row * (self.tile_size + self.tile_spacing)

                painter.setBrush(QBrush(colors[row][col]))

                if self.selected_tile == (row, col):
                    painter.setPen(QPen(QColor("#1f2328"), 2))
                else:
                    painter.setPen(QPen(QColor("#d0d7de"), 1))

                painter.drawRoundedRect(QRectF(x, y, self.tile_size, self.tile_size), 6, 6)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            col = int((pos.x() - self.margin) // (self.tile_size + self.tile_spacing))
            row = int((pos.y() - self.margin) // (self.tile_size + self.tile_spacing))

            if 0 <= row < self.palette.rows and 0 <= col < self.palette.columns:
                self.selected_tile = (row, col)
                self.tile_clicked.emit(row, col)
                self.update()
        super().mousePressEvent(event)