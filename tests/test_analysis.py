import pytest
from fastapi.testclient import TestClient


class TestAnalysisAPI:
    """分析API测试类"""
    
    def test_get_stellar_analysis_success(self, client: TestClient, monkeypatch):
        """测试成功获取天气和星象分析"""
        # 模拟天气服务返回
        def mock_weather_get_or_fetch_weather(self, city):
            from app.models.weather import Weather
            from app.schemas.weather import WeatherCreate
            
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
        
        # 模拟星象服务返回
        def mock_horoscope_get_or_fetch_horoscope(self, sign):
            from app.models.horoscope import Horoscope
            from app.schemas.horoscope import HoroscopeCreate
            
            horoscope_data = HoroscopeCreate(
                sign="白羊座",
                date_range="3月21日-4月19日",
                today="白羊座今日运势：整体运势良好，工作顺利，感情稳定。",
                tomorrow="白羊座明日运势：运势一般，需要注意人际关系。",
                week="白羊座本周运势：本周整体运势上升，适合开展新项目。",
                month="白羊座本月运势：本月运势平稳，财运不错。",
                year="白羊座本年运势：本年运势起伏较大，需要注意健康。"
            )
            db_horoscope = Horoscope(**horoscope_data.model_dump())
            db_horoscope.id = 1
            return db_horoscope
        
        # 使用monkeypatch替换真实方法
        from app.services.weather_service import WeatherService
        from app.services.horoscope_service import HoroscopeService
        monkeypatch.setattr(WeatherService, "get_or_fetch_weather", mock_weather_get_or_fetch_weather)
        monkeypatch.setattr(HoroscopeService, "get_or_fetch_horoscope", mock_horoscope_get_or_fetch_horoscope)
        
        # 调用API
        response = client.get("/api/analysis?city=北京&sign=白羊座")
        
        # 验证结果
        assert response.status_code == 200
        assert "analysis" in response.json()
        assert "北京" in response.json()["city"]
        assert "白羊座" in response.json()["sign"]
        assert "运势分析" in response.json()["analysis"]
    
    def test_get_stellar_analysis_missing_params(self, client: TestClient):
        """测试缺少参数的情况"""
        # 只提供city参数
        response = client.get("/api/analysis?city=北京")
        assert response.status_code == 422  # 参数验证错误
        
        # 只提供sign参数
        response = client.get("/api/analysis?sign=白羊座")
        assert response.status_code == 422  # 参数验证错误
        
        # 不提供任何参数
        response = client.get("/api/analysis")
        assert response.status_code == 422  # 参数验证错误
    
    def test_get_stellar_analysis_invalid_city(self, client: TestClient, monkeypatch):
        """测试无效城市的情况"""
        # 模拟天气服务返回None（城市不存在）
        def mock_weather_get_or_fetch_weather(self, city):
            return None
        
        # 使用monkeypatch替换真实方法
        from app.services.weather_service import WeatherService
        monkeypatch.setattr(WeatherService, "get_or_fetch_weather", mock_weather_get_or_fetch_weather)
        
        # 调用API
        response = client.get("/api/analysis?city=不存在的城市&sign=白羊座")
        
        # 验证结果
        assert response.status_code == 404
        assert "未找到城市" in response.json()["detail"]
    
    def test_get_stellar_analysis_invalid_sign(self, client: TestClient, monkeypatch):
        """测试无效星座的情况"""
        # 模拟天气服务正常返回
        def mock_weather_get_or_fetch_weather(self, city):
            from app.models.weather import Weather
            from app.schemas.weather import WeatherCreate
            
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
        
        # 模拟星象服务返回None（星座不存在）
        def mock_horoscope_get_or_fetch_horoscope(self, sign):
            return None
        
        # 使用monkeypatch替换真实方法
        from app.services.weather_service import WeatherService
        from app.services.horoscope_service import HoroscopeService
        monkeypatch.setattr(WeatherService, "get_or_fetch_weather", mock_weather_get_or_fetch_weather)
        monkeypatch.setattr(HoroscopeService, "get_or_fetch_horoscope", mock_horoscope_get_or_fetch_horoscope)
        
        # 调用API
        response = client.get("/api/analysis?city=北京&sign=不存在的星座")
        
        # 验证结果
        assert response.status_code == 404
        assert "未找到星座" in response.json()["detail"]
