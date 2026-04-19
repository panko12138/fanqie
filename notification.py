from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from utils.logger import get_logger
from utils.helpers import get_resources_path
import os

logger = get_logger(__name__)


class NotificationManager(QObject):
    def __init__(self):
        super().__init__()
        self.sound_enabled = True
        self.notification_enabled = True
        self._load_settings()

    def _load_settings(self):
        try:
            from database import get_db_manager
            from models import Setting
            db_manager = get_db_manager()
            with db_manager.session() as session:
                sound_setting = session.query(Setting).filter_by(key="sound_enabled").first()
                notification_setting = session.query(Setting).filter_by(key="notification_enabled").first()
                if sound_setting:
                    self.sound_enabled = sound_setting.value.lower() == "true"
                if notification_setting:
                    self.notification_enabled = notification_setting.value.lower() == "true"
        except Exception as e:
            logger.warning(f"加载通知设置失败: {e}")

    def play_pomodoro_complete_sound(self):
        if self.sound_enabled:
            sound_path = os.path.join(get_resources_path(), "sounds", "complete.wav")
            if os.path.exists(sound_path):
                QSound.play(sound_path)
                logger.info("播放完成提示音")

    def play_break_complete_sound(self):
        if self.sound_enabled:
            sound_path = os.path.join(get_resources_path(), "sounds", "break_complete.wav")
            if os.path.exists(sound_path):
                QSound.play(sound_path)
                logger.info("播放休息结束提示音")

    def show_pomodoro_complete_notification(self):
        if self.notification_enabled:
            QMessageBox.information(
                None,
                "番茄完成！",
                "太棒了！你完成了一个番茄！\n现在休息一下吧。",
                QMessageBox.Ok
            )
            logger.info("显示番茄完成通知")

    def show_break_complete_notification(self):
        if self.notification_enabled:
            QMessageBox.information(
                None,
                "休息结束！",
                "休息时间到！\n准备开始下一个番茄吧！",
                QMessageBox.Ok
            )
            logger.info("显示休息结束通知")

    def get_break_messages(self) -> list:
        return [
            "站起来活动一下吧！",
            "闭眼休息 30 秒，让眼睛放松一下。",
            "喝杯水，保持水分充足。",
            "做做拉伸运动，缓解颈椎疲劳。",
            "看看窗外，让眼睛休息一下。",
        ]

    def update_settings(self):
        self._load_settings()
