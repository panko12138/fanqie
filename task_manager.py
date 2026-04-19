from datetime import datetime
from typing import List, Optional
from database import get_db_manager
from models import Task, TaskTemplate, StatusEnum, PriorityEnum, SubjectEnum
from utils.logger import get_logger
from utils.validators import (
    validate_task_name,
    validate_subject,
    validate_priority,
    validate_pomodoro_count,
)

logger = get_logger(__name__)


class TaskManager:
    def __init__(self):
        self.db_manager = get_db_manager()

    def create_task(
        self,
        name: str,
        subject: str = SubjectEnum.OTHER,
        estimated_pomodoros: int = 1,
        priority: str = PriorityEnum.MEDIUM,
        notes: Optional[str] = None,
    ) -> Task:
        is_valid, msg = validate_task_name(name)
        if not is_valid:
            raise ValueError(msg)
        is_valid, msg = validate_subject(subject)
        if not is_valid:
            raise ValueError(msg)
        is_valid, msg = validate_priority(priority)
        if not is_valid:
            raise ValueError(msg)
        is_valid, msg = validate_pomodoro_count(estimated_pomodoros)
        if not is_valid:
            raise ValueError(msg)

        with self.db_manager.session() as session:
            task = Task(
                name=name,
                subject=subject,
                estimated_pomodoros=estimated_pomodoros,
                actual_pomodoros=0,
                priority=priority,
                status=StatusEnum.ACTIVE,
                notes=notes,
            )
            session.add(task)
            session.flush()
            session.refresh(task)
            logger.info(f"创建任务: {task.id} - {task.name}")
            return task

    def get_task(self, task_id: int) -> Optional[Task]:
        with self.db_manager.session() as session:
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                session.expunge(task)
            return task

    def get_all_tasks(
        self,
        status: Optional[str] = None,
        subject: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> List[Task]:
        with self.db_manager.session() as session:
            query = session.query(Task)
            if status:
                query = query.filter_by(status=status)
            if subject:
                query = query.filter_by(subject=subject)
            if priority:
                query = query.filter_by(priority=priority)
            tasks = query.order_by(Task.created_at.desc()).all()
            for task in tasks:
                session.expunge(task)
            return tasks

    def update_task(
        self,
        task_id: int,
        name: Optional[str] = None,
        subject: Optional[str] = None,
        estimated_pomodoros: Optional[int] = None,
        priority: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Optional[Task]:
        with self.db_manager.session() as session:
            task = session.query(Task).filter_by(id=task_id).first()
            if not task:
                logger.warning(f"任务不存在: {task_id}")
                return None

            if name:
                is_valid, msg = validate_task_name(name)
                if not is_valid:
                    raise ValueError(msg)
                task.name = name
            if subject:
                is_valid, msg = validate_subject(subject)
                if not is_valid:
                    raise ValueError(msg)
                task.subject = subject
            if estimated_pomodoros is not None:
                is_valid, msg = validate_pomodoro_count(estimated_pomodoros)
                if not is_valid:
                    raise ValueError(msg)
                task.estimated_pomodoros = estimated_pomodoros
            if priority:
                is_valid, msg = validate_priority(priority)
                if not is_valid:
                    raise ValueError(msg)
                task.priority = priority
            if notes is not None:
                task.notes = notes

            session.flush()
            session.refresh(task)
            session.expunge(task)
            logger.info(f"更新任务: {task_id}")
            return task

    def delete_task(self, task_id: int) -> bool:
        with self.db_manager.session() as session:
            task = session.query(Task).filter_by(id=task_id).first()
            if not task:
                logger.warning(f"任务不存在: {task_id}")
                return False
            session.delete(task)
            logger.info(f"删除任务: {task_id}")
            return True

    def complete_task(self, task_id: int) -> Optional[Task]:
        with self.db_manager.session() as session:
            task = session.query(Task).filter_by(id=task_id).first()
            if not task:
                logger.warning(f"任务不存在: {task_id}")
                return None

            task.status = StatusEnum.COMPLETED
            task.completed_at = datetime.now()
            session.flush()
            session.refresh(task)
            session.expunge(task)
            logger.info(f"完成任务: {task_id}")
            return task

    def create_from_template(self, template_id: int) -> Optional[Task]:
        with self.db_manager.session() as session:
            template = session.query(TaskTemplate).filter_by(id=template_id).first()
            if not template:
                logger.warning(f"任务模板不存在: {template_id}")
                return None

            task = Task(
                name=template.name,
                subject=template.subject,
                estimated_pomodoros=template.estimated_pomodoros,
                actual_pomodoros=0,
                priority=PriorityEnum.MEDIUM,
                status=StatusEnum.ACTIVE,
                notes=template.description,
            )
            session.add(task)
            session.flush()
            session.refresh(task)
            session.expunge(task)
            logger.info(f"从模板创建任务: {task.id} - {template.name}")
            return task

    def get_templates(self, only_default: bool = False) -> List[TaskTemplate]:
        with self.db_manager.session() as session:
            query = session.query(TaskTemplate)
            if only_default:
                query = query.filter_by(is_default=True)
            templates = query.order_by(TaskTemplate.created_at.desc()).all()
            for template in templates:
                session.expunge(template)
            return templates

    def get_active_tasks(self) -> List[Task]:
        return self.get_all_tasks(status=StatusEnum.ACTIVE)

    def get_completed_tasks(self) -> List[Task]:
        return self.get_all_tasks(status=StatusEnum.COMPLETED)
