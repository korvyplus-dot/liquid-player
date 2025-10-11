from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize
import qtawesome

class AlbumArtWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 200)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        self.album_art_label = QLabel()
        self.album_art_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.album_art_label)

        # Set a default placeholder icon
        self.default_pixmap = qtawesome.icon('fa5s.music', color='#555555').pixmap(QSize(150, 150))
        self.set_album_art(None)

    def set_album_art(self, image_path):
        if image_path and image_path.startswith('file:///'):
            pixmap = QPixmap(image_path[8:]) # QPixmap needs a clean path, remove 'file:///'
        else:
            pixmap = self.default_pixmap
        self.album_art_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))