from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt
from themes import ThemeManager, Radius


class Badge(QLabel):
    def __init__(self, text: str = "", parent: QWidget = None, variant: str = "default"):
        super().__init__(text, parent)
        self.theme_manager = ThemeManager()
        self.variant = variant
        self.setAlignment(Qt.AlignCenter)
        self.setContentsMargins(8, 4, 8, 4)
        self._setup_style()
        self.theme_manager.theme_changed.connect(self._setup_style)

    def _setup_style(self):
        colors = self.theme_manager.get_colors()

        if self.variant == "primary":
            bg = colors["primary"]
            fg = "#FFFFFF"
        elif self.variant == "success":
            bg = colors["success"]
            fg = "#FFFFFF"
        elif self.variant == "danger":
            bg = colors["danger"]
            fg = "#FFFFFF"
        elif self.variant == "outline":
            bg = "transparent"
            fg = colors["text_secondary"]
            border = f"1px solid {colors['border']}"
        else:
            bg = colors["surface"]
            fg = colors["text_secondary"]
            border = f"1px solid {colors['border']}"

        if self.variant == "outline" or self.variant == "default":
            style = f"""
            QLabel {{
                background-color: {bg};
                color: {fg};
                border: {border};
                border-radius: {Radius.FULL}px;
                font-size: 11px;
                font-weight: 500;
                padding: 4px 10px;
            }}
            """
        else:
            style = f"""
            QLabel {{
                background-color: {bg};
                color: {fg};
                border: none;
                border-radius: {Radius.FULL}px;
                font-size: 11px;
                font-weight: 500;
                padding: 4px 10px;
            }}
            """

        self.setStyleSheet(style)
