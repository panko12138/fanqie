from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from timer import TimerState
from themes import ThemeManager, Typography
from ui.components import (
    StyledButton, PrimaryButton, DangerButton, GhostButton,
    CircularProgressBar, PomodoroIndicator, StyledCard
)
from utils.logger import get_logger

logger = get_logger(__name__)


class TimerWidget(QWidget):
    start_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    reset_clicked = pyqtSignal()
    skip_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme_manager = ThemeManager()
        self.current_state = TimerState.IDLE
        self.current_task_name = "无当前任务"
        self.completed_pomodoros = 0
        self.long_break_interval = 4
        self.is_timer_running = False
        self.init_ui()
        self.theme_manager.theme_changed.connect(self._on_theme_changed)

    def _on_theme_changed(self):
        self._update_styles()

    def _update_styles(self):
        colors = self.theme_manager.get_colors()
        self.task_label.setStyleSheet(
            f"color: {colors['text_secondary']}; font-size: 14px; border: none;"
        )

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        layout.setAlignment(Qt.AlignCenter)

        card = StyledCard()
        card_layout = card.layout
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(24)
        card_layout.setAlignment(Qt.AlignCenter)

        self.state_label = QLabel("准备开始")
        self.state_label.setAlignment(Qt.AlignCenter)
        state_font = QFont()
        state_font.setPointSize(18)
        state_font.setBold(True)
        self.state_label.setFont(state_font)
        card_layout.addWidget(self.state_label)

        self.progress_bar = CircularProgressBar()
        self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.progress_bar.setMinimumSize(280, 280)
        card_layout.addWidget(self.progress_bar, 0, Qt.AlignCenter)

        self.time_label = QLabel("25:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        time_font = QFont()
        time_font.setPointSize(48)
        time_font.setBold(True)
        time_font.setFamily("Consolas")
        self.time_label.setFont(time_font)
        card_layout.addWidget(self.time_label)

        task_widget = QWidget()
        task_widget.setStyleSheet("border: none;")
        task_layout = QHBoxLayout(task_widget)
        task_layout.setAlignment(Qt.AlignCenter)
        task_layout.setSpacing(8)
        task_layout.setContentsMargins(0, 0, 0, 0)

        task_icon = QLabel("📖")
        task_icon.setStyleSheet("font-size: 16px; border: none;")
        task_layout.addWidget(task_icon)

        self.task_label = QLabel(self.current_task_name)
        self.task_label.setAlignment(Qt.AlignCenter)
        self.task_label.setWordWrap(True)
        task_layout.addWidget(self.task_label)

        card_layout.addWidget(task_widget)

        self.pomodoro_indicator = PomodoroIndicator()
        card_layout.addWidget(self.pomodoro_indicator)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        button_layout.setAlignment(Qt.AlignCenter)

        self.start_pause_btn = PrimaryButton("开始")
        self.start_pause_btn.setMinimumWidth(120)
        self.start_pause_btn.clicked.connect(self.on_start_pause_clicked)
        button_layout.addWidget(self.start_pause_btn)

        self.reset_btn = GhostButton("重置")
        self.reset_btn.clicked.connect(self.on_reset_clicked)
        button_layout.addWidget(self.reset_btn)

        self.skip_btn = GhostButton("跳过")
        self.skip_btn.clicked.connect(self.on_skip_clicked)
        button_layout.addWidget(self.skip_btn)

        self.stop_btn = DangerButton("停止")
        self.stop_btn.setStyleSheet(
            self.stop_btn.styleSheet().replace(
                "background-color: #DC2626",
                "background-color: transparent; color: #DC2626; border: 2px solid #DC2626"
            )
        )
        self.stop_btn.clicked.connect(self.on_stop_clicked)
        button_layout.addWidget(self.stop_btn)

        card_layout.addLayout(button_layout)
        layout.addWidget(card, 0, Qt.AlignCenter)

        self._update_styles()

    def on_start_pause_clicked(self):
        if self.current_state == TimerState.IDLE or not self.is_timer_running:
            self.start_clicked.emit()
        else:
            self.pause_clicked.emit()

    def on_reset_clicked(self):
        self.reset_clicked.emit()

    def on_skip_clicked(self):
        self.skip_clicked.emit()

    def on_stop_clicked(self):
        self.stop_clicked.emit()

    def update_timer(self, minutes: int, seconds: int):
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}")

    def update_progress(self, progress: float):
        self.progress_bar.set_progress(progress)

    def update_state(self, state: TimerState):
        self.current_state = state
        colors = self.theme_manager.get_colors()

        if state == TimerState.FOCUS:
            self.state_label.setText("专注中")
            self.state_label.setStyleSheet(
                f"color: {colors['focus']}; font-size: 18px; font-weight: bold; border: none;"
            )
            self.progress_bar.set_color(QColor(colors["focus"]))
        elif state == TimerState.SHORT_BREAK:
            self.state_label.setText("短休息")
            self.state_label.setStyleSheet(
                f"color: {colors['short_break']}; font-size: 18px; font-weight: bold; border: none;"
            )
            self.progress_bar.set_color(QColor(colors["short_break"]))
        elif state == TimerState.LONG_BREAK:
            self.state_label.setText("长休息")
            self.state_label.setStyleSheet(
                f"color: {colors['long_break']}; font-size: 18px; font-weight: bold; border: none;"
            )
            self.progress_bar.set_color(QColor(colors["long_break"]))
        else:
            self.state_label.setText("准备开始")
            self.state_label.setStyleSheet(
                f"color: {colors['text_secondary']}; font-size: 18px; font-weight: bold; border: none;"
            )
            self.progress_bar.set_color(QColor(colors["primary"]))

    def set_is_running(self, is_running: bool):
        self.is_timer_running = is_running
        if is_running:
            self.start_pause_btn.setText("暂停")
        else:
            self.start_pause_btn.setText("开始")

    def update_pomodoro_count(self, count: int):
        self.completed_pomodoros = count
        self.pomodoro_indicator.set_completed(count)

    def set_current_task(self, task_name: str):
        self.current_task_name = task_name
        self.task_label.setText(task_name)
