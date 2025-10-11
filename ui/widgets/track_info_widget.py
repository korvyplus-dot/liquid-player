from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class TrackInfoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(2)

        self.title_label = QLabel("No track loaded")
        self.artist_label = QLabel("")

        # --- Styling ---
        title_font = self.font()
        title_font.setPointSize(12)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #E0E0E0;") # Белый
        self.title_label.setAlignment(Qt.AlignCenter)

        artist_font = self.font()
        artist_font.setPointSize(10)
        self.artist_label.setFont(artist_font)
        self.artist_label.setStyleSheet("color: #9E9E9E;") # Серый
        self.artist_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.title_label)
        layout.addWidget(self.artist_label)

    def set_track_info(self, title, artist):
        self.title_label.setText(title or "Unknown Title")
        self.artist_label.setText(artist or "Unknown Artist")