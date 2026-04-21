from enum import Enum
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
from themes import ThemeManager, Radius


class ButtonVariant(Enum):
    DEFAULT = "default"
    PRIMARY = "primary"
    DANGER = "danger"
    SUCCESS = "success"
    OUTLINE = "outline"
    GHOST = "ghost"


class StyledButton(QPushButton):
    def __init__(self, text: str = "", parent: QWidget = None, variant: ButtonVariant = ButtonVariant.DEFAULT):
        super().__init__(text, parent)
        self.theme_manager = ThemeManager()
        self.variant = variant
        self._setup_style()
        self.theme_manager.theme_changed.connect(self._setup_style)

        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumHeight(40)

    def _setup_style(self):
        colors = self.theme_manager.get_colors()
        is_dark = self.theme_manager.is_dark_theme()

        base_style = f"""
        QPushButton {{
            border-radius: {Radius.MD}px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: 600;
            border: none;
            min-height: 40px;
        }}
        """

        if self.variant == ButtonVariant.DEFAULT:
            style = base_style + f"""
            QPushButton {{
                background-color: {colors["surface"]};
                color: {colors["text_primary"]};
                border: 1px solid {colors["border"]};
            }}
            QPushButton:hover {{
                background-color: {colors["surface_elevated"]};
                border-color: {colors["text_secondary"]};
            }}
            QPushButton:pressed {{
                background-color: {colors["border"]};
            }}
            QPushButton:focus {{
                outline: none;
                border: 2px solid {colors["primary"]};
            }}
            """
        elif self.variant == ButtonVariant.PRIMARY:
            style = base_style + f"""
            QPushButton {{
                background-color: {colors["primary"]};
                color: #FFFFFF;
            }}
            QPushButton:hover {{
                background-color: {colors["primary_hover"]};
            }}
            QPushButton:pressed {{
                background-color: {colors["primary_pressed"]};
            }}
            QPushButton:focus {{
                outline: none;
                border: 2px solid {colors["primary"]};
            }}
            QPushButton:disabled {{
                background-color: {colors["border"]};
                color: {colors["text_tertiary"]};
            }}
            """
        elif self.variant == ButtonVariant.DANGER:
            style = base_style + f"""
            QPushButton {{
                background-color: {colors["danger"]};
                color: #FFFFFF;
            }}
            QPushButton:hover {{
                background-color: {self._adjust_color(colors["danger"], -20)};
            }}
            QPushButton:pressed {{
                background-color: {self._adjust_color(colors["danger"], -30)};
            }}
            QPushButton:focus {{
                outline: none;
                border: 2px solid {colors["danger"]};
            }}
            """
        elif self.variant == ButtonVariant.SUCCESS:
            style = base_style + f"""
            QPushButton {{
                background-color: {colors["success"]};
                color: #FFFFFF;
            }}
            QPushButton:hover {{
                background-color: {self._adjust_color(colors["success"], -20)};
            }}
            QPushButton:pressed {{
                background-color: {self._adjust_color(colors["success"], -30)};
            }}
            QPushButton:focus {{
                outline: none;
                border: 2px solid {colors["success"]};
            }}
            """
        elif self.variant == ButtonVariant.OUTLINE:
            style = base_style + f"""
            QPushButton {{
                background-color: transparent;
                color: {colors["text_primary"]};
                border: 2px solid {colors["border"]};
            }}
            QPushButton:hover {{
                background-color: {colors["surface"]};
                border-color: {colors["text_secondary"]};
            }}
            QPushButton:pressed {{
                background-color: {colors["border"]};
            }}
            QPushButton:focus {{
                outline: none;
                border: 2px solid {colors["primary"]};
            }}
            """
        elif self.variant == ButtonVariant.GHOST:
            style = base_style + f"""
            QPushButton {{
                background-color: transparent;
                color: {colors["text_secondary"]};
                border: none;
            }}
            QPushButton:hover {{
                background-color: {colors["surface"]};
                color: {colors["text_primary"]};
            }}
            QPushButton:pressed {{
                background-color: {colors["border"]};
            }}
            QPushButton:focus {{
                outline: none;
                border: 2px solid {colors["primary"]};
            }}
            """

        self.setStyleSheet(style)

    def _adjust_color(self, hex_color: str, percent: int) -> str:
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        r = max(0, min(255, r + percent))
        g = max(0, min(255, g + percent))
        b = max(0, min(255, b + percent))

        return f"#{r:02x}{g:02x}{b:02x}"


class PrimaryButton(StyledButton):
    def __init__(self, text: str = "", parent: QWidget = None):
        super().__init__(text, parent, variant=ButtonVariant.PRIMARY)


class DangerButton(StyledButton):
    def __init__(self, text: str = "", parent: QWidget = None):
        super().__init__(text, parent, variant=ButtonVariant.DANGER)


class SuccessButton(StyledButton):
    def __init__(self, text: str = "", parent: QWidget = None):
        super().__init__(text, parent, variant=ButtonVariant.SUCCESS)


class GhostButton(StyledButton):
    def __init__(self, text: str = "", parent: QWidget = None):
        super().__init__(text, parent, variant=ButtonVariant.GHOST)


class IconButton(QPushButton):
    def __init__(self, icon: str = "", text: str = "", parent: QWidget = None):
        super().__init__(parent)
        self._icon = icon
        self._text = text
        self.theme_manager = ThemeManager()
        self._setup_style()
        self.theme_manager.theme_changed.connect(self._setup_style)

        self.setCursor(QCursor(Qt.PointingHandCursor))
        if text:
            self.setFixedSize(88, 72)
        else:
            self.setFixedSize(50, 50)

    def _setup_style(self):
        colors = self.theme_manager.get_colors()

        if self._text:
            style = f"""
            QPushButton {{
                background-color: transparent;
                color: {colors["text_secondary"]};
                border: none;
                border-radius: {Radius.MD}px;
                font-size: 11px;
                font-weight: 500;
                padding: 4px;
            }}
            QPushButton:hover {{
                background-color: {colors["surface_elevated"]};
                color: {colors["text_primary"]};
            }}
            QPushButton:pressed {{
                background-color: {colors["border"]};
            }}
            QPushButton:checked {{
                background-color: {colors["surface"]};
                color: {colors["primary"]};
            }}
            """
        else:
            style = f"""
            QPushButton {{
                background-color: {colors["surface"]};
                color: {colors["text_primary"]};
                border: 1px solid {colors["border"]};
                border-radius: 12px;
                font-size: 20px;
            }}
            QPushButton:hover {{
                background-color: {colors["surface_elevated"]};
                border-color: {colors["text_secondary"]};
            }}
            QPushButton:pressed {{
                background-color: {colors["border"]};
            }}
            QPushButton:checked {{
                background-color: {colors["primary"]};
                color: #FFFFFF;
                border: 1px solid {colors["primary"]};
            }}
            """

        self.setStyleSheet(style)
        if self._text:
            self.setText(f"{self._icon}\n{self._text}")
        else:
            self.setText(self._icon)


class IconOnlyButton(QPushButton):
    def __init__(self, icon: str = "", parent: QWidget = None, size: int = 36):
        super().__init__(icon, parent)
        self.theme_manager = ThemeManager()
        self._size = size
        self._setup_style()
        self.theme_manager.theme_changed.connect(self._setup_style)

        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedSize(size, size)

    def _setup_style(self):
        colors = self.theme_manager.get_colors()

        style = f"""
        QPushButton {{
            background-color: transparent;
            color: {colors["text_secondary"]};
            border: none;
            border-radius: {Radius.SM}px;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {colors["surface"]};
            color: {colors["text_primary"]};
        }}
        QPushButton:pressed {{
            background-color: {colors["border"]};
        }}
        """

        self.setStyleSheet(style)
