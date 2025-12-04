import requests
from datetime import datetime, timedelta
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.horoscope import Horoscope
from app.schemas.horoscope import HoroscopeCreate, HoroscopeUpdate
from app.utils.config import settings


class HoroscopeService:
    """星象服务类，处理星象数据的获取和业务逻辑"""
    
    def __init__(self, db: Session):
        self.db = db
        self.api_key = settings.HOROSCOPE_API_KEY
        self.base_url = "https://api.example.com/horoscope"
    
    def get_horoscope_by_sign(self, sign: str) -> Optional[Horoscope]:
        """根据星座名称获取星象数据"""
        return self.db.query(Horoscope).filter(Horoscope.sign == sign).first()
    
    def get_all_horoscopes(self) -> List[Horoscope]:
        """获取所有星座的星象数据"""
        return self.db.query(Horoscope).all()
    
    def create_horoscope(self, horoscope_data: HoroscopeCreate) -> Horoscope:
        """创建星象数据"""
        db_horoscope = Horoscope(**horoscope_data.model_dump())
        self.db.add(db_horoscope)
        self.db.commit()
        self.db.refresh(db_horoscope)
        return db_horoscope
    
    def update_horoscope(self, horoscope_id: int, horoscope_data: HoroscopeUpdate) -> Optional[Horoscope]:
        """更新星象数据"""
        db_horoscope = self.db.query(Horoscope).filter(Horoscope.id == horoscope_id).first()
        if db_horoscope:
            update_data = horoscope_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_horoscope, field, value)
            self.db.commit()
            self.db.refresh(db_horoscope)
        return db_horoscope
    
    def delete_horoscope(self, horoscope_id: int) -> bool:
        """删除星象数据"""
        db_horoscope = self.db.query(Horoscope).filter(Horoscope.id == horoscope_id).first()
        if db_horoscope:
            self.db.delete(db_horoscope)
            self.db.commit()
            return True
        return False
    
    def fetch_horoscope_from_api(self, sign: str) -> Optional[dict]:
        """从外部API获取星象数据"""
        try:
            # 这里使用模拟数据，实际项目中应该调用真实的星象API
            mock_data = {
                "sign": sign,
                "date_range": self._get_date_range(sign),
                "today": f"{sign}今日运势：整体运势良好，工作顺利，感情稳定。",
                "tomorrow": f"{sign}明日运势：运势一般，需要注意人际关系。",
                "week": f"{sign}本周运势：本周整体运势上升，适合开展新项目。",
                "month": f"{sign}本月运势：本月运势平稳，财运不错。",
                "year": f"{sign}本年运势：本年运势起伏较大，需要注意健康。"
            }
            return mock_data
        except Exception as e:
            print(f"获取星象数据失败: {e}")
            return None
    
    def _get_date_range(self, sign: str) -> str:
        """根据星座名称获取日期范围"""
        date_ranges = {
            "白羊座": "3月21日-4月19日",
            "金牛座": "4月20日-5月20日",
            "双子座": "5月21日-6月21日",
            "巨蟹座": "6月22日-7月22日",
            "狮子座": "7月23日-8月22日",
            "处女座": "8月23日-9月22日",
            "天秤座": "9月23日-10月23日",
            "天蝎座": "10月24日-11月22日",
            "射手座": "11月23日-12月21日",
            "摩羯座": "12月22日-1月19日",
            "水瓶座": "1月20日-2月18日",
            "双鱼座": "2月19日-3月20日"
        }
        return date_ranges.get(sign, "")
    
    def parse_horoscope_api_response(self, api_response: dict) -> HoroscopeCreate:
        """解析外部API的星象数据响应"""
        return HoroscopeCreate(
            sign=api_response["sign"],
            date_range=api_response["date_range"],
            today=api_response["today"],
            tomorrow=api_response["tomorrow"],
            week=api_response["week"],
            month=api_response["month"],
            year=api_response["year"]
        )
    
    def get_or_fetch_horoscope(self, sign: str) -> Optional[Horoscope]:
        """获取星象数据，如果数据库中没有则从API获取"""
        # 先从数据库获取
        horoscope = self.get_horoscope_by_sign(sign)
        
        # 如果数据库中没有，或者数据超过1天，则从API获取
        if not horoscope or (
            datetime.utcnow() - horoscope.updated_at.replace(tzinfo=None) > timedelta(days=1)
        ):
            api_data = self.fetch_horoscope_from_api(sign)
            if api_data:
                horoscope_data = self.parse_horoscope_api_response(api_data)
                if horoscope:
                    # 更新现有数据
                    update_data = horoscope_data.model_dump(exclude_unset=True)
                    for field, value in update_data.items():
                        setattr(horoscope, field, value)
                    self.db.commit()
                    self.db.refresh(horoscope)
                else:
                    # 创建新数据
                    horoscope = self.create_horoscope(horoscope_data)
        
        return horoscope
