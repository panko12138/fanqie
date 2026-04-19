import json
import os
from datetime import datetime
from typing import Optional
from database import get_db_manager
from models import Task, PomodoroSession, DailyStat, Setting, Achievement, TaskTemplate
from utils.logger import get_logger
from utils.helpers import get_data_path, ensure_dir

logger = get_logger(__name__)


class BackupManager:
    def __init__(self):
        self.db_manager = get_db_manager()
        self.backup_dir = os.path.join(get_data_path(), "backups")
        ensure_dir(self.backup_dir)

    def create_backup(self, backup_path: Optional[str] = None) -> str:
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"pomodoro_backup_{timestamp}.json")

        backup_data = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "data": {},
        }

        with self.db_manager.session() as session:
            tasks = session.query(Task).all()
            backup_data["data"]["tasks"] = [
                {
                    "id": t.id,
                    "name": t.name,
                    "subject": t.subject,
                    "estimated_pomodoros": t.estimated_pomodoros,
                    "actual_pomodoros": t.actual_pomodoros,
                    "priority": t.priority,
                    "status": t.status,
                    "notes": t.notes,
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                    "completed_at": t.completed_at.isoformat() if t.completed_at else None,
                } for t in tasks
            ]

            sessions = session.query(PomodoroSession).all()
            backup_data["data"]["pomodoro_sessions"] = [
                {
                    "id": s.id,
                    "task_id": s.task_id,
                    "start_time": s.start_time.isoformat() if s.start_time else None,
                    "end_time": s.end_time.isoformat() if s.end_time else None,
                    "duration": s.duration,
                    "completed": s.completed,
                    "created_at": s.created_at.isoformat() if s.created_at else None,
                } for s in sessions
            ]

            stats = session.query(DailyStat).all()
            backup_data["data"]["daily_stats"] = [
                {
                    "date": stat.date.isoformat(),
                    "total_pomodoros": stat.total_pomodoros,
                    "total_focus_time": stat.total_focus_time,
                    "tasks_completed": stat.tasks_completed,
                    "daily_goal": stat.daily_goal,
                    "goal_achieved": stat.goal_achieved,
                } for stat in stats
            ]

            settings = session.query(Setting).all()
            backup_data["data"]["settings"] = [
                {
                    "key": s.key,
                    "value": s.value,
                    "updated_at": s.updated_at.isoformat() if s.updated_at else None,
                } for s in settings
            ]

            achievements = session.query(Achievement).all()
            backup_data["data"]["achievements"] = [
                {
                    "id": a.id,
                    "name": a.name,
                    "description": a.description,
                    "icon": a.icon,
                    "condition": a.condition,
                    "unlocked_at": a.unlocked_at.isoformat() if a.unlocked_at else None,
                    "created_at": a.created_at.isoformat() if a.created_at else None,
                } for a in achievements
            ]

            templates = session.query(TaskTemplate).all()
            backup_data["data"]["task_templates"] = [
                {
                    "id": t.id,
                    "name": t.name,
                    "subject": t.subject,
                    "estimated_pomodoros": t.estimated_pomodoros,
                    "description": t.description,
                    "is_default": t.is_default,
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                } for t in templates
            ]

        with open(backup_path, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)

        logger.info(f"创建备份: {backup_path}")
        return backup_path

    def restore_backup(self, backup_path: str) -> bool:
        if not os.path.exists(backup_path):
            logger.error(f"备份文件不存在: {backup_path}")
            return False

        try:
            with open(backup_path, "r", encoding="utf-8") as f:
                backup_data = json.load(f)

            with self.db_manager.session() as session:
                session.query(PomodoroSession).delete()
                session.query(Task).delete()
                session.query(DailyStat).delete()
                session.query(Setting).delete()
                session.query(Achievement).delete()
                session.query(TaskTemplate).delete()

                if "data" in backup_data:
                    data = backup_data["data"]

                    if "tasks" in data:
                        for task_data in data["tasks"]:
                            task = Task(
                                id=task_data["id"],
                                name=task_data["name"],
                                subject=task_data["subject"],
                                estimated_pomodoros=task_data["estimated_pomodoros"],
                                actual_pomodoros=task_data["actual_pomodoros"],
                                priority=task_data["priority"],
                                status=task_data["status"],
                                notes=task_data["notes"],
                            )
                            if task_data["created_at"]:
                                task.created_at = datetime.fromisoformat(task_data["created_at"])
                            if task_data["completed_at"]:
                                task.completed_at = datetime.fromisoformat(task_data["completed_at"])
                            session.add(task)

                    if "pomodoro_sessions" in data:
                        for session_data in data["pomodoro_sessions"]:
                            pomodoro_session = PomodoroSession(
                                id=session_data["id"],
                                task_id=session_data["task_id"],
                                duration=session_data["duration"],
                                completed=session_data["completed"],
                            )
                            if session_data["start_time"]:
                                pomodoro_session.start_time = datetime.fromisoformat(session_data["start_time"])
                            if session_data["end_time"]:
                                pomodoro_session.end_time = datetime.fromisoformat(session_data["end_time"])
                            if session_data["created_at"]:
                                pomodoro_session.created_at = datetime.fromisoformat(session_data["created_at"])
                            session.add(pomodoro_session)

                    if "daily_stats" in data:
                        for stat_data in data["daily_stats"]:
                            stat = DailyStat(
                                date=datetime.fromisoformat(stat_data["date"]).date(),
                                total_pomodoros=stat_data["total_pomodoros"],
                                total_focus_time=stat_data["total_focus_time"],
                                tasks_completed=stat_data["tasks_completed"],
                                daily_goal=stat_data["daily_goal"],
                                goal_achieved=stat_data["goal_achieved"],
                            )
                            session.add(stat)

                    if "settings" in data:
                        for setting_data in data["settings"]:
                            setting = Setting(
                                key=setting_data["key"],
                                value=setting_data["value"],
                            )
                            if setting_data["updated_at"]:
                                setting.updated_at = datetime.fromisoformat(setting_data["updated_at"])
                            session.add(setting)

                    if "achievements" in data:
                        for achievement_data in data["achievements"]:
                            achievement = Achievement(
                                id=achievement_data["id"],
                                name=achievement_data["name"],
                                description=achievement_data["description"],
                                icon=achievement_data["icon"],
                                condition=achievement_data["condition"],
                            )
                            if achievement_data["unlocked_at"]:
                                achievement.unlocked_at = datetime.fromisoformat(achievement_data["unlocked_at"])
                            if achievement_data["created_at"]:
                                achievement.created_at = datetime.fromisoformat(achievement_data["created_at"])
                            session.add(achievement)

                    if "task_templates" in data:
                        for template_data in data["task_templates"]:
                            template = TaskTemplate(
                                id=template_data["id"],
                                name=template_data["name"],
                                subject=template_data["subject"],
                                estimated_pomodoros=template_data["estimated_pomodoros"],
                                description=template_data["description"],
                                is_default=template_data["is_default"],
                            )
                            if template_data["created_at"]:
                                template.created_at = datetime.fromisoformat(template_data["created_at"])
                            session.add(template)

                session.commit()

            logger.info(f"恢复备份成功: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"恢复备份失败: {e}")
            return False

    def list_backups(self) -> list:
        backups = []
        if os.path.exists(self.backup_dir):
            for filename in os.listdir(self.backup_dir):
                if filename.endswith(".json"):
                    filepath = os.path.join(self.backup_dir, filename)
                    stat = os.stat(filepath)
                    backups.append({
                        "filename": filename,
                        "path": filepath,
                        "size": stat.st_size,
                        "created_at": datetime.fromtimestamp(stat.st_mtime),
                    })
        return sorted(backups, key=lambda x: x["created_at"], reverse=True)

    def delete_backup(self, backup_path: str) -> bool:
        if os.path.exists(backup_path):
            os.remove(backup_path)
            logger.info(f"删除备份: {backup_path}")
            return True
        return False

    def export_data(self, export_path: str) -> str:
        return self.create_backup(export_path)

    def import_data(self, import_path: str) -> bool:
        return self.restore_backup(import_path)
