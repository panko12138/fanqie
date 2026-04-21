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
    DARK: dict[str, str] = {
        "primary": "#E85D04",
        "primary_hover": "#D14903",
        "primary_pressed": "#B83D02",
        "focus": "#E85D04",
        "short_break": "#2D6A4F",
        "long_break": "#4361EE",
        "danger": "#DC2626",
        "success": "#059669",
        "info": "#0891B2",
        "background": "#121212",
        "surface": "#1E1E1E",
        "surface_elevated": "#252525",
        "border": "#2D2D2D",
        "text_primary": "#E8E8E8",
        "text_secondary": "#A1A1AA",
        "text_tertiary": "#71717A",
        "text_inverse": "#1A1A1A",
        "shadow_light": "0 1px 3px rgba(255,255,255,0.06)",
        "shadow_medium": "0 4px 12px rgba(255,255,255,0.08)",
        "shadow_heavy": "0 8px 24px rgba(255,255,255,0.10)",
    }

    LIGHT: dict[str, str] = {
        "primary": "#E85D04",
        "primary_hover": "#D14903",
        "primary_pressed": "#B83D02",
        "focus": "#E85D04",
        "short_break": "#2D6A4F",
        "long_break": "#4361EE",
        "danger": "#DC2626",
        "success": "#059669",
        "info": "#0891B2",
        "background": "#FAFAF8",
        "surface": "#FFFFFF",
        "surface_elevated": "#FFFBF7",
        "border": "#E8E5E0",
        "text_primary": "#1A1A1A",
        "text_secondary": "#6B7280",
        "text_tertiary": "#9CA3AF",
        "text_inverse": "#FFFFFF",
        "shadow_light": "0 1px 3px rgba(0,0,0,0.06)",
        "shadow_medium": "0 4px 12px rgba(0,0,0,0.08)",
        "shadow_heavy": "0 8px 24px rgba(0,0,0,0.10)",
    }


class Typography:
    FONT_FAMILY = '"SF Pro Display", "Segoe UI", "Microsoft YaHei", "PingFang SC", "Hiragino Sans GB", sans-serif'
    FONT_FAMILY_MONO = '"SF Mono", "Consolas", "Microsoft YaHei", monospace'

    DISPLAY = {"size": "48px", "weight": "bold", "line_height": "1.1"}
    H1 = {"size": "28px", "weight": "bold", "line_height": "1.2"}
    H2 = {"size": "20px", "weight": "600", "line_height": "1.3"}
    H3 = {"size": "16px", "weight": "600", "line_height": "1.4"}
    BODY = {"size": "14px", "weight": "400", "line_height": "1.5"}
    CAPTION = {"size": "12px", "weight": "400", "line_height": "1.4"}
    OVERLINE = {"size": "11px", "weight": "500", "line_height": "1.2"}

    @classmethod
    def get_style(cls, level: str, color: str = None) -> str:
        token = getattr(cls, level.upper(), cls.BODY)
        style = f"font-size: {token['size']}; font-weight: {token['weight']}; line-height: {token['line_height']};"
        if color:
            style += f" color: {color};"
        return style


class Spacing:
    SPACE_1 = 4
    SPACE_2 = 8
    SPACE_3 = 12
    SPACE_4 = 16
    SPACE_5 = 20
    SPACE_6 = 24
    SPACE_8 = 32
    SPACE_10 = 40
    SPACE_12 = 48


class Shadows:
    @staticmethod
    def get_shadow(level: str, is_dark: bool) -> str:
        if is_dark:
            return Colors.DARK.get(f"shadow_{level}", "")
        return Colors.LIGHT.get(f"shadow_{level}", "")


class Radius:
    SM = 8
    MD = 12
    LG = 16
    XL = 20
    FULL = 9999


import threading


class ThemeManager(QObject):
    _instance = None
    _lock = threading.Lock()
    theme_changed = pyqtSignal(ThemeType)

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
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
                        self.current_theme = ThemeType.LIGHT
                    else:
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
        palette.setColor(QPalette.WindowText, QColor(colors["text_primary"]))
        palette.setColor(QPalette.Base, QColor(colors["surface"]))
        palette.setColor(QPalette.AlternateBase, QColor(colors["background"]))
        palette.setColor(QPalette.ToolTipBase, QColor(colors["surface"]))
        palette.setColor(QPalette.ToolTipText, QColor(colors["text_primary"]))
        palette.setColor(QPalette.Text, QColor(colors["text_primary"]))
        palette.setColor(QPalette.Button, QColor(colors["surface"]))
        palette.setColor(QPalette.ButtonText, QColor(colors["text_primary"]))
        palette.setColor(QPalette.BrightText, QColor(colors["danger"]))
        palette.setColor(QPalette.Link, QColor(colors["info"]))
        palette.setColor(QPalette.Highlight, QColor(colors["primary"]))
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
            "surface": colors["surface"],
            "surface_elevated": colors["surface_elevated"],
            "text_primary": colors["text_primary"],
            "text_secondary": colors["text_secondary"],
            "text_tertiary": colors["text_tertiary"],
            "border": colors["border"],
            "danger": colors["danger"],
            "success": colors["success"],
            "primary": colors["primary"],
        }

    def get_stylesheet(self) -> str:
        colors = self.get_colors()
        is_dark = self.is_dark_theme()

        border_style = "1px solid " + colors["border"]
        if not is_dark:
            border_style = "none"

        ss = ""
        ss += "QWidget { background-color: " + colors["background"] + "; color: " + colors["text_primary"] + "; font-family: " + Typography.FONT_FAMILY + "; font-size: 14px; line-height: 1.5; }\n"
        ss += "QPushButton { background-color: " + colors["surface"] + "; color: " + colors["text_primary"] + "; border: " + border_style + "; border-radius: " + str(Radius.MD) + "px; padding: 10px 20px; font-size: 14px; font-weight: 600; min-height: 40px; }\n"
        ss += "QPushButton:hover { background-color: " + colors["surface_elevated"] + "; }\n"
        ss += "QPushButton:pressed { background-color: " + colors["border"] + "; }\n"
        ss += "QPushButton:checked { background-color: " + colors["primary"] + "; color: #FFFFFF; border: 1px solid " + colors["primary"] + "; }\n"
        ss += "QPushButton:disabled { background-color: " + colors["background"] + "; color: " + colors["text_tertiary"] + "; border: 1px solid " + colors["border"] + "; }\n"
        ss += "QLineEdit, QTextEdit, QPlainTextEdit { background-color: " + colors["surface"] + "; color: " + colors["text_primary"] + "; border: 2px solid " + colors["border"] + "; border-radius: " + str(Radius.MD) + "px; padding: 10px 14px; font-size: 14px; selection-background-color: " + colors["primary"] + "; selection-color: #FFFFFF; min-height: 44px; }\n"
        ss += "QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus { border: 2px solid " + colors["primary"] + "; }\n"
        ss += "QLineEdit::placeholder, QTextEdit::placeholder, QPlainTextEdit::placeholder { color: " + colors["text_tertiary"] + "; }\n"
        ss += "QComboBox { background-color: " + colors["surface"] + "; color: " + colors["text_primary"] + "; border: 2px solid " + colors["border"] + "; border-radius: " + str(Radius.MD) + "px; padding: 8px 14px; padding-right: 30px; font-size: 14px; min-height: 44px; }\n"
        ss += "QComboBox:hover { border-color: " + colors["text_secondary"] + "; }\n"
        ss += "QComboBox:focus { border-color: " + colors["primary"] + "; }\n"
        ss += "QComboBox::drop-down { border: none; width: 30px; }\n"
        ss += "QComboBox::down-arrow { image: none; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 6px solid " + colors["text_secondary"] + "; margin-right: 10px; }\n"
        ss += "QComboBox QAbstractItemView { background-color: " + colors["surface"] + "; color: " + colors["text_primary"] + "; border: 1px solid " + colors["border"] + "; border-radius: " + str(Radius.MD) + "px; selection-background-color: " + colors["primary"] + "; selection-color: #FFFFFF; padding: 6px; outline: none; }\n"
        ss += "QComboBox QAbstractItemView::item { padding: 8px 12px; border-radius: 4px; margin: 2px; }\n"
        ss += "QComboBox QAbstractItemView::item:hover { background-color: " + colors["border"] + "; }\n"
        ss += "QTabWidget::pane { border: none; background-color: transparent; }\n"
        ss += "QTabBar::tab { background-color: transparent; color: " + colors["text_secondary"] + "; padding: 12px 24px; border: none; border-bottom: 2px solid transparent; margin-right: 4px; font-size: 14px; font-weight: 500; }\n"
        ss += "QTabBar::tab:selected { color: " + colors["text_primary"] + "; border-bottom: 2px solid " + colors["primary"] + "; }\n"
        ss += "QTabBar::tab:hover:!selected { color: " + colors["text_primary"] + "; background-color: " + colors["surface"] + "; }\n"
        ss += "QScrollArea { border: none; background-color: transparent; }\n"
        ss += "QScrollBar:vertical { background-color: transparent; width: 8px; border-radius: 4px; margin: 0px; }\n"
        ss += "QScrollBar::handle:vertical { background-color: " + colors["border"] + "; border-radius: 4px; min-height: 30px; }\n"
        ss += "QScrollBar::handle:vertical:hover { background-color: " + colors["text_secondary"] + "; }\n"
        ss += "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }\n"
        ss += "QScrollBar:horizontal { background-color: transparent; height: 8px; border-radius: 4px; margin: 0px; }\n"
        ss += "QScrollBar::handle:horizontal { background-color: " + colors["border"] + "; border-radius: 4px; min-width: 30px; }\n"
        ss += "QScrollBar::handle:horizontal:hover { background-color: " + colors["text_secondary"] + "; }\n"
        ss += "QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }\n"
        ss += "QSpinBox { background-color: " + colors["surface"] + "; color: " + colors["text_primary"] + "; border: 2px solid " + colors["border"] + "; border-radius: " + str(Radius.MD) + "px; padding: 8px; font-size: 14px; min-height: 44px; }\n"
        ss += "QSpinBox:focus { border: 2px solid " + colors["primary"] + "; }\n"
        ss += "QSpinBox::up-button, QSpinBox::down-button { border: none; background-color: transparent; width: 24px; }\n"
        ss += "QSpinBox::up-arrow { border-left: 6px solid transparent; border-right: 6px solid transparent; border-bottom: 6px solid " + colors["text_secondary"] + "; }\n"
        ss += "QSpinBox::down-arrow { border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 6px solid " + colors["text_secondary"] + "; }\n"
        ss += "QCheckBox { color: " + colors["text_primary"] + "; spacing: 10px; font-size: 14px; }\n"
        ss += "QCheckBox::indicator { width: 20px; height: 20px; border: 2px solid " + colors["border"] + "; border-radius: 6px; background-color: " + colors["surface"] + "; }\n"
        ss += "QCheckBox::indicator:hover { border-color: " + colors["text_secondary"] + "; }\n"
        ss += "QCheckBox::indicator:checked { background-color: " + colors["primary"] + "; border-color: " + colors["primary"] + "; }\n"
        ss += "QListWidget { background-color: transparent; border: none; outline: none; }\n"
        ss += "QListWidget::item { background-color: transparent; padding: 4px; border-radius: 6px; margin: 2px 0px; }\n"
        ss += "QListWidget::item:hover { background-color: " + colors["surface"] + "; }\n"
        ss += "QListWidget::item:selected { background-color: " + colors["primary"] + "; color: #FFFFFF; }\n"
        ss += "QFrame[frameShape=\"4\"] { color: " + colors["border"] + "; }\n"
        ss += "QDialog { background-color: " + colors["background"] + "; border-radius: " + str(Radius.XL) + "px; }\n"
        ss += "QMessageBox { background-color: " + colors["background"] + "; }\n"
        ss += "QMessageBox QPushButton { min-width: 80px; }\n"
        return ss
