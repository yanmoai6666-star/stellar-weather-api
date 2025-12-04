import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.horoscope import Horoscope
from app.schemas.horoscope import HoroscopeCreate


class TestHoroscopeAPI:
    """星象API测试类"""
    
    def test_get_horoscope_not_found(self, client: TestClient):
        """测试获取不存在的星座运势"""
        response = client.get("/api/horoscope/不存在的星座")
        assert response.status_code == 404
        assert "未找到星座" in response.json()["detail"]
    
    def test_get_horoscope_with_mock_data(self, client: TestClient, db_session: Session, monkeypatch):
        """使用模拟数据测试获取星座运势接口"""
        # 模拟HoroscopeService的get_or_fetch_horoscope方法
        def mock_get_or_fetch_horoscope(self, sign):
            # 创建一个模拟的星象数据
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
        from app.services.horoscope_service import HoroscopeService
        monkeypatch.setattr(HoroscopeService, "get_or_fetch_horoscope", mock_get_or_fetch_horoscope)
        
        # 调用API
        response = client.get("/api/horoscope/白羊座")
        
        # 验证结果
        assert response.status_code == 200
        assert response.json()["sign"] == "白羊座"
        assert "整体运势良好" in response.json()["today"]
        assert "3月21日-4月19日" in response.json()["date_range"]
    
    def test_get_today_horoscope(self, client: TestClient, monkeypatch):
        """测试获取今日星座运势接口"""
        # 模拟星象数据
        def mock_get_or_fetch_horoscope(self, sign):
            horoscope_data = HoroscopeCreate(
                sign="金牛座",
                date_range="4月20日-5月20日",
                today="金牛座今日运势：财运不错，适合理财投资。",
                tomorrow="金牛座明日运势：工作压力较大，需要适当放松。",
                week="金牛座本周运势：本周感情运势上升，适合表白。",
                month="金牛座本月运势：本月健康运势一般，注意休息。",
                year="金牛座本年运势：本年事业运势良好，有晋升机会。"
            )
            db_horoscope = Horoscope(**horoscope_data.model_dump())
            db_horoscope.id = 2
            return db_horoscope
        
        # 使用monkeypatch替换真实方法
        from app.services.horoscope_service import HoroscopeService
        monkeypatch.setattr(HoroscopeService, "get_or_fetch_horoscope", mock_get_or_fetch_horoscope)
        
        # 调用API
        response = client.get("/api/horoscope/金牛座/today")
        
        # 验证结果
        assert response.status_code == 200
        assert response.json()["sign"] == "金牛座"
        assert "财运不错" in response.json()["today"]
    
    def test_get_all_today_horoscopes(self, client: TestClient, monkeypatch):
        """测试获取所有星座今日运势接口"""
        # 模拟所有星座数据
        def mock_get_all_horoscopes(self):
            signs = ["白羊座", "金牛座", "双子座"]
            horoscopes = []
            
            for i, sign in enumerate(signs):
                horoscope_data = HoroscopeCreate(
                    sign=sign,
                    date_range="测试日期范围",
                    today=f"{sign}今日运势：测试运势数据。",
                    tomorrow="测试明日运势",
                    week="测试本周运势",
                    month="测试本月运势",
                    year="测试本年运势"
                )
                db_horoscope = Horoscope(**horoscope_data.model_dump())
                db_horoscope.id = i + 1
                horoscopes.append(db_horoscope)
            
            return horoscopes
        
        # 使用monkeypatch替换真实方法
        from app.services.horoscope_service import HoroscopeService
        monkeypatch.setattr(HoroscopeService, "get_all_horoscopes", mock_get_all_today_horoscopes)
        
        # 调用API
        response = client.get("/api/horoscope/all/today")
        
        # 验证结果
        assert response.status_code == 200
        assert len(response.json()) == 3
        assert response.json()[0]["sign"] == "白羊座"
        assert response.json()[1]["sign"] == "金牛座"
        assert response.json()[2]["sign"] == "双子座"
