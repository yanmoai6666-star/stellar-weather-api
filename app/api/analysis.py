from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.utils.database import get_db
from app.services.weather_service import WeatherService
from app.services.horoscope_service import HoroscopeService

# 创建路由实例
router = APIRouter()


@router.get("/{city}/{sign}", summary="获取城市天气与星座的趣味分析")
async def get_analysis(
    city: str,
    sign: str,
    db: Session = Depends(get_db)
):
    """根据城市天气和星座提供趣味分析"""
    # 获取天气数据
    weather_service = WeatherService(db)
    weather = weather_service.get_or_fetch_weather(city)
    
    if not weather:
        raise HTTPException(status_code=404, detail=f"未找到城市 {city} 的天气数据")
    
    # 获取星象数据
    horoscope_service = HoroscopeService(db)
    horoscope = horoscope_service.get_or_fetch_horoscope(sign)
    
    if not horoscope:
        raise HTTPException(status_code=404, detail=f"未找到星座 {sign} 的运势数据")
    
    # 生成趣味分析
    analysis = generate_stellar_weather_analysis(weather, horoscope)
    
    return {
        "city": city,
        "sign": sign,
        "weather": {
            "temperature": weather.temperature,
            "description": weather.description,
            "humidity": weather.humidity
        },
        "horoscope": {
            "today": horoscope.today
        },
        "analysis": analysis
    }


def generate_stellar_weather_analysis(weather, horoscope) -> str:
    """生成天气与星象的趣味分析"""
    # 基础分析模板
    base_analysis = f"{weather.city}今日天气{weather.description}，气温{weather.temperature}℃。"
    base_analysis += f"{horoscope.sign}今日{horoscope.today.split('：')[1]}。"
    
    # 根据天气和星座生成特殊分析
    if weather.temperature > 30:
        if horoscope.sign in ["白羊座", "狮子座", "射手座"]:
            base_analysis += "火热的天气正符合火象星座的热情性格，今天适合户外活动！"
        else:
            base_analysis += "天气炎热，注意防暑降温，保持心情愉悦。"
    elif weather.temperature < 10:
        if horoscope.sign in ["摩羯座", "金牛座", "处女座"]:
            base_analysis += "寒冷的天气让土象星座更加沉稳，今天适合室内工作学习。"
        else:
            base_analysis += "天气寒冷，注意保暖，多喝热水。"
    else:
        if horoscope.sign in ["双子座", "天秤座", "水瓶座"]:
            base_analysis += "宜人的天气最适合风象星座的社交活动，今天不妨约上朋友聚会！"
        elif horoscope.sign in ["巨蟹座", "天蝎座", "双鱼座"]:
            base_analysis += "舒适的天气让水象星座更有创造力，今天适合艺术创作或冥想。"
        else:
            base_analysis += "天气宜人，是个适合做任何事情的好日子！"
    
    # 根据天气描述添加额外分析
    if "雨" in weather.description:
        base_analysis += "雨天适合静心思考，整理思绪，规划未来。"
    elif "晴" in weather.description:
        base_analysis += "晴天心情也会变好，不妨趁机完成一些一直拖延的任务。"
    elif "云" in weather.description:
        base_analysis += "多云的天气适合低调行事，默默积累能量。"
    
    return base_analysis
