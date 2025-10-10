import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from .widgets.player_controls import PlayerControlsWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Liquid Player")
        self.resize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: #2d2d2d;")

        self.controls = PlayerControlsWidget()

        main_layout = QVBoxLayout(central_widget)
        main_layout.addStretch(5)
        main_layout.addWidget(self.controls)
        main_layout.addStretch(1)

def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
