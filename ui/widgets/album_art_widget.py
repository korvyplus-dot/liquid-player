from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize
import qtawesome
from urllib.parse import unquote

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
        self.pixmap = None
        self.set_album_art(None)

    def set_album_art(self, image_path):
        if image_path and image_path.startswith('file:///'):
            path = unquote(image_path[8:])
            self.pixmap = QPixmap(path)
        else:
            self.pixmap = self.default_pixmap
        
        if self.pixmap.isNull():
            self.pixmap = self.default_pixmap

        self.update_pixmap()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_pixmap()

    def update_pixmap(self):
        if self.pixmap:
            self.album_art_label.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))