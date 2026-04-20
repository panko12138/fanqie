from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QScrollArea,
    QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from statistics import StatisticsManager
from themes import ThemeManager
from ui.components import StyledCard
from utils.logger import get_logger
from utils.helpers import format_duration

logger = get_logger(__name__)


class StatCard(QFrame):
    def __init__(self, title: str, value: str, subtitle: str = "", parent=None):
        super().__init__(parent)
        self.theme_manager = ThemeManager()
        self.value_label = None
        self.init_ui(title, value, subtitle)
        self.theme_manager.theme_changed.connect(self._update_styles)

    def _update_styles(self):
        colors = self.theme_manager.get_colors()
        if self.title_label:
            self.title_label.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 13px;")
        if self.value_label:
            self.value_label.setStyleSheet(f"color: {colors['text']};")
        if self.subtitle_label:
            self.subtitle_label.setStyleSheet(f"color: {colors['text_muted']}; font-size: 12px;")

    def init_ui(self, title: str, value: str, subtitle: str):
        colors = self.theme_manager.get_colors()
        
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            StatCard {{
                background-color: {colors['card_background']};
                border: 1px solid {colors['border']};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        self.title_label = QLabel(title)
        layout.addWidget(self.title_label)

        self.value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(26)
        value_font.setBold(True)
        self.value_label.setFont(value_font)
        layout.addWidget(self.value_label)

        self.subtitle_label = None
        if subtitle:
            self.subtitle_label = QLabel(subtitle)
            layout.addWidget(self.subtitle_label)

        self.setMinimumHeight(130)
        self._update_styles()


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
        main_layout.setSpacing(20)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(24)
        content_layout.setContentsMargins(0, 0, 0, 0)

        today_section = self._create_section("今日统计")
        today_grid = QGridLayout()
        today_grid.setSpacing(16)
        
        self.today_pomodoros_card = StatCard("完成番茄", "0")
        today_grid.addWidget(self.today_pomodoros_card, 0, 0)

        self.today_focus_card = StatCard("专注时间", "0分钟")
        today_grid.addWidget(self.today_focus_card, 0, 1)

        self.today_tasks_card = StatCard("完成任务", "0")
        today_grid.addWidget(self.today_tasks_card, 0, 2)

        self.today_goal_card = StatCard("每日目标", "未达成")
        today_grid.addWidget(self.today_goal_card, 0, 3)

        today_section.layout.addLayout(today_grid)
        content_layout.addWidget(today_section)

        total_section = self._create_section("总体统计")
        total_grid = QGridLayout()
        total_grid.setSpacing(16)

        self.total_pomodoros_card = StatCard("总番茄数", "0")
        total_grid.addWidget(self.total_pomodoros_card, 0, 0)

        self.total_focus_card = StatCard("总专注时间", "0小时")
        total_grid.addWidget(self.total_focus_card, 0, 1)

        self.total_tasks_card = StatCard("完成任务", "0")
        total_grid.addWidget(self.total_tasks_card, 0, 2)

        self.consecutive_days_card = StatCard("连续打卡", "0天")
        total_grid.addWidget(self.consecutive_days_card, 0, 3)

        total_section.layout.addLayout(total_grid)
        content_layout.addWidget(total_section)

        achievements_section = self._create_section("成就")
        self.achievements_layout = QHBoxLayout()
        self.achievements_layout.setSpacing(16)
        achievements_section.layout.addLayout(self.achievements_layout)
        content_layout.addWidget(achievements_section)

        content_layout.addStretch()

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def _create_section(self, title: str) -> StyledCard:
        card = StyledCard()
        # 使用 StyledCard 已经创建好的布局
        layout = card.layout
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        title_label = QLabel(title)
        title_label.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        layout.addWidget(title_label)

        return card

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
            self.today_goal_card.value_label.setStyleSheet(f"color: {colors['success']}; font-size: 26px; font-weight: bold;")

        self.total_pomodoros_card.value_label.setText(str(total_stats["total_pomodoros"]))
        self.total_focus_card.value_label.setText(format_duration(total_stats["total_focus_time"], True))
        self.total_tasks_card.value_label.setText(str(total_stats["completed_tasks"]))
        self.consecutive_days_card.value_label.setText(f"{total_stats['consecutive_days']}天")

        self.load_achievements()

    def load_achievements(self):
        for i in reversed(range(self.achievements_layout.count())):
            self.achievements_layout.itemAt(i).widget().setParent(None)

        achievements = self.stats_manager.get_achievements()
        colors = self.theme_manager.get_colors()
        for achievement in achievements:
            card = StatCard(
                achievement["icon"] + " " + achievement["name"],
                "已解锁" if achievement["unlocked"] else "未解锁",
                achievement["description"]
            )
            if achievement["unlocked"]:
                card.value_label.setStyleSheet(f"color: {colors['success']}; font-size: 26px; font-weight: bold;")
            else:
                card.value_label.setStyleSheet(f"color: {colors['text_muted']}; font-size: 26px; font-weight: bold;")
            self.achievements_layout.addWidget(card)

    def refresh(self):
        self.load_stats()
