import sys

from PyQt6.QtWidgets import QApplication, QLabel


def main() -> int:
    app = QApplication(sys.argv)
    window = QLabel("Hi, droppy 👁️")
    window.setWindowTitle("eyedroppy")
    window.resize(400, 300)
    window.show()
    return app.exec()
