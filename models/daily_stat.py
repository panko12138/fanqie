from sqlalchemy import Column, Date, Integer, Boolean, Index
from .base import Base


class DailyStat(Base):
    __tablename__ = "daily_stats"

    date = Column(Date, primary_key=True, comment="日期")
    total_pomodoros = Column(Integer, default=0, comment="当日完成番茄数")
    total_focus_time = Column(Integer, default=0, comment="当日总专注时长（秒）")
    tasks_completed = Column(Integer, default=0, comment="当日完成任务数")
    daily_goal = Column(Integer, default=8, comment="每日番茄目标")
    goal_achieved = Column(Boolean, default=False, comment="是否达成目标")

    __table_args__ = (
        Index("idx_date", "date"),
    )

    def __repr__(self):
        return f"<DailyStat(date={self.date}, total_pomodoros={self.total_pomodoros})>"
