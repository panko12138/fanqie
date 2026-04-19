from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Index
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum


class SubjectEnum(str, enum.Enum):
    POLITICS = "政治"
    ENGLISH = "英语"
    MATH = "数学"
    SPECIALIZED = "专业课"
    OTHER = "其他"


class PriorityEnum(str, enum.Enum):
    HIGH = "高"
    MEDIUM = "中"
    LOW = "低"


class StatusEnum(str, enum.Enum):
    ACTIVE = "进行中"
    COMPLETED = "已完成"


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, comment="任务名称")
    subject = Column(String(50), nullable=False, default=SubjectEnum.OTHER, comment="科目分类")
    estimated_pomodoros = Column(Integer, default=1, comment="预估番茄数")
    actual_pomodoros = Column(Integer, default=0, comment="实际番茄数")
    priority = Column(String(20), default=PriorityEnum.MEDIUM, comment="优先级")
    status = Column(String(20), default=StatusEnum.ACTIVE, comment="状态")
    notes = Column(Text, nullable=True, comment="任务备注")
    completed_at = Column(DateTime, nullable=True, comment="完成时间")

    pomodoro_sessions = relationship("PomodoroSession", back_populates="task", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_status_created", "status", "created_at"),
        Index("idx_subject", "subject"),
    )

    def __repr__(self):
        return f"<Task(id={self.id}, name='{self.name}', status='{self.status}')>"
