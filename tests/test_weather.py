import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.weather import Weather
from app.schemas.weather import WeatherCreate


class TestWeatherAPI:
    """天气API测试类"""
    
    def test_root_endpoint(self, client: TestClient):
        """测试根路径"""
        response = client.get("/")
        assert response.status_code == 200
        assert "Welcome to Stellar Weather API" in response.json()["message"]
    
    def test_health_check(self, client: TestClient):
        """测试健康检查接口"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_get_weather_not_found(self, client: TestClient):
        """测试获取不存在的城市天气"""
        response = client.get("/api/weather/不存在的城市")
        assert response.status_code == 404
        assert "未找到城市" in response.json()["detail"]
    
    def test_get_weather_with_mock_data(self, client: TestClient, db_session: Session, monkeypatch):
        """使用模拟数据测试获取天气接口"""
        # 模拟WeatherService的get_or_fetch_weather方法
        def mock_get_or_fetch_weather(self, city):
            # 创建一个模拟的天气数据
            weather_data = WeatherCreate(
                city="北京",
                country="CN",
                temperature=25.5,
                humidity=60,
                wind_speed=3.5,
                description="晴",
                icon="01d"
            )
            db_weather = Weather(**weather_data.model_dump())
            db_weather.id = 1
            return db_weather
        
        # 使用monkeypatch替换真实方法
        from app.services.weather_service import WeatherService
        monkeypatch.setattr(WeatherService, "get_or_fetch_weather", mock_get_or_fetch_weather)
        
        # 调用API
        response = client.get("/api/weather/北京")
        
        # 验证结果
        assert response.status_code == 200
        assert response.json()["city"] == "北京"
        assert response.json()["temperature"] == 25.5
        assert response.json()["description"] == "晴"
    
    def test_get_weather_forecast(self, client: TestClient, monkeypatch):
        """测试获取天气预报接口"""
        # 模拟API响应
        mock_api_response = {
            "city": {
                "name": "北京",
                "country": "CN"
            },
            "list": [
                {
                    "dt_txt": "2023-12-04 12:00:00",
                    "main": {
                        "temp_min": 20.0,
                        "temp_max": 25.0,
                        "humidity": 60
                    },
                    "wind": {
                        "speed": 3.5
                    },
                    "weather": [
                        {
                            "description": "晴",
                            "icon": "01d"
                        }
                    ]
                },
                {
                    "dt_txt": "2023-12-05 12:00:00",
                    "main": {
                        "temp_min": 19.0,
                        "temp_max": 24.0,
                        "humidity": 65
                    },
                    "wind": {
                        "speed": 3.0
                    },
                    "weather": [
                        {
                            "description": "多云",
                            "icon": "02d"
                        }
                    ]
                }
            ]
        }
        
        # 模拟fetch_forecast_from_api方法
        def mock_fetch_forecast_from_api(self, city):
            return mock_api_response
        
        # 使用monkeypatch替换真实方法
        from app.services.weather_service import WeatherService
        monkeypatch.setattr(WeatherService, "fetch_forecast_from_api", mock_fetch_forecast_from_api)
        
        # 调用API
        response = client.get("/api/weather/forecast/北京?days=2")
        
        # 验证结果
        assert response.status_code == 200
        assert response.json()["city"] == "北京"
        assert len(response.json()["forecast"]) == 2
        assert response.json()["forecast"][0]["date"] == "2023-12-04"
        assert response.json()["forecast"][1]["date"] == "2023-12-05"
