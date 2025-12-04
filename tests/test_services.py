import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.services.weather_service import WeatherService
from app.services.horoscope_service import HoroscopeService
from app.models.weather import Weather
from app.models.horoscope import Horoscope
from app.schemas.weather import WeatherCreate
from app.schemas.horoscope import HoroscopeCreate


class TestWeatherService:
    """天气服务测试类"""
    
    def test_should_update_expired_data(self, db_session: Session):
        """测试应该更新过期数据"""
        # 创建一个过期的天气数据（2小时前）
        expired_time = datetime.utcnow() - timedelta(hours=2)
        weather_data = WeatherCreate(
            city="北京",
            country="CN",
            temperature=20.0,
            humidity=50,
            wind_speed=2.0,
            description="多云",
            icon="02d"
        )
        
        expired_weather = Weather(**weather_data.model_dump(), last_updated=expired_time)
        db_session.add(expired_weather)
        db_session.commit()
        db_session.refresh(expired_weather)
        
        # 检查是否应该更新
        service = WeatherService(db_session)
        should_update = service._should_update(expired_weather)
        
        assert should_update is True
    
    def test_should_not_update_fresh_data(self, db_session: Session):
        """测试不应该更新新鲜数据"""
        # 创建一个新鲜的天气数据（30分钟前）
        fresh_time = datetime.utcnow() - timedelta(minutes=30)
        weather_data = WeatherCreate(
            city="北京",
            country="CN",
            temperature=20.0,
            humidity=50,
            wind_speed=2.0,
            description="多云",
            icon="02d"
        )
        
        fresh_weather = Weather(**weather_data.model_dump(), last_updated=fresh_time)
        db_session.add(fresh_weather)
        db_session.commit()
        db_session.refresh(fresh_weather)
        
        # 检查是否应该更新
        service = WeatherService(db_session)
        should_update = service._should_update(fresh_weather)
        
        assert should_update is False


class TestHoroscopeService:
    """星象服务测试类"""
    
    def test_should_update_expired_data(self, db_session: Session):
        """测试应该更新过期数据"""
        # 创建一个过期的星象数据（2天前）
        expired_time = datetime.utcnow() - timedelta(days=2)
        horoscope_data = HoroscopeCreate(
            sign="白羊座",
            date_range="3月21日-4月19日",
            today="测试今日运势",
            tomorrow="测试明日运势",
            week="测试本周运势",
            month="测试本月运势",
            year="测试本年运势"
        )
        
        expired_horoscope = Horoscope(**horoscope_data.model_dump(), last_updated=expired_time)
        db_session.add(expired_horoscope)
        db_session.commit()
        db_session.refresh(expired_horoscope)
        
        # 检查是否应该更新
        service = HoroscopeService(db_session)
        should_update = service._should_update(expired_horoscope)
        
        assert should_update is True
    
    def test_should_not_update_fresh_data(self, db_session: Session):
        """测试不应该更新新鲜数据"""
        # 创建一个新鲜的星象数据（12小时前）
        fresh_time = datetime.utcnow() - timedelta(hours=12)
        horoscope_data = HoroscopeCreate(
            sign="白羊座",
            date_range="3月21日-4月19日",
            today="测试今日运势",
            tomorrow="测试明日运势",
            week="测试本周运势",
            month="测试本月运势",
            year="测试本年运势"
        )
        
        fresh_horoscope = Horoscope(**horoscope_data.model_dump(), last_updated=fresh_time)
        db_session.add(fresh_horoscope)
        db_session.commit()
        db_session.refresh(fresh_horoscope)
        
        # 检查是否应该更新
        service = HoroscopeService(db_session)
        should_update = service._should_update(fresh_horoscope)
        
        assert should_update is False
