from enum import Enum
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication
from utils.logger import get_logger

logger = get_logger(__name__)


class ThemeType(Enum):
    LIGHT = "light"
    DARK = "dark"


class Colors:
    DARK = {
        "background": "#0F172A",
        "card_background": "#1E293B",
        "border": "#334155",
        "text": "#F8FAFC",
        "text_secondary": "#94A3B8",
        "text_muted": "#64748B",
        "focus": "#F97316",
        "short_break": "#22C55E",
        "long_break": "#3B82F6",
        "danger": "#EF4444",
        "success": "#10B981",
        "info": "#06B6D4",
        "shadow_light": "rgba(0,0,0,0.05)",
        "shadow_medium": "rgba(0,0,0,0.1)",
        "shadow_heavy": "rgba(0,0,0,0.15)"
    }
    
    LIGHT = {
        "background": "#F8FAFC",
        "card_background": "#FFFFFF",
        "border": "#E2E8F0",
        "text": "#1E293B",
        "text_secondary": "#64748B",
        "text_muted": "#94A3B8",
        "focus": "#F97316",
        "short_break": "#22C55E",
        "long_break": "#3B82F6",
        "danger": "#EF4444",
        "success": "#10B981",
        "info": "#06B6D4",
        "shadow_light": "rgba(0,0,0,0.05)",
        "shadow_medium": "rgba(0,0,0,0.1)",
        "shadow_heavy": "rgba(0,0,0,0.1)"
    }


class ThemeManager(QObject):
    theme_changed = pyqtSignal(ThemeType)

    def __init__(self):
        super().__init__()
        self.current_theme = ThemeType.LIGHT
        self._load_settings()

    def _load_settings(self):
        try:
            from database import get_db_manager
            from models import Setting
            db_manager = get_db_manager()
            with db_manager.session() as session:
                setting = session.query(Setting).filter_by(key="theme").first()
                if setting:
                    if setting.value == "auto":
                        setting.value = "light"
                        session.commit()
                    self.current_theme = ThemeType(setting.value)
        except Exception as e:
            logger.warning(f"加载主题设置失败: {e}")

    def set_theme(self, theme: ThemeType):
        self.current_theme = theme
        self._apply_theme()
        self._save_theme()
        self.theme_changed.emit(theme)
        logger.info(f"切换主题: {theme.value}")

    def _apply_theme(self):
        app = QApplication.instance()
        if not app:
            return

        colors = self.get_colors()
        palette = QPalette()
        
        palette.setColor(QPalette.Window, QColor(colors["background"]))
        palette.setColor(QPalette.WindowText, QColor(colors["text"]))
        palette.setColor(QPalette.Base, QColor(colors["card_background"]))
        palette.setColor(QPalette.AlternateBase, QColor(colors["background"]))
        palette.setColor(QPalette.ToolTipBase, QColor(colors["card_background"]))
        palette.setColor(QPalette.ToolTipText, QColor(colors["text"]))
        palette.setColor(QPalette.Text, QColor(colors["text"]))
        palette.setColor(QPalette.Button, QColor(colors["card_background"]))
        palette.setColor(QPalette.ButtonText, QColor(colors["text"]))
        palette.setColor(QPalette.BrightText, QColor(colors["danger"]))
        palette.setColor(QPalette.Link, QColor(colors["info"]))
        palette.setColor(QPalette.Highlight, QColor(colors["focus"]))
        palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))

        app.setPalette(palette)

    def _save_theme(self):
        try:
            from database import get_db_manager
            from models import Setting
            db_manager = get_db_manager()
            with db_manager.session() as session:
                setting = session.query(Setting).filter_by(key="theme").first()
                if setting:
                    setting.value = self.current_theme.value
                else:
                    setting = Setting(key="theme", value=self.current_theme.value)
                    session.add(setting)
        except Exception as e:
            logger.error(f"保存主题设置失败: {e}")

    def get_theme(self) -> ThemeType:
        return self.current_theme

    def is_dark_theme(self) -> bool:
        return self.current_theme == ThemeType.DARK

    def get_colors(self) -> dict:
        return Colors.DARK if self.is_dark_theme() else Colors.LIGHT

    def get_state_colors(self) -> dict:
        colors = self.get_colors()
        return {
            "focus": colors["focus"],
            "short_break": colors["short_break"],
            "long_break": colors["long_break"],
            "background": colors["background"],
            "card_background": colors["card_background"],
            "text": colors["text"],
            "text_secondary": colors["text_secondary"],
            "text_muted": colors["text_muted"],
            "border": colors["border"],
            "danger": colors["danger"],
            "success": colors["success"]
        }

    def get_stylesheet(self) -> str:
        colors = self.get_colors()
        
        return f"""
        QWidget {{
            background-color: {colors["background"]};
            color: {colors["text"]};
            font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
        }}
        
        QPushButton {{
            background-color: {colors["card_background"]};
            color: {colors["text"]};
            border: 1px solid {colors["border"]};
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: 500;
        }}
        
        QPushButton:hover {{
            background-color: {colors["border"]};
            border: 1px solid {colors["text_secondary"]};
        }}
        
        QPushButton:pressed {{
            background-color: {colors["border"]};
        }}
        
        QPushButton:checked {{
            background-color: {colors["focus"]};
            color: #FFFFFF;
            border: 1px solid {colors["focus"]};
        }}
        
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {colors["card_background"]};
            color: {colors["text"]};
            border: 1px solid {colors["border"]};
            border-radius: 6px;
            padding: 8px;
            selection-background-color: {colors["focus"]};
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border: 2px solid {colors["focus"]};
        }}
        
        QComboBox {{
            background-color: {colors["card_background"]};
            color: {colors["text"]};
            border: 1px solid {colors["border"]};
            border-radius: 6px;
            padding: 6px 12px;
        }}
        
        QComboBox:hover {{
            border: 1px solid {colors["text_secondary"]};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {colors["text_secondary"]};
            margin-right: 8px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {colors["card_background"]};
            color: {colors["text"]};
            border: 1px solid {colors["border"]};
            selection-background-color: {colors["focus"]};
            selection-color: #FFFFFF;
            padding: 4px;
        }}
        
        QTabWidget::pane {{
            border: none;
            background-color: {colors["background"]};
        }}
        
        QTabBar::tab {{
            background-color: {colors["background"]};
            color: {colors["text_secondary"]};
            padding: 10px 20px;
            border: none;
            border-bottom: 2px solid transparent;
            margin-right: 4px;
            font-size: 14px;
            font-weight: 500;
        }}
        
        QTabBar::tab:selected {{
            color: {colors["text"]};
            border-bottom: 2px solid {colors["focus"]};
        }}
        
        QTabBar::tab:hover:!selected {{
            color: {colors["text"]};
            background-color: {colors["card_background"]};
        }}
        
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        
        QScrollBar:vertical {{
            background-color: transparent;
            width: 8px;
            border-radius: 4px;
            margin: 0px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {colors["border"]};
            border-radius: 4px;
            min-height: 30px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {colors["text_secondary"]};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            background-color: transparent;
            height: 8px;
            border-radius: 4px;
            margin: 0px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {colors["border"]};
            border-radius: 4px;
            min-width: 30px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {colors["text_secondary"]};
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        
        QSpinBox {{
            background-color: {colors["card_background"]};
            color: {colors["text"]};
            border: 1px solid {colors["border"]};
            border-radius: 6px;
            padding: 6px;
        }}
        
        QSpinBox:focus {{
            border: 2px solid {colors["focus"]};
        }}
        
        QSpinBox::up-button, QSpinBox::down-button {{
            border: none;
            background-color: transparent;
            width: 20px;
        }}
        
        QSpinBox::up-arrow {{
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-bottom: 5px solid {colors["text_secondary"]};
        }}
        
        QSpinBox::down-arrow {{
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {colors["text_secondary"]};
        }}
        
        QCheckBox {{
            color: {colors["text"]};
            spacing: 8px;
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {colors["border"]};
            border-radius: 4px;
            background-color: {colors["card_background"]};
        }}
        
        QCheckBox::indicator:hover {{
            border-color: {colors["text_secondary"]};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {colors["focus"]};
            border-color: {colors["focus"]};
        }}
        
        QListWidget {{
            background-color: {colors["background"]};
            border: none;
            outline: none;
        }}
        
        QListWidget::item {{
            background-color: transparent;
            padding: 4px;
            border-radius: 6px;
            margin: 2px 0px;
        }}
        
        QListWidget::item:hover {{
            background-color: {colors["card_background"]};
        }}
        
        QListWidget::item:selected {{
            background-color: {colors["focus"]};
            color: #FFFFFF;
        }}
        """
