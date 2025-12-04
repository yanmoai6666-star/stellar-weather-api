from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.utils.database import get_db
from app.schemas.horoscope import HoroscopeResponse, TodayHoroscope
from app.services.horoscope_service import HoroscopeService

# 创建路由实例
router = APIRouter()


@router.get("/{sign}", response_model=HoroscopeResponse, summary="获取星座运势")
async def get_horoscope(
    sign: str,
    db: Session = Depends(get_db)
):
    """根据星座名称获取星象运势数据"""
    horoscope_service = HoroscopeService(db)
    
    # 尝试获取星象数据
    horoscope = horoscope_service.get_or_fetch_horoscope(sign)
    
    if not horoscope:
        raise HTTPException(status_code=404, detail=f"未找到星座 {sign} 的运势数据")
    
    return horoscope


@router.get("/{sign}/today", response_model=TodayHoroscope, summary="获取今日星座运势")
async def get_today_horoscope(
    sign: str,
    db: Session = Depends(get_db)
):
    """根据星座名称获取今日星象运势数据"""
    horoscope_service = HoroscopeService(db)
    
    # 尝试获取星象数据
    horoscope = horoscope_service.get_or_fetch_horoscope(sign)
    
    if not horoscope:
        raise HTTPException(status_code=404, detail=f"未找到星座 {sign} 的运势数据")
    
    return horoscope


@router.get("/all/today", response_model=List[TodayHoroscope], summary="获取所有星座今日运势")
async def get_all_today_horoscopes(
    db: Session = Depends(get_db)
):
    """获取所有星座的今日星象运势数据"""
    horoscope_service = HoroscopeService(db)
    
    # 从数据库获取所有星座的今日运势
    horoscopes = horoscope_service.get_all_horoscopes()
    
    # 如果数据库中没有数据，则从API获取
    if not horoscopes:
        # 所有星座列表
        signs = ["白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座", 
                 "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座"]
        
        horoscopes = []
        for sign in signs:
            horoscope = horoscope_service.get_or_fetch_horoscope(sign)
            if horoscope:
                horoscopes.append(horoscope)
    
    if not horoscopes:
        raise HTTPException(status_code=404, detail="未找到任何星座的运势数据")
    
    return horoscopes
