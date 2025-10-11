from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QSlider, QHBoxLayout, QLabel, QToolTip
from PySide6.QtGui import QCursor

class ProgressSlider(QWidget):
    """
    A widget containing a slider and labels to display and control track progress.
    """
    # Signal emitted when the user releases the slider handle
    seek_requested = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_seeking = False # Flag to prevent updates while user is dragging

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)

        self.current_time_label = QLabel("00:00")
        self.slider = QSlider(Qt.Horizontal)
        self.total_time_label = QLabel("00:00")

        # --- Styling ---
        self.current_time_label.setStyleSheet("color: #E0E0E0;")
        self.total_time_label.setStyleSheet("color: #E0E0E0;")
        self.slider.setStyleSheet("""
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
                background: #1DB954; /* Spotify green for played part */
                height: 4px;
                border-radius: 2px;
            }
        """)

        layout.addWidget(self.current_time_label)
        layout.addWidget(self.slider)
        layout.addWidget(self.total_time_label)

        self.slider.sliderMoved.connect(self.on_slider_moved)
        self.slider.sliderPressed.connect(self.on_slider_pressed)
        self.slider.sliderReleased.connect(self.on_slider_released)

    def on_slider_moved(self, value):
        """Shows a tooltip with the current time when the user drags the slider."""
        if self.slider.maximum() > 0:
            formatted_time = self._format_time(value)
            # Show tooltip slightly above and to the left of the cursor
            tooltip_pos = QCursor.pos()
            QToolTip.showText(tooltip_pos, formatted_time, self, self.slider.rect())

    def on_slider_pressed(self):
        self._is_seeking = True

    def on_slider_released(self):
        self._is_seeking = False
        QToolTip.hideText() # Ensure the tooltip is hidden on release
        if self.slider.maximum() > 0:
            position = self.slider.value() / self.slider.maximum()
            self.seek_requested.emit(position)

    def _format_time(self, ms):
        seconds = int((ms / 1000) % 60)
        minutes = int((ms / (1000 * 60)) % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def update_progress(self, time_ms, duration_ms):
        # Only update the slider if the user is not currently dragging it
        if not self._is_seeking:
            self.slider.setRange(0, duration_ms)
            self.slider.setValue(time_ms)
            self.current_time_label.setText(self._format_time(time_ms))
            self.total_time_label.setText(self._format_time(duration_ms))