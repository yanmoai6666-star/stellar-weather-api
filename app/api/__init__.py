from app.api.weather import router as weather_router
from app.api.horoscope import router as horoscope_router
from app.api.analysis import router as analysis_router

__all__ = ["weather_router", "horoscope_router", "analysis_router"]
