import requests
from datetime import datetime, timedelta
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.weather import Weather
from app.schemas.weather import WeatherCreate, WeatherUpdate, ForecastDay, WeatherForecast
from app.utils.config import settings


class WeatherService:
    """天气服务类，处理天气数据的获取和业务逻辑"""
    
    def __init__(self, db: Session):
        self.db = db
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_weather_by_city(self, city: str) -> Optional[Weather]:
        """根据城市名称获取天气数据"""
        return self.db.query(Weather).filter(Weather.city == city).first()
    
    def create_weather(self, weather_data: WeatherCreate) -> Weather:
        """创建天气数据"""
        db_weather = Weather(**weather_data.model_dump())
        self.db.add(db_weather)
        self.db.commit()
        self.db.refresh(db_weather)
        return db_weather
    
    def update_weather(self, weather_id: int, weather_data: WeatherUpdate) -> Optional[Weather]:
        """更新天气数据"""
        db_weather = self.db.query(Weather).filter(Weather.id == weather_id).first()
        if db_weather:
            update_data = weather_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_weather, field, value)
            self.db.commit()
            self.db.refresh(db_weather)
        return db_weather
    
    def delete_weather(self, weather_id: int) -> bool:
        """删除天气数据"""
        db_weather = self.db.query(Weather).filter(Weather.id == weather_id).first()
        if db_weather:
            self.db.delete(db_weather)
            self.db.commit()
            return True
        return False
    
    def fetch_weather_from_api(self, city: str) -> Optional[dict]:
        """从外部API获取天气数据"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",  # 使用摄氏度
                "lang": "zh_cn"  # 使用中文
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"获取天气数据失败: {e}")
            return None
    
    def fetch_forecast_from_api(self, city: str) -> Optional[dict]:
        """从外部API获取天气预报数据"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",  # 使用摄氏度
                "lang": "zh_cn"  # 使用中文
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"获取天气预报数据失败: {e}")
            return None
    
    def parse_weather_api_response(self, api_response: dict) -> WeatherCreate:
        """解析外部API的天气数据响应"""
        return WeatherCreate(
            city=api_response["name"],
            country=api_response["sys"]["country"],
            temperature=api_response["main"]["temp"],
            humidity=api_response["main"]["humidity"],
            wind_speed=api_response["wind"]["speed"],
            description=api_response["weather"][0]["description"],
            icon=api_response["weather"][0]["icon"]
        )
    
    def parse_forecast_api_response(self, api_response: dict) -> WeatherForecast:
        """解析外部API的天气预报数据响应"""
        city = api_response["city"]["name"]
        country = api_response["city"]["country"]
        
        # 按日期分组，只保留每天的第一个预测
        daily_forecasts = {}
        for item in api_response["list"]:
            date = item["dt_txt"].split(" ")[0]  # 获取日期部分
            if date not in daily_forecasts:
                daily_forecasts[date] = item
        
        # 转换为ForecastDay列表
        forecast_list = []
        for date, data in sorted(daily_forecasts.items()):
            forecast_day = ForecastDay(
                date=date,
                temperature_min=data["main"]["temp_min"],
                temperature_max=data["main"]["temp_max"],
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"],
                description=data["weather"][0]["description"],
                icon=data["weather"][0]["icon"]
            )
            forecast_list.append(forecast_day)
        
        return WeatherForecast(
            city=city,
            country=country,
            forecast=forecast_list
        )
    
    def get_or_fetch_weather(self, city: str) -> Optional[Weather]:
        """获取天气数据，如果数据库中没有则从API获取"""
        # 先从数据库获取
        weather = self.get_weather_by_city(city)
        
        # 如果数据库中没有，或者数据超过1小时，则从API获取
        if not weather or (
            datetime.utcnow() - weather.updated_at.replace(tzinfo=None) > timedelta(hours=1)
        ):
            api_data = self.fetch_weather_from_api(city)
            if api_data:
                weather_data = self.parse_weather_api_response(api_data)
                if weather:
                    # 更新现有数据
                    update_data = weather_data.model_dump(exclude_unset=True)
                    for field, value in update_data.items():
                        setattr(weather, field, value)
                    self.db.commit()
                    self.db.refresh(weather)
                else:
                    # 创建新数据
                    weather = self.create_weather(weather_data)
        
        return weather
