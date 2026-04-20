from enum import Enum
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
from themes import ThemeManager


class ButtonVariant(Enum):
    DEFAULT = "default"
    PRIMARY = "primary"
    DANGER = "danger"
    SUCCESS = "success"
    OUTLINE = "outline"


class StyledButton(QPushButton):
    def __init__(self, text: str = "", parent: QWidget = None, variant: ButtonVariant = ButtonVariant.DEFAULT):
        super().__init__(text, parent)
        self.theme_manager = ThemeManager()
        self.variant = variant
        self._setup_style()
        self.theme_manager.theme_changed.connect(self._setup_style)
        
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumHeight(44)
    
    def _setup_style(self):
        colors = self.theme_manager.get_colors()
        
        base_style = f"""
        QPushButton {{
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: 600;
            border: none;
        }}
        """
        
        if self.variant == ButtonVariant.DEFAULT:
            style = base_style + f"""
            QPushButton {{
                background-color: {colors["card_background"]};
                color: {colors["text"]};
                border: 1px solid {colors["border"]};
            }}
            QPushButton:hover {{
                background-color: {colors["border"]};
                border-color: {colors["text_secondary"]};
            }}
            QPushButton:pressed {{
                background-color: {colors["border"]};
            }}
            """
        elif self.variant == ButtonVariant.PRIMARY:
            style = base_style + f"""
            QPushButton {{
                background-color: {colors["focus"]};
                color: #FFFFFF;
            }}
            QPushButton:hover {{
                background-color: {self._adjust_color(colors["focus"], -20)};
            }}
            QPushButton:pressed {{
                background-color: {self._adjust_color(colors["focus"], -30)};
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
            """
        elif self.variant == ButtonVariant.OUTLINE:
            style = base_style + f"""
            QPushButton {{
                background-color: transparent;
                color: {colors["text"]};
                border: 2px solid {colors["border"]};
            }}
            QPushButton:hover {{
                background-color: {colors["card_background"]};
                border-color: {colors["text_secondary"]};
            }}
            QPushButton:pressed {{
                background-color: {colors["border"]};
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


class IconButton(QPushButton):
    def __init__(self, icon: str = "", parent: QWidget = None):
        super().__init__(icon, parent)
        self.theme_manager = ThemeManager()
        self._setup_style()
        self.theme_manager.theme_changed.connect(self._setup_style)
        
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedSize(50, 50)
    
    def _setup_style(self):
        colors = self.theme_manager.get_colors()
        
        style = f"""
        QPushButton {{
            background-color: {colors["card_background"]};
            color: {colors["text"]};
            border: 1px solid {colors["border"]};
            border-radius: 12px;
            font-size: 20px;
        }}
        QPushButton:hover {{
            background-color: {colors["border"]};
            border-color: {colors["text_secondary"]};
        }}
        QPushButton:pressed {{
            background-color: {colors["border"]};
        }}
        QPushButton:checked {{
            background-color: {colors["focus"]};
            color: #FFFFFF;
            border: 1px solid {colors["focus"]};
        }}
        """
        
        self.setStyleSheet(style)
