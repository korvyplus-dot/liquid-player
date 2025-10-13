import vlc
import os
from PySide6.QtCore import QObject, Signal
import mutagen
import tempfile

def get_album_art(track_path):
    """
    Extracts album art from a music file and saves it to a temporary file.
    Returns the path to the temporary file, or None if no art is found.
    """
    try:
        audio = mutagen.File(track_path, easy=True)
        if audio is None:
            return None

        if 'APIC:' in audio:
            artwork = audio['APIC:'].data
            ext = audio['APIC:'].mime.split('/')[-1]
            with tempfile.NamedTemporaryFile(suffix=f'.{ext}', delete=False) as tmp:
                tmp.write(artwork)
                return "file:///" + tmp.name.replace('\\', '/')
        # Fallback for FLAC files
        elif hasattr(audio, 'pictures') and audio.pictures:
            artwork = audio.pictures[0].data
            ext = audio.pictures[0].mime.split('/')[-1]
            with tempfile.NamedTemporaryFile(suffix=f'.{ext}', delete=False) as tmp:
                tmp.write(artwork)
                return "file:///" + tmp.name.replace('\\', '/')

    except Exception as e:
        print(f"Error extracting album art: {e}")
    return None


class Player(QObject):
    # --- Signals to safely update the UI from any thread ---
    state_changed = Signal(bool)
    position_changed = Signal(int, int)
    album_art_changed = Signal(str)
    track_info_changed = Signal(str, str)
    mute_changed = Signal(bool)
    end_reached = Signal() # Signal to notify the main thread that the track has ended

    def __init__(self, playlist):
        super().__init__()
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.playlist = playlist
        self.current_track_index = 0
        self._is_muted = False

        # Load the first track if the playlist is not empty
        if self.playlist:
            self._load_track()

        # Set initial volume
        self.set_volume(70)

        # Ensure the player starts unmuted and the UI is synced
        self.set_mute(False)

        events = self.player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerPlaying, self.on_playing)
        events.event_attach(vlc.EventType.MediaPlayerPaused, self.on_paused)
        events.event_attach(vlc.EventType.MediaPlayerStopped, self.on_paused) # Treat stopped as paused
        events.event_attach(vlc.EventType.MediaPlayerTimeChanged, self.on_time_changed)
        events.event_attach(vlc.EventType.MediaPlayerLengthChanged, self.on_time_changed) # Update on length change too
        events.event_attach(vlc.EventType.MediaPlayerEndReached, self.on_end_reached)

    def _load_track(self):
        """Loads the current track from the playlist into the player."""
        if not self.playlist or not (0 <= self.current_track_index < len(self.playlist)):
            return

        path = self.playlist[self.current_track_index]
        media = self.instance.media_new(path)
        self.player.set_media(media)

        # Re-attach event for the new media object to get its metadata
        media_events = media.event_manager()
        media_events.event_attach(vlc.EventType.MediaParsedChanged, self.on_media_parsed)

    def on_end_reached(self, event):
        """Called when a track finishes. Plays the next one automatically."""
        self.end_reached.emit()

    def on_media_parsed(self, event, retrying=False):
        """
        Called when media is parsed. This is the reliable point to fetch metadata.
        """
        media = self.player.get_media()
        if not media: return

        # --- Album Art ---
        artwork_url = get_album_art(self.playlist[self.current_track_index])
        if not artwork_url:
            artwork_url = media.get_meta(vlc.Meta.ArtworkURL)
        self.album_art_changed.emit(artwork_url)


        # --- Track Info ---
        title = media.get_meta(vlc.Meta.Title) or os.path.basename(self.playlist[self.current_track_index])
        artist = media.get_meta(vlc.Meta.Artist)
        self.track_info_changed.emit(title, artist)

    def on_playing(self, event):
        self.state_changed.emit(True)

    def on_paused(self, event):
        self.state_changed.emit(False)

    def on_time_changed(self, event):
        current_time = self.player.get_time()
        duration = self.player.get_length()
        if duration > 0: # Avoid division by zero
            self.position_changed.emit(current_time, duration)

    def play_pause(self):
        if self.player.is_playing():
            self.player.pause()
        else:
            self.player.play()

    def next(self):
        """Plays the next track in the playlist."""
        if not self.playlist: return
        self.player.stop()
        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        self._load_track()
        self.player.play()

    def previous(self):
        """Plays the previous track in the playlist."""
        if not self.playlist: return
        self.player.stop()
        self.current_track_index = (self.current_track_index - 1 + len(self.playlist)) % len(self.playlist)
        self._load_track()
        self.player.play()

    def is_playing(self):
        return self.player.is_playing()

    def seek(self, position):
        if self.player.is_seekable():
            self.player.set_position(position)

    def set_volume(self, volume):
        """Sets the player volume (0-100)."""
        self.player.audio_set_volume(volume)

    def set_mute(self, mute_state):
        """Sets the audio mute state and updates the UI via callback."""
        self._is_muted = mute_state
        self.player.audio_set_mute(self._is_muted)
        self.mute_changed.emit(self._is_muted)

    def toggle_mute(self):
        """Toggles the current mute state."""
        self.set_mute(not self._is_muted)
