import sys
import os
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QCursor, QPixmap, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        script_path = os.path.dirname(os.path.abspath(__file__))
        main_ui_path = os.path.join(script_path, "main.ui")
        uic.loadUi(main_ui_path, self)

        self.set_eyedropper_cursor()

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

    def set_eyedropper_cursor(self):
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
        custom_cursor = QCursor(cursor_pixmap, cursor_x, cursor_y)
        self.setCursor(custom_cursor)

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

    def handle_paste(self):
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()

        if mime_data.hasImage():
            pixmap = clipboard.pixmap()
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
        pixmap = pixmap.scaled(
                        self.imageDropFrame.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
        self.imageLabel.setPixmap(pixmap)