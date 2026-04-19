from sqlalchemy import Column, Integer, String, Text, Boolean
from .base import Base, TimestampMixin


class TaskTemplate(Base, TimestampMixin):
    __tablename__ = "task_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, comment="模板名称")
    subject = Column(String(50), nullable=False, comment="科目分类")
    estimated_pomodoros = Column(Integer, default=1, comment="预估番茄数")
    description = Column(Text, nullable=True, comment="模板描述")
    is_default = Column(Boolean, default=False, comment="是否为默认模板")

    def __repr__(self):
        return f"<TaskTemplate(id={self.id}, name='{self.name}')>"
