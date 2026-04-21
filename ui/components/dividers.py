from PyQt5.QtWidgets import QFrame, QWidget
from PyQt5.QtCore import Qt
from themes import ThemeManager


class Divider(QFrame):
    def __init__(self, orientation: Qt.Orientation = Qt.Horizontal, parent: QWidget = None):
        super().__init__(parent)
        self.theme_manager = ThemeManager()
        self.setFrameShape(QFrame.HLine if orientation == Qt.Horizontal else QFrame.VLine)
        self.setFrameShadow(QFrame.Plain)
        self._setup_style()
        self.theme_manager.theme_changed.connect(self._setup_style)

    def _setup_style(self):
        colors = self.theme_manager.get_colors()
        self.setStyleSheet(f"color: {colors['border']};")
