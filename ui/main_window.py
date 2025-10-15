import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QPoint, QTimer, Property, QPropertyAnimation
from PySide6.QtGui import QColor
import ctypes
from ctypes import wintypes
from ui.widgets.album_art_widget import AlbumArtWidget
from ui.widgets.progress_slider import ProgressSlider

# Constants for Acrylic effect
WCA_ACCENT_POLICY = 19
ACCENT_ENABLE_ACRYLICBLURBEHIND = 4

class ACCENT_POLICY(ctypes.Structure):
    _fields_ = [
        ("AccentState", ctypes.c_uint),
        ("AccentFlags", ctypes.c_uint),
        ("GradientColor", ctypes.c_uint),
        ("AnimationId", ctypes.c_uint),
    ]

class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [
        ("Attribute", ctypes.c_int),
        ("Data", ctypes.POINTER(ACCENT_POLICY)),
        ("SizeOfData", ctypes.c_size_t),
    ]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.width = 212
        self.height = 252
        
        self.resize(self.width, self.height)

        self.central_widget = QWidget()
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(4, 8, 4, 4)

        self.album_art = AlbumArtWidget()
        self.album_art.setFixedSize(200, 200)
        self.main_layout.addWidget(self.album_art, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.main_layout.addSpacing(4)

        self._tint_color = QColor(0,0,0,0)

        self.progress_slider = ProgressSlider(self._tint_color)
        self.progress_slider.setFixedWidth(200)
        self.main_layout.addWidget(self.progress_slider, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.main_layout.addStretch()

        self.dragging = False
        self.offset = QPoint()

        # Set default tint color to white
        default_color = QColor(255, 255, 255, 30)
        self.set_tint_color(default_color)

    def get_tint_color(self):
        return self._tint_color

    def set_tint_color(self, color: QColor):
        '''Sets the tint color for the acrylic effect.'''
        self._tint_color = color
        user32 = ctypes.windll.user32
        set_window_composition_attribute = user32.SetWindowCompositionAttribute

        accent = ACCENT_POLICY()
        accent.AccentState = ACCENT_ENABLE_ACRYLICBLURBEHIND
        
        gradient_color = (color.alpha() << 24) | (color.blue() << 16) | (color.green() << 8) | color.red()
        accent.GradientColor = gradient_color

        data = WINDOWCOMPOSITIONATTRIBDATA()
        data.Attribute = WCA_ACCENT_POLICY
        data.SizeOfData = ctypes.sizeof(accent)
        data.Data = ctypes.cast(ctypes.pointer(accent), ctypes.POINTER(ACCENT_POLICY))

        set_window_composition_attribute(int(self.winId()), ctypes.pointer(data))
        
        border_color = color.lighter(150)
        self.central_widget.setStyleSheet(f'''
            #central_widget {{
                background-color: transparent;
                border: 2px solid {border_color.name()};
                border-radius: 10px;
            }}
        ''')
        self.progress_slider.set_main_window_color(color)

    tint_color = Property(QColor, get_tint_color, set_tint_color)

    def start_color_animation(self, color: QColor):
        self.anim = QPropertyAnimation(self, b"tint_color")
        self.anim.setEndValue(color)
        self.anim.setDuration(1000) # 1000ms for a smooth animation
        self.anim.start()

    def mousePressEvent(self, event):
        self.dragging = True
        self.offset = event.globalPosition().toPoint() - self.pos()
        event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False
        event.accept()

def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    run()
