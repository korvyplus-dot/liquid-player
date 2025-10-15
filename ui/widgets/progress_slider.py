from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QSlider, QHBoxLayout, QVBoxLayout, QLabel, QToolTip
from PySide6.QtGui import QCursor, QColor

class ProgressSlider(QWidget):
    """
    A widget containing a slider and labels to display and control track progress.
    """
    seek_requested = Signal(float)

    def __init__(self, main_window_color: QColor, parent=None):
        super().__init__(parent)
        self._is_seeking = False
        self._main_window_color = main_window_color
        self._elapsed_color = QColor("#A8E6CF")  # Gentle green

        # --- Layout ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        labels_layout = QHBoxLayout()
        labels_layout.setContentsMargins(4, 0, 4, 0)

        self.current_time_label = QLabel("00:00")
        self.total_time_label = QLabel("00:00")
        
        labels_layout.addWidget(self.current_time_label)
        labels_layout.addStretch()
        labels_layout.addWidget(self.total_time_label)

        self.slider = QSlider(Qt.Horizontal)

        main_layout.addLayout(labels_layout)
        main_layout.addWidget(self.slider)

        self.update_stylesheet()

        # --- Connections ---
        self.slider.sliderMoved.connect(self.on_slider_moved)
        self.slider.sliderPressed.connect(self.on_slider_pressed)
        self.slider.sliderReleased.connect(self.on_slider_released)

    def set_elapsed_color(self, color: QColor):
        self._elapsed_color = color
        self.update_stylesheet()

    def set_main_window_color(self, color: QColor):
        self._main_window_color = color
        self.update_stylesheet()

    def update_stylesheet(self):
        main_window_color_hex = self._main_window_color.name()
        
        # Invert the main window color for the outer handle
        inverted_color = QColor(
            255 - self._main_window_color.red(),
            255 - self._main_window_color.green(),
            255 - self._main_window_color.blue()
        )
        inverted_color_hex = inverted_color.name()

        self.slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 4px;
                background: {main_window_color_hex};
                margin: 2px 0;
                border-radius: 2px;
            }}
            QSlider::sub-page:horizontal {{
                background: {self._elapsed_color.name()};
                height: 4px;
                border-radius: 2px;
                margin: 2px 0;
            }}
            QSlider::handle:horizontal {{
                background: {main_window_color_hex};
                border: 1px solid {inverted_color_hex};
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }}
        """)
        self.current_time_label.setStyleSheet(f"color: {inverted_color.name()};")
        self.total_time_label.setStyleSheet(f"color: {inverted_color.name()};")
        
        tooltip_bg_color = self._elapsed_color.darker(150)
        self.setStyleSheet(f"""
            QToolTip {{
                color: #ffffff;
                background-color: {tooltip_bg_color.name()};
                border: 1px solid white;
                border-radius: 5px;
                padding: 5px;
            }}
        """)

    def on_slider_moved(self, value):
        if self.slider.maximum() > 0:
            formatted_time = self._format_time(value)
            tooltip_pos = QCursor.pos()
            QToolTip.showText(tooltip_pos, formatted_time, self, self.slider.rect())

    def on_slider_pressed(self):
        self._is_seeking = True

    def on_slider_released(self):
        self._is_seeking = False
        QToolTip.hideText()
        if self.slider.maximum() > 0:
            position = self.slider.value() / self.slider.maximum()
            self.seek_requested.emit(position)

    def _format_time(self, ms):
        seconds = int((ms / 1000) % 60)
        minutes = int((ms / (1000 * 60)) % 60)
        return f"{{minutes:02d}}:{{seconds:02d}}"

    def update_progress(self, time_ms, duration_ms):
        if not self._is_seeking:
            self.slider.setRange(0, duration_ms)
            self.slider.setValue(time_ms)
            self.current_time_label.setText(self._format_time(time_ms))
            self.total_time_label.setText(self._format_time(duration_ms))