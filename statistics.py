from datetime import datetime, timedelta, date
from typing import Dict, List, Optional
from sqlalchemy import func, and_, or_
from database import get_db_manager
from models import PomodoroSession, Task, DailyStat, Achievement, SubjectEnum
from utils.logger import get_logger
from utils.helpers import get_week_range, get_month_range

logger = get_logger(__name__)


class StatisticsManager:
    def __init__(self):
        self.db_manager = get_db_manager()

    def get_today_stats(self) -> Dict:
        today = datetime.now().date()
        with self.db_manager.session() as session:
            stat = session.query(DailyStat).filter_by(date=today).first()
            if stat:
                return {
                    "date": stat.date,
                    "total_pomodoros": stat.total_pomodoros,
                    "total_focus_time": stat.total_focus_time,
                    "tasks_completed": stat.tasks_completed,
                    "daily_goal": stat.daily_goal,
                    "goal_achieved": stat.goal_achieved,
                }
            return {
                "date": today,
                "total_pomodoros": 0,
                "total_focus_time": 0,
                "tasks_completed": 0,
                "daily_goal": 8,
                "goal_achieved": False,
            }

    def get_week_stats(self) -> List[Dict]:
        start_date, end_date = get_week_range()
        with self.db_manager.session() as session:
            stats = session.query(DailyStat).filter(
                and_(DailyStat.date >= start_date, DailyStat.date <= end_date)
            ).order_by(DailyStat.date).all()

            result = []
            current_date = start_date
            while current_date <= end_date:
                stat = next((s for s in stats if s.date == current_date), None)
                if stat:
                    result.append({
                        "date": stat.date,
                        "total_pomodoros": stat.total_pomodoros,
                        "total_focus_time": stat.total_focus_time,
                    })
                else:
                    result.append({
                        "date": current_date,
                        "total_pomodoros": 0,
                        "total_focus_time": 0,
                    })
                current_date += timedelta(days=1)
            return result

    def get_month_stats(self) -> List[Dict]:
        start_date, end_date = get_month_range()
        with self.db_manager.session() as session:
            stats = session.query(DailyStat).filter(
                and_(DailyStat.date >= start_date, DailyStat.date <= end_date)
            ).order_by(DailyStat.date).all()

            result = []
            current_date = start_date
            while current_date <= end_date:
                stat = next((s for s in stats if s.date == current_date), None)
                if stat:
                    result.append({
                        "date": stat.date,
                        "total_pomodoros": stat.total_pomodoros,
                        "total_focus_time": stat.total_focus_time,
                    })
                else:
                    result.append({
                        "date": current_date,
                        "total_pomodoros": 0,
                        "total_focus_time": 0,
                    })
                current_date += timedelta(days=1)
            return result

    def get_subject_distribution(self) -> Dict[str, int]:
        with self.db_manager.session() as session:
            result = session.query(
                Task.subject,
                func.sum(Task.actual_pomodoros).label("total")
            ).filter(Task.actual_pomodoros > 0).group_by(Task.subject).all()

            distribution = {row[0]: row[1] for row in result}
            total = sum(distribution.values())
            return {
                "distribution": distribution,
                "total": total,
            }

    def get_total_stats(self) -> Dict:
        with self.db_manager.session() as session:
            total_pomodoros = session.query(func.count(PomodoroSession.id)).filter(
                PomodoroSession.completed == True
            ).scalar() or 0

            total_focus_time = session.query(func.sum(PomodoroSession.duration)).filter(
                PomodoroSession.completed == True
            ).scalar() or 0

            completed_tasks = session.query(func.count(Task.id)).filter(
                Task.status == "已完成"
            ).scalar() or 0

            consecutive_days = self._calculate_consecutive_days(session)
            max_consecutive_days = self._calculate_max_consecutive_days(session)

            return {
                "total_pomodoros": total_pomodoros,
                "total_focus_time": total_focus_time,
                "completed_tasks": completed_tasks,
                "consecutive_days": consecutive_days,
                "max_consecutive_days": max_consecutive_days,
            }

    def _calculate_consecutive_days(self, session) -> int:
        today = datetime.now().date()
        stats = session.query(DailyStat).filter(
            DailyStat.total_pomodoros > 0
        ).order_by(DailyStat.date.desc()).all()

        if not stats:
            return 0

        dates = [stat.date for stat in stats]
        consecutive = 0
        expected_date = today

        for stat_date in dates:
            if stat_date == expected_date:
                consecutive += 1
                expected_date -= timedelta(days=1)
            elif stat_date < expected_date:
                break

        return consecutive

    def _calculate_max_consecutive_days(self, session) -> int:
        stats = session.query(DailyStat).filter(
            DailyStat.total_pomodoros > 0
        ).order_by(DailyStat.date).all()

        if not stats:
            return 0

        max_consecutive = 1
        current_consecutive = 1
        prev_date = stats[0].date

        for stat in stats[1:]:
            if stat.date == prev_date + timedelta(days=1):
                current_consecutive += 1
                if current_consecutive > max_consecutive:
                    max_consecutive = current_consecutive
            else:
                current_consecutive = 1
            prev_date = stat.date

        return max_consecutive

    def get_achievements(self) -> List[Dict]:
        with self.db_manager.session() as session:
            achievements = session.query(Achievement).order_by(Achievement.id).all()
            return [{
                "id": a.id,
                "name": a.name,
                "description": a.description,
                "icon": a.icon,
                "condition": a.condition,
                "unlocked": a.unlocked_at is not None,
                "unlocked_at": a.unlocked_at,
            } for a in achievements]

    def check_achievement_unlock(self, achievement: Achievement, total_stats: Dict, extra_data: Dict = None) -> bool:
        condition = achievement.condition
        num = self._extract_number(condition)

        if "total_pomodoros" in condition:
            return total_stats["total_pomodoros"] >= num

        if "consecutive_days" in condition:
            return total_stats["consecutive_days"] >= num

        if "single_subject_pomodoros" in condition:
            if extra_data and "subject_distribution" in extra_data:
                subject_dist = extra_data["subject_distribution"]["distribution"]
                return any(count >= num for count in subject_dist.values())
            return False

        if "monthly_pomodoros" in condition:
            if extra_data and "month_stats" in extra_data:
                month_total = sum(day["total_pomodoros"] for day in extra_data["month_stats"])
                return month_total >= num
            return False

        if "all_subjects_pomodoros" in condition:
            if extra_data and "subject_distribution" in extra_data:
                subject_dist = extra_data["subject_distribution"]["distribution"]
                subjects = ["政治", "英语", "数学", "专业课", "其他"]
                return all(subject_dist.get(subject, 0) >= 10 for subject in subjects)
            return False

        if "exam_days_left" in condition and "total_pomodoros" in condition:
            if extra_data and "exam_days_left" in extra_data:
                exam_days = extra_data["exam_days_left"]
                return exam_days is not None and exam_days <= num and total_stats["total_pomodoros"] >= 1
            return False

        return False

    def check_and_unlock_achievements(self) -> List[Dict]:
        unlocked_achievements = []
        
        try:
            with self.db_manager.session() as session:
                total_stats = self.get_total_stats()
                
                extra_data = {
                    "subject_distribution": self.get_subject_distribution(),
                    "month_stats": self.get_month_stats(),
                }
                
                achievements = session.query(Achievement).all()
                
                for achievement in achievements:
                    if achievement.unlocked_at is None:
                        if self.check_achievement_unlock(achievement, total_stats, extra_data):
                            achievement.unlocked_at = datetime.now()
                            session.add(achievement)
                            unlocked_achievements.append({
                                "id": achievement.id,
                                "name": achievement.name,
                                "icon": achievement.icon,
                            })
                            logger.info(f"解锁成就: {achievement.name}")
        except Exception as e:
            logger.error(f"检查成就解锁失败: {e}")
        
        return unlocked_achievements

    def _extract_number(self, condition: str) -> int:
        import re
        match = re.search(r'\d+', condition)
        return int(match.group()) if match else 0

    def get_calendar_data(self, year: int, month: int) -> Dict[date, int]:
        with self.db_manager.session() as session:
            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = date(year, month + 1, 1) - timedelta(days=1)

            stats = session.query(DailyStat).filter(
                and_(DailyStat.date >= start_date, DailyStat.date <= end_date)
            ).all()

            return {stat.date: stat.total_pomodoros for stat in stats}
