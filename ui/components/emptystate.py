from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from themes import ThemeManager
from ui.components import PrimaryButton


class EmptyState(QWidget):
    def __init__(self, icon: str = "", title: str = "", subtitle: str = "", parent: QWidget = None):
        super().__init__(parent)
        self.theme_manager = ThemeManager()
        self._icon = icon
        self._title = title
        self._subtitle = subtitle
        self._setup_ui()
        self.theme_manager.theme_changed.connect(self._update_styles)

    def _setup_ui(self):
        colors = self.theme_manager.get_colors()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)

        if self._icon:
            self.icon_label = QLabel(self._icon)
            icon_font = QFont()
            icon_font.setPointSize(48)
            self.icon_label.setFont(icon_font)
            self.icon_label.setAlignment(Qt.AlignCenter)
            self.icon_label.setStyleSheet(f"color: {colors['text_tertiary']};")
            layout.addWidget(self.icon_label)

        if self._title:
            self.title_label = QLabel(self._title)
            title_font = QFont()
            title_font.setPointSize(16)
            title_font.setBold(True)
            self.title_label.setFont(title_font)
            self.title_label.setAlignment(Qt.AlignCenter)
            self.title_label.setStyleSheet(f"color: {colors['text_primary']};")
            layout.addWidget(self.title_label)

        if self._subtitle:
            self.subtitle_label = QLabel(self._subtitle)
            self.subtitle_label.setAlignment(Qt.AlignCenter)
            self.subtitle_label.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 14px;")
            layout.addWidget(self.subtitle_label)

        self.action_button = None

    def set_action(self, text: str, callback):
        if self.action_button is None:
            self.action_button = PrimaryButton(text)
            self.layout().addWidget(self.action_button)
        else:
            self.action_button.setText(text)
        self.action_button.clicked.connect(callback)

    def _update_styles(self):
        colors = self.theme_manager.get_colors()
        if hasattr(self, 'icon_label'):
            self.icon_label.setStyleSheet(f"color: {colors['text_tertiary']};")
        if hasattr(self, 'title_label'):
            self.title_label.setStyleSheet(f"color: {colors['text_primary']};")
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 14px;")
