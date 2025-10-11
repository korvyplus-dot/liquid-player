import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from .widgets.player_controls import PlayerControlsWidget
from .widgets.progress_slider import ProgressSlider
from .widgets.album_art_widget import AlbumArtWidget
from .widgets.track_info_widget import TrackInfoWidget
from core.player import Player

def find_music_files(root_dir):
    """
    Recursively finds all music files in a directory.
    """
    supported_formats = ('.mp3', '.flac', '.wav', '.m4a', '.ogg')
    music_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(supported_formats):
                music_files.append(os.path.join(root, file))
    return music_files

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Liquid Player")
        self.resize(400, 500)
        self.setMinimumSize(350, 450)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: #2d2d2d;")

        # --- Widgets ---
        self.album_art = AlbumArtWidget()
        self.track_info = TrackInfoWidget()
        self.progress_slider = ProgressSlider()
        self.controls = PlayerControlsWidget()

        # --- Playlist ---
        # Dynamically find the user's music directory
        music_directory = os.path.join(Path.home(), "Music")
        if os.path.isdir(music_directory):
            self.playlist = find_music_files(music_directory)
        else:
            self.playlist = [] # Start with an empty playlist if the directory doesn't exist

        # --- Player Core ---
        self.player = Player(playlist=self.playlist)

        # --- Connections ---
        # Connect player signals to UI slots
        self.player.state_changed.connect(self.controls.set_play_icon)
        self.player.position_changed.connect(self.progress_slider.update_progress)
        self.player.album_art_changed.connect(self.album_art.set_album_art)
        self.player.track_info_changed.connect(self.track_info.set_track_info)
        self.player.mute_changed.connect(self.controls.set_mute_icon)
        self.player.end_reached.connect(self.player.next) # Safely handle track end

        # Connect UI controls to player slots
        self.controls.play_button.clicked.connect(self.toggle_play)
        self.controls.next_button.clicked.connect(self.player.next)
        self.controls.prev_button.clicked.connect(self.player.previous)
        self.controls.volume_button.clicked.connect(self.player.toggle_mute)
        self.progress_slider.seek_requested.connect(self.player.seek)
        self.controls.volume_slider.valueChanged.connect(self.player.set_volume)
        self.controls.volume_slider.setValue(70) # Set initial slider position

        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(self.album_art, 5) # Give it more stretch factor
        main_layout.addWidget(self.track_info)
        main_layout.addWidget(self.progress_slider)
        main_layout.addWidget(self.controls)
        main_layout.addStretch(1)

    def toggle_play(self):
        self.player.play_pause() # The icon will be updated automatically by the callback

def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
