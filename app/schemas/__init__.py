from app.schemas.weather import (
    WeatherBase,
    WeatherCreate,
    WeatherUpdate,
    WeatherInDB,
    WeatherResponse,
    ForecastDay,
    WeatherForecast
)
from app.schemas.horoscope import (
    HoroscopeBase,
    HoroscopeCreate,
    HoroscopeUpdate,
    HoroscopeInDB,
    HoroscopeResponse,
    TodayHoroscope
)

__all__ = [
    # Weather schemas
    "WeatherBase",
    "WeatherCreate",
    "WeatherUpdate",
    "WeatherInDB",
    "WeatherResponse",
    "ForecastDay",
    "WeatherForecast",
    
    # Horoscope schemas
    "HoroscopeBase",
    "HoroscopeCreate",
    "HoroscopeUpdate",
    "HoroscopeInDB",
    "HoroscopeResponse",
    "TodayHoroscope"
]
