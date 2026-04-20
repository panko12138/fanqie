from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget,
    QListWidgetItem, QComboBox, QDialog, QFormLayout, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from models import Task, SubjectEnum, PriorityEnum
from task_manager import TaskManager
from themes import ThemeManager
from ui.components import (
    StyledButton, PrimaryButton, DangerButton, SuccessButton,
    StyledCard, StyledLineEdit, StyledComboBox
)
from utils.logger import get_logger

logger = get_logger(__name__)


class TaskItemWidget(QFrame):
    task_selected = pyqtSignal(int)
    task_edited = pyqtSignal(int)
    task_deleted = pyqtSignal(int)
    task_completed = pyqtSignal(int)

    def __init__(self, task: Task, parent=None):
        super().__init__(parent)
        self.task = task
        self.theme_manager = ThemeManager()
        self.init_ui()
        self.theme_manager.theme_changed.connect(self._update_styles)

    def _update_styles(self):
        colors = self.theme_manager.get_colors()
        self.subject_label.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 13px;")
        if self.task.notes:
            self.notes_label.setStyleSheet(f"color: {colors['text_muted']}; font-size: 12px;")

    def init_ui(self):
        colors = self.theme_manager.get_colors()
        
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            TaskItemWidget {{
                background-color: {colors['card_background']};
                border: 1px solid {colors['border']};
                border-radius: 10px;
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(6)

        name_label = QLabel(self.task.name)
        name_font = QFont()
        name_font.setBold(True)
        name_font.setPointSize(14)
        name_label.setFont(name_font)
        name_label.setWordWrap(True)
        info_layout.addWidget(name_label)

        self.subject_label = QLabel(f"{self.task.subject} | 预估: {self.task.estimated_pomodoros} | 实际: {self.task.actual_pomodoros}")
        info_layout.addWidget(self.subject_label)

        if self.task.notes:
            self.notes_label = QLabel(self.task.notes)
            self.notes_label.setWordWrap(True)
            info_layout.addWidget(self.notes_label)

        layout.addLayout(info_layout, 1)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(8)

        select_btn = PrimaryButton("选择")
        select_btn.setFixedWidth(90)
        select_btn.clicked.connect(lambda: self.task_selected.emit(self.task.id))
        button_layout.addWidget(select_btn)

        edit_btn = StyledButton("编辑")
        edit_btn.setFixedWidth(90)
        edit_btn.clicked.connect(lambda: self.task_edited.emit(self.task.id))
        button_layout.addWidget(edit_btn)

        if self.task.status != "已完成":
            complete_btn = SuccessButton("完成")
            complete_btn.setFixedWidth(90)
            complete_btn.clicked.connect(lambda: self.task_completed.emit(self.task.id))
            button_layout.addWidget(complete_btn)

        delete_btn = DangerButton("删除")
        delete_btn.setFixedWidth(90)
        delete_btn.clicked.connect(lambda: self.task_deleted.emit(self.task.id))
        button_layout.addWidget(delete_btn)

        layout.addLayout(button_layout)
        
        self._update_styles()


class TaskEditDialog(QDialog):
    def __init__(self, task: Task = None, parent=None):
        super().__init__(parent)
        self.task = task
        self.theme_manager = ThemeManager()
        self.init_ui()
        self.setWindowTitle("编辑任务" if task else "新建任务")
        self.resize(450, 380)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        form_layout = QFormLayout()
        form_layout.setSpacing(12)

        self.name_edit = StyledLineEdit()
        self.name_edit.setText(self.task.name if self.task else "")
        form_layout.addRow("任务名称:", self.name_edit)

        self.subject_combo = StyledComboBox()
        for subject in SubjectEnum:
            self.subject_combo.addItem(subject.value, subject.value)
        if self.task:
            index = self.subject_combo.findData(self.task.subject)
            if index >= 0:
                self.subject_combo.setCurrentIndex(index)
        form_layout.addRow("科目:", self.subject_combo)

        self.priority_combo = StyledComboBox()
        for priority in PriorityEnum:
            self.priority_combo.addItem(priority.value, priority.value)
        if self.task:
            index = self.priority_combo.findData(self.task.priority)
            if index >= 0:
                self.priority_combo.setCurrentIndex(index)
        form_layout.addRow("优先级:", self.priority_combo)

        self.pomodoro_spin = StyledLineEdit()
        self.pomodoro_spin.setText(str(self.task.estimated_pomodoros) if self.task else "1")
        form_layout.addRow("预估番茄数:", self.pomodoro_spin)

        from PyQt5.QtWidgets import QTextEdit
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(100)
        self.notes_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.theme_manager.get_colors()['card_background']};
                color: {self.theme_manager.get_colors()['text']};
                border: 2px solid {self.theme_manager.get_colors()['border']};
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 14px;
                selection-background-color: {self.theme_manager.get_colors()['focus']};
            }}
        """)
        self.notes_edit.setText(self.task.notes if self.task else "")
        form_layout.addRow("备注:", self.notes_edit)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        button_layout.addStretch()
        
        cancel_btn = StyledButton("取消")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        ok_btn = PrimaryButton("确定")
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)

    def get_data(self) -> dict:
        return {
            "name": self.name_edit.text(),
            "subject": self.subject_combo.currentData(),
            "priority": self.priority_combo.currentData(),
            "estimated_pomodoros": int(self.pomodoro_spin.text() or "1"),
            "notes": self.notes_edit.toPlainText(),
        }


class TaskPanel(QWidget):
    task_selected = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.task_manager = TaskManager()
        self.theme_manager = ThemeManager()
        self.current_task_id = None
        self.init_ui()
        self.load_tasks()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        toolbar = StyledCard()
        # 使用 StyledCard 已经创建好的布局
        toolbar_layout = toolbar.layout
        toolbar_layout.setContentsMargins(16, 12, 16, 12)

        add_btn = PrimaryButton("+ 新建任务")
        add_btn.clicked.connect(self.on_add_task)
        toolbar_layout.addWidget(add_btn)

        self.filter_combo = StyledComboBox()
        self.filter_combo.addItem("全部", "all")
        self.filter_combo.addItem("进行中", "进行中")
        self.filter_combo.addItem("已完成", "已完成")
        self.filter_combo.addItem("政治", "政治")
        self.filter_combo.addItem("英语", "英语")
        self.filter_combo.addItem("数学", "数学")
        self.filter_combo.addItem("专业课", "专业课")
        self.filter_combo.currentIndexChanged.connect(self.on_filter_changed)
        toolbar_layout.addWidget(self.filter_combo)

        toolbar_layout.addStretch()
        layout.addWidget(toolbar)

        self.task_list = QListWidget()
        self.task_list.setSpacing(10)
        self.task_list.setFrameShape(QFrame.NoFrame)
        self.task_list.setStyleSheet(f"""
            QListWidget {{
                background-color: transparent;
                border: none;
            }}
        """)
        layout.addWidget(self.task_list)

    def load_tasks(self):
        self.task_list.clear()

        filter_type = self.filter_combo.currentData()

        if filter_type == "all":
            tasks = self.task_manager.get_all_tasks()
        elif filter_type in ["进行中", "已完成"]:
            tasks = self.task_manager.get_all_tasks(status=filter_type)
        else:
            tasks = self.task_manager.get_all_tasks(subject=filter_type)

        for task in tasks:
            item = QListWidgetItem()
            widget = TaskItemWidget(task)
            widget.task_selected.connect(self.on_task_selected)
            widget.task_edited.connect(self.on_task_edited)
            widget.task_deleted.connect(self.on_task_deleted)
            widget.task_completed.connect(self.on_task_completed)
            item.setSizeHint(widget.sizeHint())
            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, widget)

    def on_add_task(self):
        dialog = TaskEditDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            try:
                self.task_manager.create_task(**data)
                self.load_tasks()
                logger.info("任务创建成功")
            except ValueError as e:
                QMessageBox.warning(self, "输入错误", str(e))
            except Exception as e:
                QMessageBox.critical(self, "错误", f"创建任务失败: {e}")
                logger.error(f"创建任务失败: {e}")

    def on_task_selected(self, task_id: int):
        self.current_task_id = task_id
        self.task_selected.emit(task_id)
        logger.info(f"选择任务: {task_id}")

    def on_task_edited(self, task_id: int):
        try:
            task = self.task_manager.get_task(task_id)
            if task:
                dialog = TaskEditDialog(task, parent=self)
                if dialog.exec_() == QDialog.Accepted:
                    data = dialog.get_data()
                    try:
                        self.task_manager.update_task(task_id, **data)
                        self.load_tasks()
                        logger.info("任务更新成功")
                    except ValueError as e:
                        QMessageBox.warning(self, "输入错误", str(e))
                    except Exception as e:
                        QMessageBox.critical(self, "错误", f"更新任务失败: {e}")
                        logger.error(f"更新任务失败: {e}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取任务信息失败: {e}")
            logger.error(f"获取任务信息失败: {e}")

    def on_task_deleted(self, task_id: int):
        reply = QMessageBox.question(
            self, "确认删除", "确定要删除这个任务吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if self.task_manager.delete_task(task_id):
                self.load_tasks()
                if self.current_task_id == task_id:
                    self.current_task_id = None
                logger.info("任务删除成功")

    def on_task_completed(self, task_id: int):
        if self.task_manager.complete_task(task_id):
            self.load_tasks()
            logger.info("任务完成")

    def on_filter_changed(self):
        self.load_tasks()

    def refresh(self):
        self.load_tasks()
