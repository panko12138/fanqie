from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt
from themes import ThemeManager, Radius, Shadows


class StyledCard(QFrame):
    def __init__(self, parent: QWidget = None, elevation: int = 1):
        super().__init__(parent)
        self.theme_manager = ThemeManager()
        self.elevation = elevation
        self._setup_ui()
        self.theme_manager.theme_changed.connect(self._setup_style)

    def _setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)
        self._setup_style()

    def _setup_style(self):
        colors = self.theme_manager.get_colors()
        is_dark = self.theme_manager.is_dark_theme()

        if is_dark:
            border = "1px solid " + colors["border"]
        else:
            border = "none"

        self.setStyleSheet(
            "StyledCard { background-color: " + colors["surface"] + "; border: " + border + "; border-radius: " + str(Radius.LG) + "px; }"
        )


class HoverCard(StyledCard):
    def __init__(self, parent: QWidget = None, elevation: int = 1):
        super().__init__(parent, elevation)
        self.setMouseTracking(True)
        self._is_hovered = False

    def enterEvent(self, event):
        self._is_hovered = True
        self._update_hover_style()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._is_hovered = False
        self._setup_style()
        super().leaveEvent(event)

    def _update_hover_style(self):
        colors = self.theme_manager.get_colors()
        is_dark = self.theme_manager.is_dark_theme()

        if is_dark:
            border = "1px solid " + colors["text_tertiary"]
        else:
            border = "none"

        self.setStyleSheet(
            "HoverCard { background-color: " + colors["surface_elevated"] + "; border: " + border + "; border-radius: " + str(Radius.LG) + "px; }"
        )


class StatCard(QFrame):
    def __init__(self, title: str, value: str, subtitle: str = "", parent=None):
        super().__init__(parent)
        self.theme_manager = ThemeManager()
        self.title_text = title
        self.value_text = value
        self.subtitle_text = subtitle
        self.value_label = None
        self.title_label = None
        self.subtitle_label = None
        self._setup_ui()
        self.theme_manager.theme_changed.connect(self._update_styles)

    def _setup_ui(self):
        from PyQt5.QtWidgets import QLabel
        from PyQt5.QtGui import QFont

        colors = self.theme_manager.get_colors()
        is_dark = self.theme_manager.is_dark_theme()

        if is_dark:
            border = "1px solid " + colors["border"]
        else:
            border = "none"

        self.setStyleSheet(
            "StatCard { background-color: " + colors["surface"] + "; border: " + border + "; border-radius: " + str(Radius.LG) + "px; }"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        self.title_label = QLabel(self.title_text.upper())
        self.title_label.setStyleSheet(
            "color: " + colors["text_secondary"] + "; font-size: 11px; font-weight: 500; letter-spacing: 1px;"
        )
        layout.addWidget(self.title_label)

        self.value_label = QLabel(self.value_text)
        value_font = QFont()
        value_font.setPointSize(26)
        value_font.setBold(True)
        self.value_label.setFont(value_font)
        self.value_label.setStyleSheet("color: " + colors["text_primary"] + ";")
        layout.addWidget(self.value_label)

        if self.subtitle_text:
            self.subtitle_label = QLabel(self.subtitle_text)
            self.subtitle_label.setStyleSheet(
                "color: " + colors["text_tertiary"] + "; font-size: 12px;"
            )
            layout.addWidget(self.subtitle_label)

        self.setMinimumHeight(140)

    def _update_styles(self):
        colors = self.theme_manager.get_colors()
        is_dark = self.theme_manager.is_dark_theme()

        if is_dark:
            border = "1px solid " + colors["border"]
        else:
            border = "none"

        self.setStyleSheet(
            "StatCard { background-color: " + colors["surface"] + "; border: " + border + "; border-radius: " + str(Radius.LG) + "px; }"
        )

        if self.title_label:
            self.title_label.setStyleSheet(
                "color: " + colors["text_secondary"] + "; font-size: 11px; font-weight: 500; letter-spacing: 1px;"
            )
        if self.value_label:
            self.value_label.setStyleSheet("color: " + colors["text_primary"] + ";")
        if self.subtitle_label:
            self.subtitle_label.setStyleSheet(
                "color: " + colors["text_tertiary"] + "; font-size: 12px;"
            )
