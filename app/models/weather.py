from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from app.utils.database import Base


class Weather(Base):
    """天气数据模型"""
    __tablename__ = "weather"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), index=True, nullable=False)
    country = Column(String(100), nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    wind_speed = Column(Float, nullable=False)
    description = Column(String(200), nullable=False)
    icon = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
