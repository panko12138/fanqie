from enum import Enum
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication
from utils.logger import get_logger

logger = get_logger(__name__)


class ThemeType(Enum):
    LIGHT = "light"
    DARK = "dark"


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

        palette = QPalette()

        if self.current_theme == ThemeType.DARK:
            palette.setColor(QPalette.Window, QColor(26, 26, 46))
            palette.setColor(QPalette.WindowText, QColor(232, 232, 232))
            palette.setColor(QPalette.Base, QColor(22, 33, 62))
            palette.setColor(QPalette.AlternateBase, QColor(26, 26, 46))
            palette.setColor(QPalette.ToolTipBase, QColor(26, 26, 46))
            palette.setColor(QPalette.ToolTipText, QColor(232, 232, 232))
            palette.setColor(QPalette.Text, QColor(232, 232, 232))
            palette.setColor(QPalette.Button, QColor(22, 33, 62))
            palette.setColor(QPalette.ButtonText, QColor(232, 232, 232))
            palette.setColor(QPalette.BrightText, QColor(231, 76, 60))
            palette.setColor(QPalette.Link, QColor(52, 152, 219))
            palette.setColor(QPalette.Highlight, QColor(52, 152, 219))
            palette.setColor(QPalette.HighlightedText, QColor(232, 232, 232))
        else:
            palette.setColor(QPalette.Window, QColor(250, 250, 250))
            palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
            palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
            palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
            palette.setColor(QPalette.Text, QColor(0, 0, 0))
            palette.setColor(QPalette.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
            palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.Link, QColor(0, 0, 255))
            palette.setColor(QPalette.Highlight, QColor(46, 204, 113))
            palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

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

    def get_state_colors(self) -> dict:
        if self.current_theme == ThemeType.DARK:
            return {
                "focus": "#E74C3C",
                "short_break": "#2ECC71",
                "long_break": "#3498DB",
                "background": "#1A1A2E",
                "card_background": "#16213E",
                "text": "#E8E8E8",
                "text_secondary": "#A0A0A0",
            }
        else:
            return {
                "focus": "#E74C3C",
                "short_break": "#2ECC71",
                "long_break": "#3498DB",
                "background": "#FAFAFA",
                "card_background": "#FFFFFF",
                "text": "#000000",
                "text_secondary": "#666666",
            }
