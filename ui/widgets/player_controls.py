import qtawesome
from PySide6.QtCore import QSize, Qt, Signal, QTimer
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QSlider, QLabel

class PlayerControlsWidget(QWidget):
    next_requested = Signal()
    prev_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.icon_color = "#E0E0E0"
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

        # --- Playback Buttons ---
        self.prev_button = QPushButton(qtawesome.icon('fa5s.step-backward', color=self.icon_color), "")
        self.prev_button.setIconSize(icon_size)
        self.prev_button.setFixedSize(icon_size)
        self.prev_button.setStyleSheet(button_style)

        self.play_icon = qtawesome.icon('fa5s.play-circle', color=self.icon_color)
        self.pause_icon = qtawesome.icon('fa5s.pause-circle', color=self.icon_color)

        self.play_button = QPushButton(self.play_icon, "")
        self.play_button.setIconSize(icon_size)
        self.play_button.setFixedSize(icon_size)
        self.play_button.setStyleSheet(button_style)

        self.next_button = QPushButton(qtawesome.icon('fa5s.step-forward', color=self.icon_color), "")
        self.next_button.setIconSize(icon_size)
        self.next_button.setFixedSize(icon_size)
        self.next_button.setStyleSheet(button_style)

        layout.addStretch()
        layout.addWidget(self.prev_button)
        layout.addWidget(self.play_button)
        layout.addWidget(self.next_button)
        layout.addStretch()

        # --- Volume Slider ---
        self.volume_container = QWidget()
        volume_layout = QHBoxLayout(self.volume_container)
        volume_layout.setContentsMargins(0,0,0,0)

        self.volume_up_icon = qtawesome.icon('fa5s.volume-up', color=self.icon_color)
        self.volume_mute_icon = qtawesome.icon('fa5s.volume-mute', color=self.icon_color)

        self.volume_button = QPushButton(self.volume_up_icon, "")
        self.volume_button.setIconSize(QSize(24, 24))
        self.volume_button.setFixedSize(QSize(32, 32))
        self.volume_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #454545;
                border-radius: 16px;
            }
        """)


        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px;
                background: #3d3d3d;
                margin: 2px 0;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #E0E0E0;
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
            QSlider::sub-page:horizontal {
                background: #E0E0E0;
                height: 4px;
                border-radius: 2px;
            }
        """)
        volume_layout.addWidget(self.volume_button)
        volume_layout.addWidget(self.volume_slider)
        layout.addWidget(self.volume_container)

        # --- Throttling ---
        self.throttle_timer = QTimer(self)
        self.throttle_timer.setSingleShot(True)
        self.throttle_timer.setInterval(500) # 500ms throttle
        self.throttle_timer.timeout.connect(self._enable_buttons)

        self.next_button.clicked.connect(self._on_next_clicked)
        self.prev_button.clicked.connect(self._on_prev_clicked)

    def _on_next_clicked(self):
        if not self.throttle_timer.isActive():
            self.next_requested.emit()
            self.next_button.setDisabled(True)
            self.prev_button.setDisabled(True)
            self.throttle_timer.start()

    def _on_prev_clicked(self):
        if not self.throttle_timer.isActive():
            self.prev_requested.emit()
            self.next_button.setDisabled(True)
            self.prev_button.setDisabled(True)
            self.throttle_timer.start()

    def _enable_buttons(self):
        self.next_button.setDisabled(False)
        self.prev_button.setDisabled(False)

    def set_play_icon(self, is_playing):
        icon = self.pause_icon if is_playing else self.play_icon
        self.play_button.setIcon(icon)

    def set_mute_icon(self, is_muted):
        icon = self.volume_mute_icon if is_muted else self.volume_up_icon
        self.volume_button.setIcon(icon)
        self.volume_slider.setDisabled(is_muted)

    def set_volume_controls_visible(self, visible):
        self.volume_container.setVisible(visible)