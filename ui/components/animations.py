from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QWidget


class FadeAnimation:
    @staticmethod
    def fade_in(widget: QWidget, duration: int = 250, callback=None):
        if widget is None:
            if callback:
                callback()
            return None
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        if callback:
            animation.finished.connect(callback)
        animation.start(QPropertyAnimation.DeleteWhenStopped)
        return animation

    @staticmethod
    def fade_out(widget: QWidget, duration: int = 250, callback=None):
        if widget is None:
            if callback:
                callback()
            return None
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        if callback:
            animation.finished.connect(callback)
        animation.start(QPropertyAnimation.DeleteWhenStopped)
        return animation


class ScaleAnimation:
    @staticmethod
    def pulse(widget: QWidget, duration: int = 150):
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        original_geo = widget.geometry()
        center = original_geo.center()
        scaled_geo = original_geo.adjusted(2, 2, -2, -2)
        scaled_geo.moveCenter(center)
        animation.setStartValue(original_geo)
        animation.setEndValue(scaled_geo)
        animation.setEasingCurve(QEasingCurve.OutQuad)

        def restore():
            widget.setGeometry(original_geo)

        animation.finished.connect(restore)
        animation.start(QPropertyAnimation.DeleteWhenStopped)
        return animation
