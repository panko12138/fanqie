from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class PomodoroSession(Base, TimestampMixin):
    __tablename__ = "pomodoro_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True, comment="关联任务ID")
    start_time = Column(DateTime, nullable=False, comment="开始时间")
    end_time = Column(DateTime, nullable=False, comment="结束时间")
    duration = Column(Integer, nullable=False, comment="实际专注时长（秒）")
    completed = Column(Boolean, default=True, comment="是否完成（vs 中断）")

    task = relationship("Task", back_populates="pomodoro_sessions")

    __table_args__ = (
        Index("idx_task_id", "task_id"),
        Index("idx_start_time", "start_time"),
    )

    def __repr__(self):
        return f"<PomodoroSession(id={self.id}, task_id={self.task_id}, completed={self.completed})>"
