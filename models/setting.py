from sqlalchemy import Column, String, Text, DateTime, func
from .base import Base


class Setting(Base):
    __tablename__ = "settings"

    key = Column(String(100), primary_key=True, comment="设置项名称")
    value = Column(Text, nullable=False, comment="设置项值")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<Setting(key='{self.key}', value='{self.value}')>"
