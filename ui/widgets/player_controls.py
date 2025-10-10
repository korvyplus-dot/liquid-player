import qtawesome
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout

class PlayerControlsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        icon_color = "#E0E0E0"
        icon_size = QSize(48, 48)

        button_style = """
        QPushButton {
            border: none;
            background-color: transparent;
        }
        QPushButton:hover {
            background-color: #454545;
            border-radius: 24px;
        }
        QPushButton:pressed {
            background-color: #555555;
        }
        """

        self.prev_button = QPushButton(qtawesome.icon('fa5s.step-backward', color=icon_color), "")
        self.prev_button.setIconSize(icon_size)
        self.prev_button.setFixedSize(icon_size)
        self.prev_button.setStyleSheet(button_style)

        self.play_button = QPushButton(qtawesome.icon('fa5s.play-circle', color=icon_color), "")
        self.play_button.setIconSize(icon_size)
        self.play_button.setFixedSize(icon_size)
        self.play_button.setStyleSheet(button_style)

        self.next_button = QPushButton(qtawesome.icon('fa5s.step-forward', color=icon_color), "")
        self.next_button.setIconSize(icon_size)
        self.next_button.setFixedSize(icon_size)
        self.next_button.setStyleSheet(button_style)

        layout.addStretch()
        layout.addWidget(self.prev_button)
        layout.addWidget(self.play_button)
        layout.addWidget(self.next_button)
        layout.addStretch()
