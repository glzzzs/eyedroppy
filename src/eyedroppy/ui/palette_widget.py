from PyQt6.QtCore import Qt, QRectF, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget
from numpy import uint

from eyedroppy.core.palette import Palette

class PaletteWidget(QWidget):
    tile_clicked = pyqtSignal(int, int)

    def __init__(self, palette=None, parent=None):
        super().__init__(parent)
        self.palette = palette if palette is not None else Palette()
        self.tile_width = 110
        self.tile_height = 32
        self.tile_spacing_x = 1
        self.tile_spacing_y = 1
        self.tile_rounding = 0
        self.margin_x = 4
        self.margin_y = 4
        self.selected_tile = None
        self.setMinimumSize(200, 450)

        self.palette.changed.connect(self.on_palette_changed)

    def on_palette_changed(self, row: uint, column: uint, color: QColor):
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        colors = self.palette.get_colors()
        for row in range(self.palette.rows):
            for col in range(self.palette.columns):
                x = self.margin_x + col * (self.tile_width + self.tile_spacing_x)
                y = self.margin_y + row * (self.tile_height + self.tile_spacing_y)

                painter.setBrush(QBrush(colors[row][col], Qt.BrushStyle.SolidPattern))

                if self.selected_tile == (row, col):
                    painter.setPen(QPen(QColor("#1f2328"), 2))
                else:
                    painter.setPen(QPen(QColor("#d0d7de"), 1))

                painter.drawRoundedRect(QRectF(x, y, self.tile_width, self.tile_height), self.tile_rounding, self.tile_rounding)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            col = uint((pos.x() - self.margin_x) // (self.tile_width + self.tile_spacing_x))
            row = uint((pos.y() - self.margin_y) // (self.tile_height + self.tile_spacing_y))

            if 0 <= row < self.palette.rows and 0 <= col < self.palette.columns:
                self.selected_tile = (row, col)
                self.tile_clicked.emit(row, col)
                self.update()

        super().mousePressEvent(event)