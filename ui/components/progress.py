from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen
from themes import ThemeManager


class CircularProgressBar(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._progress = 0.0
        self.theme_manager = ThemeManager()
        self.color = QColor(self.theme_manager.get_colors()["primary"])
        self.background_color = QColor(self.theme_manager.get_colors()["border"])
        self.setMinimumSize(260, 260)
        self.theme_manager.theme_changed.connect(self._on_theme_changed)

    def _on_theme_changed(self):
        colors = self.theme_manager.get_colors()
        self.background_color = QColor(colors["border"])
        self.color = QColor(colors["primary"])
        self.update()

    def set_progress(self, progress: float):
        self._progress = min(1.0, max(0.0, progress))
        self.update()

    def set_color(self, color: QColor):
        self.color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        w = min(self.width(), self.height())
        margin = 30
        diameter = w - 2 * margin
        center_x = self.width() / 2
        center_y = self.height() / 2
        radius = diameter / 2

        painter.setPen(QPen(self.background_color, 14))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(int(center_x - radius), int(center_y - radius), int(diameter), int(diameter))

        if self._progress > 0:
            gradient_color = QColor(self.color)
            pen = QPen(gradient_color, 14)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)

            start_angle = 90 * 16
            span_angle = -int(self._progress * 360 * 16)
            painter.drawArc(int(center_x - radius), int(center_y - radius), int(diameter), int(diameter), start_angle, span_angle)


class PomodoroIndicator(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.completed = 0
        self.total = 4
        self.theme_manager = ThemeManager()
        self._dots = []
        self._setup_ui()
        self.theme_manager.theme_changed.connect(self._update_dots)

    def _setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignCenter)
        for _ in range(self.total):
            dot = QLabel()
            dot.setFixedSize(14, 14)
            self.layout.addWidget(dot)
            self._dots.append(dot)
        self._update_dots()

    def set_completed(self, completed: int):
        self.completed = completed % self.total
        self._update_dots()

    def set_total(self, total: int):
        self.total = total
        colors = self.theme_manager.get_colors()

        while len(self._dots) < total:
            dot = QLabel()
            dot.setFixedSize(14, 14)
            self.layout.addWidget(dot)
            self._dots.append(dot)

        while len(self._dots) > total:
            dot = self._dots.pop()
            dot.setParent(None)

        self._update_dots()

    def _update_dots(self):
        colors = self.theme_manager.get_colors()

        for i, dot in enumerate(self._dots):
            if i < self.completed:
                dot.setStyleSheet(
                    f"background-color: {colors['primary']}; border-radius: 7px;"
                )
            else:
                dot.setStyleSheet(
                    f"background-color: transparent; border: 2px solid {colors['border']}; border-radius: 7px;"
                )


class LinearProgressBar(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._progress = 0.0
        self.theme_manager = ThemeManager()
        self.setMinimumHeight(6)
        self.setMaximumHeight(6)
        self.theme_manager.theme_changed.connect(self.update)

    def set_progress(self, progress: float):
        self._progress = min(1.0, max(0.0, progress))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        colors = self.theme_manager.get_colors()
        bg_color = QColor(colors["border"])
        fill_color = QColor(colors["primary"])

        rect = self.rect()
        radius = rect.height() / 2

        painter.setPen(Qt.NoPen)
        painter.setBrush(bg_color)
        painter.drawRoundedRect(rect, radius, radius)

        if self._progress > 0:
            fill_rect = rect.adjusted(0, 0, -int(rect.width() * (1 - self._progress)), 0)
            painter.setBrush(fill_color)
            painter.drawRoundedRect(fill_rect, radius, radius)
