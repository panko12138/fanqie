from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath
from themes import ThemeManager


class CircularProgressBar(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.progress = 0.0
        self.theme_manager = ThemeManager()
        self.color = QColor(self.theme_manager.get_colors()["focus"])
        self.background_color = QColor(self.theme_manager.get_colors()["border"])
        self.setMinimumSize(220, 220)
        self.theme_manager.theme_changed.connect(self._on_theme_changed)
    
    def _on_theme_changed(self):
        colors = self.theme_manager.get_colors()
        self.background_color = QColor(colors["border"])
        self.update()
    
    def set_progress(self, progress: float):
        self.progress = min(1.0, max(0.0, progress))
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

        painter.setPen(QPen(self.background_color, 12))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(int(center_x - radius), int(center_y - radius), int(diameter), int(diameter))

        if self.progress > 0:
            gradient_color = QColor(self.color)
            pen = QPen(gradient_color, 12)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            
            start_angle = 90 * 16
            span_angle = -int(self.progress * 360 * 16)
            painter.drawArc(int(center_x - radius), int(center_y - radius), int(diameter), int(diameter), start_angle, span_angle)


class PomodoroIndicator(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.completed = 0
        self.total = 4
        self.theme_manager = ThemeManager()
        self._setup_ui()
        self.theme_manager.theme_changed.connect(self._update_dots)
    
    def _setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)
        self.layout.setAlignment(Qt.AlignCenter)
        self._update_dots()
    
    def set_completed(self, completed: int):
        self.completed = completed % self.total
        self._update_dots()
    
    def set_total(self, total: int):
        self.total = total
        self._update_dots()
    
    def _update_dots(self):
        colors = self.theme_manager.get_colors()
        
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        
        for i in range(self.total):
            dot = QLabel()
            dot.setFixedSize(12, 12)
            
            if i < self.completed:
                bg_color = colors["focus"]
            else:
                bg_color = colors["border"]
            
            dot.setStyleSheet(f"""
                QLabel {{
                    background-color: {bg_color};
                    border-radius: 6px;
                }}
            """)
            self.layout.addWidget(dot)
