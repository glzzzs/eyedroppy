import sys
import os
from PyQt6 import uic
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QCursor, QPixmap, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout

from eyedroppy.core.palette import Palette
from eyedroppy.ui.palette_widget import PaletteWidget

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        script_path = os.path.dirname(os.path.abspath(__file__))
        main_ui_path = os.path.join(script_path, "main.ui")
        uic.loadUi(main_ui_path, self)

        self.palette = Palette()
        self.palette_widget.palette = self.palette
        self.palette_widget.tile_clicked.connect(self.on_tile_clicked)

        self.image = None

        self.create_eyedropper_cursor()

        self.imageDropFrame.dragEnterEvent = self.frame_drag_enter
        self.imageDropFrame.dropEvent = self.frame_drop
        self.dropped_pixmap = None

        layout = self.imageDropFrame.layout()
        if layout is None:
            layout = QVBoxLayout(self.imageDropFrame)
            layout.setContentsMargins(0, 0, 0, 0)
            self.imageDropFrame.setLayout(layout)

        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.imageLabel)

    def on_tile_clicked(self, row, col):
        self.setCursor(self.eyedropper)

    def create_eyedropper_cursor(self):
        script_path = os.path.dirname(os.path.abspath(__file__))
        cursor_path = os.path.join(script_path, "../assets/icons/eyedropper.svg")
        
        cursor_x = 0
        cursor_y = 32
        cursor_pixmap = QPixmap(cursor_path)
        cursor_pixmap = cursor_pixmap.scaled(
            32, 
            32, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation)
        
        self.eyedropper = QCursor(cursor_pixmap, cursor_x, cursor_y)

    def frame_drag_enter(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def frame_drop(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.handle_file(file_path)
            event.acceptProposedAction()

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_V:
            self.handle_paste()
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        widget_at = self.childAt(event.position().toPoint())
        if self.image and event.button() == Qt.MouseButton.LeftButton:
            if isinstance(widget_at, QLabel):
                pos = event.position()
                self.palette.set_color(self.palette_widget.selected_tile[0], self.palette_widget.selected_tile[1], QColor(self.image.pixel(int(pos.x()), int(pos.y()))))
                print(f"Color: {self.image.pixel(int(pos.x()), int(pos.y()))}")

    def handle_paste(self):
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()

        if mime_data.hasImage():
            pixmap = clipboard.pixmap()
            self.image = pixmap.toImage()
            if not pixmap.isNull():
                self.set_image(pixmap)
                return

        if mime_data.hasUrls():
            file_path = mime_data.urls()[0].toLocalFile()
            self.handle_file(file_path)
            return

        if mime_data.hasText():
            print(f"Pasted Text: {mime_data.text()}")
            return

    def handle_file(self, file_path):
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            self.set_image(QPixmap(file_path))
        else:
            print(f"Dropped/Pasted/Loaded File: {file_path}")

    def set_image(self, pixmap: QPixmap):
        self.image = pixmap.toImage()
        pixmap = pixmap.scaled(
                        self.imageDropFrame.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
        self.imageLabel.setPixmap(pixmap)