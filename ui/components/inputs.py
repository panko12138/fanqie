from PyQt5.QtWidgets import QLineEdit, QComboBox, QWidget
from PyQt5.QtCore import Qt
from themes import ThemeManager


class StyledLineEdit(QLineEdit):
    def __init__(self, parent: QWidget = None, placeholder: str = ""):
        super().__init__(parent)
        self.theme_manager = ThemeManager()
        self._setup_style()
        self.theme_manager.theme_changed.connect(self._setup_style)
        
        if placeholder:
            self.setPlaceholderText(placeholder)
    
    def _setup_style(self):
        colors = self.theme_manager.get_colors()
        
        style = f"""
        QLineEdit {{
            background-color: {colors["card_background"]};
            color: {colors["text"]};
            border: 2px solid {colors["border"]};
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 14px;
            selection-background-color: {colors["focus"]};
            selection-color: #FFFFFF;
        }}
        QLineEdit:focus {{
            border: 2px solid {colors["focus"]};
        }}
        QLineEdit::placeholder {{
            color: {colors["text_muted"]};
        }}
        """
        
        self.setStyleSheet(style)


class StyledComboBox(QComboBox):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.theme_manager = ThemeManager()
        self._setup_style()
        self.theme_manager.theme_changed.connect(self._setup_style)
    
    def _setup_style(self):
        colors = self.theme_manager.get_colors()
        
        style = f"""
        QComboBox {{
            background-color: {colors["card_background"]};
            color: {colors["text"]};
            border: 2px solid {colors["border"]};
            border-radius: 8px;
            padding: 8px 14px;
            padding-right: 30px;
            font-size: 14px;
            min-height: 24px;
        }}
        QComboBox:hover {{
            border-color: {colors["text_secondary"]};
        }}
        QComboBox:focus {{
            border-color: {colors["focus"]};
        }}
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        QComboBox::down-arrow {{
            image: none;
            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-top: 6px solid {colors["text_secondary"]};
            margin-right: 10px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {colors["card_background"]};
            color: {colors["text"]};
            border: 1px solid {colors["border"]};
            border-radius: 8px;
            selection-background-color: {colors["focus"]};
            selection-color: #FFFFFF;
            padding: 6px;
            outline: none;
        }}
        QComboBox QAbstractItemView::item {{
            padding: 8px 12px;
            border-radius: 4px;
            margin: 2px;
        }}
        QComboBox QAbstractItemView::item:hover {{
            background-color: {colors["border"]};
        }}
        """
        
        self.setStyleSheet(style)
