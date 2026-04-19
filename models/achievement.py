from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, func
from .base import Base, TimestampMixin


class Achievement(Base, TimestampMixin):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="成就名称")
    description = Column(Text, nullable=False, comment="成就描述")
    icon = Column(String(255), nullable=False, comment="成就图标")
    condition = Column(Text, nullable=False, comment="解锁条件")
    unlocked_at = Column(DateTime, nullable=True, comment="解锁时间")

    def __repr__(self):
        return f"<Achievement(id={self.id}, name='{self.name}', unlocked={self.unlocked_at is not None})>"
