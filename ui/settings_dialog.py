from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpinBox,
    QComboBox, QCheckBox, QTabWidget, QWidget, QFormLayout, QFileDialog,
    QMessageBox, QListWidget, QListWidgetItem, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database import get_db_manager
from models import Setting
from themes import ThemeManager, ThemeType
from backup import BackupManager
from ui.components import (
    StyledButton, PrimaryButton, DangerButton,
    StyledComboBox, StyledCard
)
from utils.logger import get_logger

logger = get_logger(__name__)


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme_manager = ThemeManager()
        self.backup_manager = BackupManager()
        self.settings = {}
        self.init_ui()
        self.load_settings()
        self.setWindowTitle("设置")
        self.resize(520, 620)

    def init_ui(self):
        colors = self.theme_manager.get_colors()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: transparent;
            }}
            QTabBar::tab {{
                background-color: transparent;
                color: {colors['text_secondary']};
                padding: 12px 24px;
                border: none;
                border-bottom: 2px solid transparent;
                margin-right: 4px;
                font-size: 14px;
                font-weight: 500;
            }}
            QTabBar::tab:selected {{
                color: {colors['text']};
                border-bottom: 2px solid {colors['focus']};
            }}
            QTabBar::tab:hover:!selected {{
                color: {colors['text']};
                background-color: {colors['card_background']};
            }}
        """)

        timer_tab = self._create_timer_tab()
        self.tab_widget.addTab(timer_tab, "计时器")

        appearance_tab = self._create_appearance_tab()
        self.tab_widget.addTab(appearance_tab, "外观")

        notification_tab = self._create_notification_tab()
        self.tab_widget.addTab(notification_tab, "通知")

        backup_tab = self._create_backup_tab()
        self.tab_widget.addTab(backup_tab, "备份")

        layout.addWidget(self.tab_widget)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        button_layout.addStretch()
        
        cancel_btn = StyledButton("取消")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        ok_btn = PrimaryButton("确定")
        ok_btn.clicked.connect(self.save_and_close)
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)

    def _create_timer_tab(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 8, 0, 8)

        from PyQt5.QtWidgets import QSpinBox
        self.focus_spin = QSpinBox()
        self.focus_spin.setRange(1, 60)
        self.focus_spin.setValue(25)
        self.focus_spin.setSuffix(" 分钟")
        self._style_spinbox(self.focus_spin)
        layout.addRow("专注时长:", self.focus_spin)

        self.short_break_spin = QSpinBox()
        self.short_break_spin.setRange(1, 15)
        self.short_break_spin.setValue(5)
        self.short_break_spin.setSuffix(" 分钟")
        self._style_spinbox(self.short_break_spin)
        layout.addRow("短休息时长:", self.short_break_spin)

        self.long_break_spin = QSpinBox()
        self.long_break_spin.setRange(1, 30)
        self.long_break_spin.setValue(15)
        self.long_break_spin.setSuffix(" 分钟")
        self._style_spinbox(self.long_break_spin)
        layout.addRow("长休息时长:", self.long_break_spin)

        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(2, 8)
        self.interval_spin.setValue(4)
        self._style_spinbox(self.interval_spin)
        layout.addRow("长休息间隔（番茄数）:", self.interval_spin)

        self.daily_goal_spin = QSpinBox()
        self.daily_goal_spin.setRange(1, 20)
        self.daily_goal_spin.setValue(8)
        self._style_spinbox(self.daily_goal_spin)
        layout.addRow("每日番茄目标:", self.daily_goal_spin)

        return widget

    def _style_spinbox(self, spinbox):
        colors = self.theme_manager.get_colors()
        spinbox.setStyleSheet(f"""
            QSpinBox {{
                background-color: {colors['card_background']};
                color: {colors['text']};
                border: 2px solid {colors['border']};
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 14px;
            }}
            QSpinBox:focus {{
                border: 2px solid {colors['focus']};
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                border: none;
                background-color: transparent;
                width: 24px;
            }}
            QSpinBox::up-arrow {{
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-bottom: 6px solid {colors['text_secondary']};
            }}
            QSpinBox::down-arrow {{
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid {colors['text_secondary']};
            }}
        """)

    def _create_appearance_tab(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 8, 0, 8)

        self.theme_combo = StyledComboBox()
        self.theme_combo.addItem("浅色", ThemeType.LIGHT)
        self.theme_combo.addItem("深色", ThemeType.DARK)
        layout.addRow("主题:", self.theme_combo)

        return widget

    def _create_notification_tab(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 8, 0, 8)

        colors = self.theme_manager.get_colors()
        self.sound_check = QCheckBox("启用提示音")
        self.sound_check.setStyleSheet(f"""
            QCheckBox {{
                color: {colors['text']};
                spacing: 10px;
                font-size: 14px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border: 2px solid {colors['border']};
                border-radius: 4px;
                background-color: {colors['card_background']};
            }}
            QCheckBox::indicator:hover {{
                border-color: {colors['text_secondary']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {colors['focus']};
                border-color: {colors['focus']};
            }}
        """)
        layout.addRow(self.sound_check)

        self.notification_check = QCheckBox("启用系统通知")
        self.notification_check.setStyleSheet(f"""
            QCheckBox {{
                color: {colors['text']};
                spacing: 10px;
                font-size: 14px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border: 2px solid {colors['border']};
                border-radius: 4px;
                background-color: {colors['card_background']};
            }}
            QCheckBox::indicator:hover {{
                border-color: {colors['text_secondary']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {colors['focus']};
                border-color: {colors['focus']};
            }}
        """)
        layout.addRow(self.notification_check)

        return widget

    def _create_backup_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 8, 0, 8)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        create_backup_btn = PrimaryButton("创建备份")
        create_backup_btn.clicked.connect(self.create_backup)
        btn_layout.addWidget(create_backup_btn)
        
        restore_backup_btn = StyledButton("恢复备份")
        restore_backup_btn.clicked.connect(self.restore_backup)
        btn_layout.addWidget(restore_backup_btn)
        
        layout.addLayout(btn_layout)

        backup_label = QLabel("备份列表:")
        backup_label.setStyleSheet(f"color: {self.theme_manager.get_colors()['text']}; font-size: 14px; font-weight: 500;")
        layout.addWidget(backup_label)

        self.backup_list = QListWidget()
        self.backup_list.setSpacing(6)
        self.backup_list.setFrameShape(QFrame.StyledPanel)
        self.backup_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {self.theme_manager.get_colors()['card_background']};
                color: {self.theme_manager.get_colors()['text']};
                border: 1px solid {self.theme_manager.get_colors()['border']};
                border-radius: 8px;
                padding: 8px;
            }}
            QListWidget::item {{
                background-color: transparent;
                padding: 8px 12px;
                border-radius: 6px;
                margin: 2px 0px;
            }}
            QListWidget::item:hover {{
                background-color: {self.theme_manager.get_colors()['border']};
            }}
            QListWidget::item:selected {{
                background-color: {self.theme_manager.get_colors()['focus']};
                color: white;
            }}
        """)
        layout.addWidget(self.backup_list)

        delete_backup_btn = DangerButton("删除选中备份")
        delete_backup_btn.clicked.connect(self.delete_backup)
        layout.addWidget(delete_backup_btn)

        self.refresh_backup_list()

        return widget

    def load_settings(self):
        try:
            db_manager = get_db_manager()
            with db_manager.session() as session:
                settings_list = session.query(Setting).all()
                self.settings = {s.key: s.value for s in settings_list}

            self.focus_spin.setValue(int(self.settings.get("focus_duration", "1500")) // 60)
            self.short_break_spin.setValue(int(self.settings.get("short_break_duration", "300")) // 60)
            self.long_break_spin.setValue(int(self.settings.get("long_break_duration", "900")) // 60)
            self.interval_spin.setValue(int(self.settings.get("long_break_interval", "4")))
            self.daily_goal_spin.setValue(int(self.settings.get("daily_goal", "8")))

            theme_str = self.settings.get("theme", "light")
            theme = ThemeType(theme_str)
            index = self.theme_combo.findData(theme)
            if index >= 0:
                self.theme_combo.setCurrentIndex(index)

            self.sound_check.setChecked(self.settings.get("sound_enabled", "true").lower() == "true")
            self.notification_check.setChecked(self.settings.get("notification_enabled", "true").lower() == "true")
        except Exception as e:
            logger.warning(f"加载设置失败: {e}")

    def save_settings(self):
        try:
            db_manager = get_db_manager()
            with db_manager.session() as session:
                new_settings = {
                    "focus_duration": str(self.focus_spin.value() * 60),
                    "short_break_duration": str(self.short_break_spin.value() * 60),
                    "long_break_duration": str(self.long_break_spin.value() * 60),
                    "long_break_interval": str(self.interval_spin.value()),
                    "daily_goal": str(self.daily_goal_spin.value()),
                    "theme": self.theme_combo.currentData().value,
                    "sound_enabled": "true" if self.sound_check.isChecked() else "false",
                    "notification_enabled": "true" if self.notification_check.isChecked() else "false",
                }

                for key, value in new_settings.items():
                    setting = session.query(Setting).filter_by(key=key).first()
                    if setting:
                        setting.value = value
                    else:
                        setting = Setting(key=key, value=value)
                        session.add(setting)
                session.commit()

            self.theme_manager.set_theme(self.theme_combo.currentData())
            logger.info("设置保存成功")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存设置失败: {e}")
            logger.error(f"保存设置失败: {e}")

    def save_and_close(self):
        self.save_settings()
        self.accept()

    def create_backup(self):
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "创建备份", "", "JSON Files (*.json)"
            )
            if filename:
                self.backup_manager.create_backup(filename)
                QMessageBox.information(self, "成功", "备份创建成功!")
                self.refresh_backup_list()
        except Exception as e:
            QMessageBox.warning(self, "错误", f"创建备份失败: {e}")

    def restore_backup(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self, "恢复备份", "", "JSON Files (*.json)"
            )
            if filename:
                reply = QMessageBox.question(
                    self, "确认恢复",
                    "恢复备份将覆盖当前所有数据，确定要恢复吗？",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    if self.backup_manager.restore_backup(filename):
                        QMessageBox.information(self, "成功", "备份恢复成功!")
                    else:
                        QMessageBox.warning(self, "错误", "备份恢复失败!")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"恢复备份失败: {e}")

    def delete_backup(self):
        current_item = self.backup_list.currentItem()
        if current_item:
            backup_path = current_item.data(Qt.UserRole)
            reply = QMessageBox.question(
                self, "确认删除", "确定要删除这个备份文件吗？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.backup_manager.delete_backup(backup_path)
                self.refresh_backup_list()

    def refresh_backup_list(self):
        self.backup_list.clear()
        backups = self.backup_manager.list_backups()
        for backup in backups:
            item = QListWidgetItem(f"{backup['filename']} - {backup['created_at'].strftime('%Y-%m-%d %H:%M')}")
            item.setData(Qt.UserRole, backup['path'])
            self.backup_list.addItem(item)
