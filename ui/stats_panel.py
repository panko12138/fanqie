from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QScrollArea,
    QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from statistics import StatisticsManager
from themes import ThemeManager, Radius
from ui.components import StyledCard, StatCard, Badge
from utils.logger import get_logger
from utils.helpers import format_duration

logger = get_logger(__name__)


class StatsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stats_manager = StatisticsManager()
        self.theme_manager = ThemeManager()
        self.init_ui()
        self.load_stats()

    def init_ui(self):
        colors = self.theme_manager.get_colors()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(24)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content_widget = QWidget()
        content_widget.setStyleSheet("border: none;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(24)
        content_layout.setContentsMargins(0, 0, 0, 0)

        today_section = self._create_section("今日统计")
        self.today_grid = QGridLayout()
        self.today_grid.setSpacing(16)

        self.today_pomodoros_card = StatCard("完成番茄", "0")
        self.today_grid.addWidget(self.today_pomodoros_card, 0, 0)

        self.today_focus_card = StatCard("专注时间", "0分钟")
        self.today_grid.addWidget(self.today_focus_card, 0, 1)

        self.today_tasks_card = StatCard("完成任务", "0")
        self.today_grid.addWidget(self.today_tasks_card, 0, 2)

        self.today_goal_card = StatCard("每日目标", "未达成")
        self.today_grid.addWidget(self.today_goal_card, 0, 3)

        today_section.layout.addLayout(self.today_grid)
        content_layout.addWidget(today_section)

        total_section = self._create_section("总体统计")
        self.total_grid = QGridLayout()
        self.total_grid.setSpacing(16)

        self.total_pomodoros_card = StatCard("总番茄数", "0")
        self.total_grid.addWidget(self.total_pomodoros_card, 0, 0)

        self.total_focus_card = StatCard("总专注时间", "0小时")
        self.total_grid.addWidget(self.total_focus_card, 0, 1)

        self.total_tasks_card = StatCard("完成任务", "0")
        self.total_grid.addWidget(self.total_tasks_card, 0, 2)

        self.consecutive_days_card = StatCard("连续打卡", "0天")
        self.total_grid.addWidget(self.consecutive_days_card, 0, 3)

        total_section.layout.addLayout(self.total_grid)
        content_layout.addWidget(total_section)

        achievements_section = self._create_section("成就")
        self.achievements_widget = QWidget()
        self.achievements_widget.setStyleSheet("border: none;")
        self.achievements_layout = QHBoxLayout(self.achievements_widget)
        self.achievements_layout.setSpacing(12)
        self.achievements_layout.setAlignment(Qt.AlignLeft)
        achievements_section.layout.addWidget(self.achievements_widget)
        content_layout.addWidget(achievements_section)

        content_layout.addStretch()

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def _create_section(self, title: str) -> StyledCard:
        card = StyledCard()
        layout = card.layout
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet(
            f"color: {self.theme_manager.get_colors()['text_primary']}; border: none;"
        )
        layout.addWidget(title_label)

        return card

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._adjust_grid_columns()

    def _adjust_grid_columns(self):
        width = self.width()
        if width < 800:
            cols = 2
        else:
            cols = 4

        for grid in [self.today_grid, self.total_grid]:
            widgets = []
            for i in range(grid.count()):
                item = grid.itemAt(i)
                if item and item.widget():
                    widgets.append(item.widget())

            while grid.count():
                item = grid.takeAt(0)
                if item.widget():
                    grid.removeWidget(item.widget())

            for i, widget in enumerate(widgets):
                row = i // cols
                col = i % cols
                grid.addWidget(widget, row, col)

    def load_stats(self):
        today_stats = self.stats_manager.get_today_stats()
        total_stats = self.stats_manager.get_total_stats()

        self.today_pomodoros_card.value_label.setText(str(today_stats["total_pomodoros"]))
        self.today_focus_card.value_label.setText(format_duration(today_stats["total_focus_time"]))
        self.today_tasks_card.value_label.setText(str(today_stats["tasks_completed"]))
        goal_text = "已达成!" if today_stats["goal_achieved"] else f"目标: {today_stats['daily_goal']}"
        self.today_goal_card.value_label.setText(goal_text)
        if today_stats["goal_achieved"]:
            colors = self.theme_manager.get_colors()
            self.today_goal_card.value_label.setStyleSheet(
                f"color: {colors['success']}; font-size: 26px; font-weight: bold; border: none;"
            )

        self.total_pomodoros_card.value_label.setText(str(total_stats["total_pomodoros"]))
        self.total_focus_card.value_label.setText(format_duration(total_stats["total_focus_time"], True))
        self.total_tasks_card.value_label.setText(str(total_stats["completed_tasks"]))
        self.consecutive_days_card.value_label.setText(f"{total_stats['consecutive_days']}天")

        self.load_achievements()

    def load_achievements(self):
        for i in reversed(range(self.achievements_layout.count())):
            item = self.achievements_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

        achievements = self.stats_manager.get_achievements()
        for achievement in achievements:
            badge = Badge(
                f"{achievement['icon']} {achievement['name']}",
                variant="primary" if achievement["unlocked"] else "outline"
            )
            self.achievements_layout.addWidget(badge)

    def refresh(self):
        self.load_stats()
