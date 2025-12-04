from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.utils.database import Base


class Horoscope(Base):
    """星象数据模型"""
    __tablename__ = "horoscope"
    
    id = Column(Integer, primary_key=True, index=True)
    sign = Column(String(50), index=True, nullable=False)  # 星座名称
    date_range = Column(String(100), nullable=False)  # 日期范围
    today = Column(Text, nullable=False)  # 今日运势
    tomorrow = Column(Text, nullable=False)  # 明日运势
    week = Column(Text, nullable=False)  # 本周运势
    month = Column(Text, nullable=False)  # 本月运势
    year = Column(Text, nullable=False)  # 本年运势
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
