from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal, QRectF, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QBrush, QPainterPath
from timer import TimerState
from themes import ThemeManager
from utils.logger import get_logger

logger = get_logger(__name__)


class CircularProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress = 0.0
        self.color = QColor(231, 76, 60)
        self.background_color = QColor(200, 200, 200)
        self.setMinimumSize(200, 200)

    def set_progress(self, progress: float):
        self.progress = min(1.0, max(0.0, progress))
        self.update()

    def set_color(self, color: QColor):
        self.color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = min(self.width(), self.height())
        margin = 20
        diameter = w - 2 * margin

        center_x = self.width() / 2
        center_y = self.height() / 2

        painter.setPen(QPen(self.background_color, 10))
        painter.setBrush(Qt.NoBrush)
        x = int(center_x - diameter / 2)
        y = int(center_y - diameter / 2)
        painter.drawEllipse(x, y, int(diameter), int(diameter))

        if self.progress > 0:
            painter.setPen(QPen(self.color, 10))
            start_angle = 90 * 16
            span_angle = -int(self.progress * 360 * 16)
            x = int(center_x - diameter / 2)
            y = int(center_y - diameter / 2)
            painter.drawArc(x, y, int(diameter), int(diameter), start_angle, span_angle)


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
        self.is_timer_running = False  # 初始化状态属性
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        self.state_label = QLabel("准备开始")
        self.state_label.setAlignment(Qt.AlignCenter)
        state_font = QFont()
        state_font.setPointSize(18)
        state_font.setBold(True)
        self.state_label.setFont(state_font)
        layout.addWidget(self.state_label)

        self.progress_bar = CircularProgressBar()
        self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.progress_bar)

        self.time_label = QLabel("25:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        time_font = QFont()
        time_font.setPointSize(48)
        time_font.setBold(True)
        self.time_label.setFont(time_font)
        layout.addWidget(self.time_label)

        self.task_label = QLabel(self.current_task_name)
        self.task_label.setAlignment(Qt.AlignCenter)
        self.task_label.setStyleSheet("color: #666666; font-size: 14px;")
        self.task_label.setWordWrap(True)
        layout.addWidget(self.task_label)

        self.pomodoro_indicator = QLabel("●" * self.completed_pomodoros + "○" * (self.long_break_interval - self.completed_pomodoros))
        self.pomodoro_indicator.setAlignment(Qt.AlignCenter)
        self.pomodoro_indicator.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.pomodoro_indicator)

        button_layout = QHBoxLayout()

        self.start_pause_btn = QPushButton("开始")
        self.start_pause_btn.setMinimumHeight(50)
        self.start_pause_btn.clicked.connect(self.on_start_pause_clicked)
        button_layout.addWidget(self.start_pause_btn)

        self.reset_btn = QPushButton("重置")
        self.reset_btn.setMinimumHeight(50)
        self.reset_btn.clicked.connect(self.on_reset_clicked)
        button_layout.addWidget(self.reset_btn)

        self.skip_btn = QPushButton("跳过")
        self.skip_btn.setMinimumHeight(50)
        self.skip_btn.clicked.connect(self.on_skip_clicked)
        button_layout.addWidget(self.skip_btn)

        self.stop_btn = QPushButton("停止")
        self.stop_btn.setMinimumHeight(50)
        self.stop_btn.clicked.connect(self.on_stop_clicked)
        button_layout.addWidget(self.stop_btn)

        layout.addLayout(button_layout)

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
        colors = self.theme_manager.get_state_colors()

        if state == TimerState.FOCUS:
            self.state_label.setText("专注中")
            self.state_label.setStyleSheet(f"color: {colors['focus']};")
            self.progress_bar.setColor(QColor(colors["focus"]))
        elif state == TimerState.SHORT_BREAK:
            self.state_label.setText("短休息")
            self.state_label.setStyleSheet(f"color: {colors['short_break']};")
            self.progress_bar.setColor(QColor(colors["short_break"]))
        elif state == TimerState.LONG_BREAK:
            self.state_label.setText("长休息")
            self.state_label.setStyleSheet(f"color: {colors['long_break']};")
            self.progress_bar.setColor(QColor(colors["long_break"]))
        else:
            self.state_label.setText("准备开始")
            self.state_label.setStyleSheet("color: #666666;")

    def set_is_running(self, is_running: bool):
        self.is_timer_running = is_running
        if is_running:
            self.start_pause_btn.setText("暂停")
        else:
            self.start_pause_btn.setText("开始")

    def update_pomodoro_count(self, count: int):
        self.completed_pomodoros = count
        indicator = "●" * (count % self.long_break_interval) + "○" * (self.long_break_interval - (count % self.long_break_interval))
        self.pomodoro_indicator.setText(indicator)

    def set_current_task(self, task_name: str):
        self.current_task_name = task_name
        self.task_label.setText(task_name)

    def set_is_running(self, is_running: bool):
        self.is_timer_running = is_running
        if is_running:
            self.start_pause_btn.setText("暂停")
        else:
            self.start_pause_btn.setText("开始")

    def apply_theme(self):
        colors = self.theme_manager.get_state_colors()
        self.task_label.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 14px;")
