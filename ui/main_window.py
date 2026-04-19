import sys
from datetime import datetime, date
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QStackedWidget, QSystemTrayIcon, QMenu, QAction, QApplication
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont

from timer import PomodoroTimer
from task_manager import TaskManager
from notification import NotificationManager
from themes import ThemeManager
from ui.timer_widget import TimerWidget
from ui.task_panel import TaskPanel
from ui.stats_panel import StatsPanel
from ui.settings_dialog import SettingsDialog
from database import init_database, test_connection
from models import Setting
from utils.logger import get_logger

logger = get_logger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.theme_manager = ThemeManager()
        self.timer = PomodoroTimer()
        self.task_manager = TaskManager()
        self.notification_manager = NotificationManager()
        self.current_task_id = None
        self.exam_date = None

        self.init_ui()
        self.init_connections()
        self.load_exam_date()
        self.init_tray()

        self.setWindowTitle("考研番茄钟")
        self.setMinimumSize(900, 700)
        self.theme_manager._apply_theme()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        nav_bar = self.create_nav_bar()
        main_layout.addWidget(nav_bar)

        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        top_bar = self.create_top_bar()
        content_layout.addWidget(top_bar)

        self.stacked_widget = QStackedWidget()
        self.timer_widget = TimerWidget()
        self.task_panel = TaskPanel()
        self.stats_panel = StatsPanel()

        self.stacked_widget.addWidget(self.timer_widget)
        self.stacked_widget.addWidget(self.task_panel)
        self.stacked_widget.addWidget(self.stats_panel)

        content_layout.addWidget(self.stacked_widget)

        main_layout.addWidget(content_area, 1)

    def create_nav_bar(self) -> QWidget:
        nav_bar = QWidget()
        nav_bar.setFixedWidth(70)
        nav_bar.setStyleSheet("background-color: #2C3E50;")

        layout = QVBoxLayout(nav_bar)
        layout.setContentsMargins(5, 20, 5, 20)
        layout.setSpacing(15)

        self.nav_timer_btn = QPushButton("⏱️")
        self.nav_timer_btn.setStyleSheet("background-color: #3498DB; color: white;")
        self.nav_timer_btn.setFixedHeight(60)
        self.nav_timer_btn.setCursor(Qt.PointingHandCursor)

        self.nav_task_btn = QPushButton("📋")
        self.nav_task_btn.setFixedHeight(60)
        self.nav_task_btn.setCursor(Qt.PointingHandCursor)

        self.nav_stats_btn = QPushButton("📊")
        self.nav_stats_btn.setFixedHeight(60)
        self.nav_stats_btn.setCursor(Qt.PointingHandCursor)

        self.nav_settings_btn = QPushButton("⚙️")
        self.nav_settings_btn.setFixedHeight(60)
        self.nav_settings_btn.setCursor(Qt.PointingHandCursor)

        layout.addWidget(self.nav_timer_btn)
        layout.addWidget(self.nav_task_btn)
        layout.addWidget(self.nav_stats_btn)
        layout.addStretch()
        layout.addWidget(self.nav_settings_btn)

        return nav_bar

    def create_top_bar(self) -> QWidget:
        top_bar = QWidget()
        top_bar.setFixedHeight(50)
        top_bar.setStyleSheet("background-color: #f0f0f0; border-bottom: 1px solid #ddd;")

        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(20, 0, 20, 0)

        self.exam_countdown_label = QLabel("设置考研日期")
        exam_font = QFont()
        exam_font.setPointSize(14)
        exam_font.setBold(True)
        self.exam_countdown_label.setFont(exam_font)
        layout.addWidget(self.exam_countdown_label)

        layout.addStretch()

        today_stat_label = QLabel("今日番茄: 0")
        today_stat_label.setStyleSheet("color: #666; font-size: 14px;")
        self.today_stat_label = today_stat_label
        layout.addWidget(today_stat_label)

        return top_bar

    def init_connections(self):
        self.nav_timer_btn.clicked.connect(lambda: self.switch_page(0))
        self.nav_task_btn.clicked.connect(lambda: self.switch_page(1))
        self.nav_stats_btn.clicked.connect(lambda: self.switch_page(2))
        self.nav_settings_btn.clicked.connect(self.open_settings)

        self.timer_widget.start_clicked.connect(self.timer.start)
        self.timer_widget.pause_clicked.connect(self.timer.pause)
        self.timer_widget.reset_clicked.connect(self.timer.reset)
        self.timer_widget.skip_clicked.connect(self.timer.skip)
        self.timer_widget.stop_clicked.connect(self.timer.stop)

        self.timer.timer_updated.connect(self.timer_widget.update_timer)
        self.timer.progress_updated.connect(self.timer_widget.update_progress)
        self.timer.state_changed.connect(self.timer_widget.update_state)
        self.timer.is_running_changed.connect(self.timer_widget.set_is_running)
        self.timer.pomodoro_completed.connect(self.on_pomodoro_completed)
        self.timer.session_saved.connect(self.on_session_saved)
        self.timer.achievement_unlocked.connect(self.on_achievement_unlocked)

        self.task_panel.task_selected.connect(self.on_task_selected)

        self.update_exam_countdown()
        self.exam_timer = QTimer()
        self.exam_timer.timeout.connect(self.update_exam_countdown)
        self.exam_timer.start(60000)

    def switch_page(self, index: int):
        self.stacked_widget.setCurrentIndex(index)

        self.nav_timer_btn.setStyleSheet("")
        self.nav_task_btn.setStyleSheet("")
        self.nav_stats_btn.setStyleSheet("")

        if index == 0:
            self.nav_timer_btn.setStyleSheet("background-color: #3498DB; color: white;")
        elif index == 1:
            self.nav_task_btn.setStyleSheet("background-color: #3498DB; color: white;")
        elif index == 2:
            self.nav_stats_btn.setStyleSheet("background-color: #3498DB; color: white;")

        if index == 2:
            self.stats_panel.refresh()

    def on_task_selected(self, task_id: int):
        self.current_task_id = task_id
        self.timer.set_current_task(task_id)

        task = self.task_manager.get_task(task_id)
        if task:
            self.timer_widget.set_current_task(task.name)

    def on_pomodoro_completed(self, count: int):
        self.timer_widget.update_pomodoro_count(count)
        self.notification_manager.play_pomodoro_complete_sound()
        self.update_today_stat()
        self.stats_panel.refresh()

    def on_achievement_unlocked(self, achievements):
        message = "恭喜解锁成就：\n"
        for ach in achievements:
            message += f"{ach['icon']} {ach['name']}\n"
        QMessageBox.information(self, "成就解锁", message)

    def on_session_saved(self, session):
        self.task_panel.refresh()

    def update_today_stat(self):
        from statistics import StatisticsManager
        stats = StatisticsManager()
        today_stats = stats.get_today_stats()
        self.today_stat_label.setText(f"今日番茄: {today_stats['total_pomodoros']}")

    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec_() == SettingsDialog.Accepted:
            self.notification_manager.update_settings()
            self.timer.update_settings()
            self.load_exam_date()

    def load_exam_date(self):
        try:
            from database import get_db_manager
            db_manager = get_db_manager()
            with db_manager.session() as session:
                setting = session.query(Setting).filter_by(key="exam_date").first()
                if setting and setting.value:
                    self.exam_date = date.fromisoformat(setting.value)
                else:
                    self.exam_date = None
        except Exception as e:
            logger.warning(f"加载考研日期失败: {e}")

    def update_exam_countdown(self):
        if self.exam_date:
            today = date.today()
            delta = self.exam_date - today
            if delta.days >= 0:
                self.exam_countdown_label.setText(f"距离考研还有 {delta.days} 天")
            else:
                self.exam_countdown_label.setText("考研已结束")
        else:
            self.exam_countdown_label.setText("设置考研日期")

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setToolTip("考研番茄钟")

        tray_menu = QMenu()

        show_action = QAction("显示", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        start_action = QAction("开始/暂停", self)
        start_action.triggered.connect(lambda: self.timer.start() if not self.timer.is_running() else self.timer.pause())
        tray_menu.addAction(start_action)

        quit_action = QAction("退出", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "考研番茄钟",
            "应用已最小化到托盘",
            QSystemTrayIcon.Information,
            2000
        )


def main():
    app = QApplication(sys.argv)

    logger.info("正在初始化数据库...")
    try:
        init_database()
        logger.info("数据库初始化成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        QMessageBox.critical(None, "错误", f"数据库初始化失败: {e}\n请检查MySQL配置！")
        return 1

    window = MainWindow()
    window.show()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
