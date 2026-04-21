from PyQt5.QtWidgets import QLineEdit, QComboBox, QWidget, QTextEdit, QSpinBox
from PyQt5.QtCore import Qt
from themes import ThemeManager, Radius


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
            background-color: {colors["surface"]};
            color: {colors["text_primary"]};
            border: 2px solid {colors["border"]};
            border-radius: {Radius.MD}px;
            padding: 10px 14px;
            font-size: 14px;
            selection-background-color: {colors["primary"]};
            selection-color: #FFFFFF;
            min-height: 44px;
        }}
        QLineEdit:focus {{
            border: 2px solid {colors["primary"]};
        }}
        QLineEdit::placeholder {{
            color: {colors["text_tertiary"]};
        }}
        """

        self.setStyleSheet(style)


class StyledTextEdit(QTextEdit):
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
        QTextEdit {{
            background-color: {colors["surface"]};
            color: {colors["text_primary"]};
            border: 2px solid {colors["border"]};
            border-radius: {Radius.MD}px;
            padding: 10px 14px;
            font-size: 14px;
            selection-background-color: {colors["primary"]};
            selection-color: #FFFFFF;
        }}
        QTextEdit:focus {{
            border: 2px solid {colors["primary"]};
        }}
        QTextEdit::placeholder {{
            color: {colors["text_tertiary"]};
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
            background-color: {colors["surface"]};
            color: {colors["text_primary"]};
            border: 2px solid {colors["border"]};
            border-radius: {Radius.MD}px;
            padding: 8px 14px;
            padding-right: 30px;
            font-size: 14px;
            min-height: 44px;
        }}
        QComboBox:hover {{
            border-color: {colors["text_secondary"]};
        }}
        QComboBox:focus {{
            border-color: {colors["primary"]};
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
            background-color: {colors["surface"]};
            color: {colors["text_primary"]};
            border: 1px solid {colors["border"]};
            border-radius: {Radius.MD}px;
            selection-background-color: {colors["primary"]};
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


class StyledSpinBox(QSpinBox):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.theme_manager = ThemeManager()
        self._setup_style()
        self.theme_manager.theme_changed.connect(self._setup_style)

    def _setup_style(self):
        colors = self.theme_manager.get_colors()

        style = f"""
        QSpinBox {{
            background-color: {colors["surface"]};
            color: {colors["text_primary"]};
            border: 2px solid {colors["border"]};
            border-radius: {Radius.MD}px;
            padding: 8px;
            font-size: 14px;
            min-height: 44px;
        }}
        QSpinBox:focus {{
            border: 2px solid {colors["primary"]};
        }}
        QSpinBox::up-button, QSpinBox::down-button {{
            border: none;
            background-color: transparent;
            width: 24px;
        }}
        QSpinBox::up-arrow {{
            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-bottom: 6px solid {colors["text_secondary"]};
        }}
        QSpinBox::down-arrow {{
            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-top: 6px solid {colors["text_secondary"]};
        }}
        """

        self.setStyleSheet(style)
