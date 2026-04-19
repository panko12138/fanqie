from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QScrollArea,
    QFrame, QTabWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from statistics import StatisticsManager
from utils.logger import get_logger
from utils.helpers import format_duration

logger = get_logger(__name__)


class StatCard(QWidget):
    def __init__(self, title: str, value: str, subtitle: str = "", parent=None):
        super().__init__(parent)
        self.value_label = None
        self.init_ui(title, value, subtitle)

    def init_ui(self, title: str, value: str, subtitle: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: #666666; font-size: 12px;")
        layout.addWidget(title_label)

        self.value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(24)
        value_font.setBold(True)
        self.value_label.setFont(value_font)
        self.value_label.setStyleSheet("color: #333333;")
        layout.addWidget(self.value_label)

        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setStyleSheet("color: #888888; font-size: 11px;")
            layout.addWidget(subtitle_label)

        self.setStyleSheet("background-color: white; border-radius: 8px;")
        self.setMinimumHeight(120)


class StatsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stats_manager = StatisticsManager()
        self.init_ui()
        self.load_stats()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)

        today_title = QLabel("今日统计")
        today_title.setFont(QFont("Arial", 16, QFont.Bold))
        content_layout.addWidget(today_title)

        today_grid = QGridLayout()
        today_grid.setSpacing(10)
        content_layout.addLayout(today_grid)

        self.today_pomodoros_card = StatCard("完成番茄", "0")
        today_grid.addWidget(self.today_pomodoros_card, 0, 0)

        self.today_focus_card = StatCard("专注时间", "0分钟")
        today_grid.addWidget(self.today_focus_card, 0, 1)

        self.today_tasks_card = StatCard("完成任务", "0")
        today_grid.addWidget(self.today_tasks_card, 0, 2)

        self.today_goal_card = StatCard("每日目标", "未达成")
        today_grid.addWidget(self.today_goal_card, 0, 3)

        total_title = QLabel("总体统计")
        total_title.setFont(QFont("Arial", 16, QFont.Bold))
        content_layout.addWidget(total_title)

        total_grid = QGridLayout()
        total_grid.setSpacing(10)
        content_layout.addLayout(total_grid)

        self.total_pomodoros_card = StatCard("总番茄数", "0")
        total_grid.addWidget(self.total_pomodoros_card, 0, 0)

        self.total_focus_card = StatCard("总专注时间", "0小时")
        total_grid.addWidget(self.total_focus_card, 0, 1)

        self.total_tasks_card = StatCard("完成任务", "0")
        total_grid.addWidget(self.total_tasks_card, 0, 2)

        self.consecutive_days_card = StatCard("连续打卡", "0天")
        total_grid.addWidget(self.consecutive_days_card, 0, 3)

        achievements_title = QLabel("成就")
        achievements_title.setFont(QFont("Arial", 16, QFont.Bold))
        content_layout.addWidget(achievements_title)

        self.achievements_layout = QHBoxLayout()
        content_layout.addLayout(self.achievements_layout)

        content_layout.addStretch()

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def load_stats(self):
        today_stats = self.stats_manager.get_today_stats()
        total_stats = self.stats_manager.get_total_stats()

        self.today_pomodoros_card.value_label.setText(str(today_stats["total_pomodoros"]))
        self.today_focus_card.value_label.setText(format_duration(today_stats["total_focus_time"]))
        self.today_tasks_card.value_label.setText(str(today_stats["tasks_completed"]))
        goal_text = "已达成!" if today_stats["goal_achieved"] else f"目标: {today_stats['daily_goal']}"
        self.today_goal_card.value_label.setText(goal_text)
        if today_stats["goal_achieved"]:
            self.today_goal_card.value_label.setStyleSheet("color: #2ECC71;")

        self.total_pomodoros_card.value_label.setText(str(total_stats["total_pomodoros"]))
        self.total_focus_card.value_label.setText(format_duration(total_stats["total_focus_time"], True))
        self.total_tasks_card.value_label.setText(str(total_stats["completed_tasks"]))
        self.consecutive_days_card.value_label.setText(f"{total_stats['consecutive_days']}天")

        self.load_achievements()

    def load_achievements(self):
        for i in reversed(range(self.achievements_layout.count())):
            self.achievements_layout.itemAt(i).widget().setParent(None)

        achievements = self.stats_manager.get_achievements()
        for achievement in achievements:
            card = StatCard(
                achievement["icon"] + " " + achievement["name"],
                "已解锁" if achievement["unlocked"] else "未解锁",
                achievement["description"]
            )
            if achievement["unlocked"]:
                card.value_label.setStyleSheet("color: #2ECC71;")
            else:
                card.value_label.setStyleSheet("color: #888888;")
            self.achievements_layout.addWidget(card)

    def refresh(self):
        self.load_stats()
