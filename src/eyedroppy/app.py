import sys
import os
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout

class EyeDroppyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_ui_path = os.path.join(script_dir, "../../ui/main.ui")
        uic.loadUi(main_ui_path, self)

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

    def frame_drag_enter(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def frame_drop(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()

            pixmap = QPixmap(file_path).scaled(
                self.imageDropFrame.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            self.imageLabel.setPixmap(pixmap)
            event.acceptProposedAction()

def main() -> int:
    app = QApplication(sys.argv)
    window = EyeDroppyApp()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
