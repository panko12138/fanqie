from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from timer import TimerState
from themes import ThemeManager
from ui.components import (
    StyledButton, PrimaryButton, DangerButton,
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
        self.task_label.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 14px;")

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)

        card = StyledCard()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.setSpacing(20)

        self.state_label = QLabel("准备开始")
        self.state_label.setAlignment(Qt.AlignCenter)
        state_font = QFont()
        state_font.setPointSize(18)
        state_font.setBold(True)
        self.state_label.setFont(state_font)
        card_layout.addWidget(self.state_label)

        self.progress_bar = CircularProgressBar()
        self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        card_layout.addWidget(self.progress_bar)

        self.time_label = QLabel("25:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        time_font = QFont()
        time_font.setPointSize(52)
        time_font.setBold(True)
        self.time_label.setFont(time_font)
        card_layout.addWidget(self.time_label)

        self.task_label = QLabel(self.current_task_name)
        self.task_label.setAlignment(Qt.AlignCenter)
        self.task_label.setWordWrap(True)
        card_layout.addWidget(self.task_label)

        self.pomodoro_indicator = PomodoroIndicator()
        card_layout.addWidget(self.pomodoro_indicator)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.start_pause_btn = PrimaryButton("开始")
        self.start_pause_btn.clicked.connect(self.on_start_pause_clicked)
        button_layout.addWidget(self.start_pause_btn)

        self.reset_btn = StyledButton("重置")
        self.reset_btn.clicked.connect(self.on_reset_clicked)
        button_layout.addWidget(self.reset_btn)

        self.skip_btn = StyledButton("跳过")
        self.skip_btn.clicked.connect(self.on_skip_clicked)
        button_layout.addWidget(self.skip_btn)

        self.stop_btn = DangerButton("停止")
        self.stop_btn.clicked.connect(self.on_stop_clicked)
        button_layout.addWidget(self.stop_btn)

        card_layout.addLayout(button_layout)
        layout.addWidget(card)

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
            self.state_label.setStyleSheet(f"color: {colors['focus']}; font-size: 18px; font-weight: bold;")
            self.progress_bar.set_color(QColor(colors["focus"]))
        elif state == TimerState.SHORT_BREAK:
            self.state_label.setText("短休息")
            self.state_label.setStyleSheet(f"color: {colors['short_break']}; font-size: 18px; font-weight: bold;")
            self.progress_bar.set_color(QColor(colors["short_break"]))
        elif state == TimerState.LONG_BREAK:
            self.state_label.setText("长休息")
            self.state_label.setStyleSheet(f"color: {colors['long_break']}; font-size: 18px; font-weight: bold;")
            self.progress_bar.set_color(QColor(colors["long_break"]))
        else:
            self.state_label.setText("准备开始")
            self.state_label.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 18px; font-weight: bold;")

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
