from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt
from themes import ThemeManager


class StyledCard(QFrame):
    def __init__(self, parent: QWidget = None, elevation: int = 1):
        super().__init__(parent)
        self.theme_manager = ThemeManager()
        self.elevation = elevation
        self._setup_ui()
        self.theme_manager.theme_changed.connect(self._setup_style)
    
    def _setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(12)
        self._setup_style()
    
    def _setup_style(self):
        colors = self.theme_manager.get_colors()
        
        shadow = "0 4px 6px -1px rgba(0,0,0,0.1)"
        if self.elevation >= 2:
            shadow = "0 10px 15px -3px rgba(0,0,0,0.1)"
        if self.elevation >= 3:
            shadow = "0 20px 25px -5px rgba(0,0,0,0.15)"
        
        style = f"""
        StyledCard {{
            background-color: {colors["card_background"]};
            border: 1px solid {colors["border"]};
            border-radius: 12px;
        }}
        """
        
        self.setStyleSheet(style)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
