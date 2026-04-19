from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget,
    QListWidgetItem, QComboBox, QDialog, QLineEdit, QTextEdit, QFormLayout,
    QMessageBox, QSplitter, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from models import Task, SubjectEnum, PriorityEnum
from task_manager import TaskManager
from themes import ThemeManager
from utils.logger import get_logger

logger = get_logger(__name__)


class TaskItemWidget(QWidget):
    task_selected = pyqtSignal(int)
    task_edited = pyqtSignal(int)
    task_deleted = pyqtSignal(int)
    task_completed = pyqtSignal(int)

    def __init__(self, task: Task, parent=None):
        super().__init__(parent)
        self.task = task
        self.theme_manager = ThemeManager()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)

        name_label = QLabel(self.task.name)
        name_font = QFont()
        name_font.setBold(True)
        name_font.setPointSize(12)
        name_label.setFont(name_font)
        info_layout.addWidget(name_label)

        subject_label = QLabel(f"{self.task.subject} | 预估: {self.task.estimated_pomodoros} | 实际: {self.task.actual_pomodoros}")
        subject_label.setStyleSheet("color: #666666; font-size: 11px;")
        info_layout.addWidget(subject_label)

        if self.task.notes:
            notes_label = QLabel(self.task.notes)
            notes_label.setStyleSheet("color: #888888; font-size: 10px;")
            notes_label.setWordWrap(True)
            info_layout.addWidget(notes_label)

        layout.addLayout(info_layout, 1)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(5)

        select_btn = QPushButton("选择")
        select_btn.setMaximumWidth(80)
        select_btn.clicked.connect(lambda: self.task_selected.emit(self.task.id))
        button_layout.addWidget(select_btn)

        edit_btn = QPushButton("编辑")
        edit_btn.setMaximumWidth(80)
        edit_btn.clicked.connect(lambda: self.task_edited.emit(self.task.id))
        button_layout.addWidget(edit_btn)

        if self.task.status != "已完成":
            complete_btn = QPushButton("完成")
            complete_btn.setMaximumWidth(80)
            complete_btn.setStyleSheet("background-color: #2ECC71; color: white;")
            complete_btn.clicked.connect(lambda: self.task_completed.emit(self.task.id))
            button_layout.addWidget(complete_btn)

        delete_btn = QPushButton("删除")
        delete_btn.setMaximumWidth(80)
        delete_btn.setStyleSheet("background-color: #E74C3C; color: white;")
        delete_btn.clicked.connect(lambda: self.task_deleted.emit(self.task.id))
        button_layout.addWidget(delete_btn)

        layout.addLayout(button_layout)

        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet("border: 1px solid #ddd; border-radius: 5px; background-color: white;")


class TaskEditDialog(QDialog):
    def __init__(self, task: Task = None, parent=None):
        super().__init__(parent)
        self.task = task
        self.init_ui()
        self.setWindowTitle("编辑任务" if task else "新建任务")
        self.resize(400, 300)

    def init_ui(self):
        layout = QFormLayout(self)

        self.name_edit = QLineEdit()
        self.name_edit.setText(self.task.name if self.task else "")
        layout.addRow("任务名称:", self.name_edit)

        self.subject_combo = QComboBox()
        for subject in SubjectEnum:
            self.subject_combo.addItem(subject.value, subject.value)
        if self.task:
            index = self.subject_combo.findData(self.task.subject)
            if index >= 0:
                self.subject_combo.setCurrentIndex(index)
        layout.addRow("科目:", self.subject_combo)

        self.priority_combo = QComboBox()
        for priority in PriorityEnum:
            self.priority_combo.addItem(priority.value, priority.value)
        if self.task:
            index = self.priority_combo.findData(self.task.priority)
            if index >= 0:
                self.priority_combo.setCurrentIndex(index)
        layout.addRow("优先级:", self.priority_combo)

        self.pomodoro_spin = QLineEdit()
        self.pomodoro_spin.setText(str(self.task.estimated_pomodoros) if self.task else "1")
        layout.addRow("预估番茄数:", self.pomodoro_spin)

        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(100)
        self.notes_edit.setText(self.task.notes if self.task else "")
        layout.addRow("备注:", self.notes_edit)

        button_layout = QHBoxLayout()
        ok_btn = QPushButton("确定")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addRow(button_layout)

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
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        toolbar_layout = QHBoxLayout()

        add_btn = QPushButton("+ 新建任务")
        add_btn.clicked.connect(self.on_add_task)
        toolbar_layout.addWidget(add_btn)

        self.filter_combo = QComboBox()
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
        layout.addLayout(toolbar_layout)

        self.task_list = QListWidget()
        self.task_list.setSpacing(10)
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
