import os
import httpx
from fastapi import HTTPException
import redis.asyncio as aioredis
import json

API_KEY=os.getenv("OPENWEATHER_API_KEY")

redis_client = aioredis.from_url("redis://localhost:6379")

async def get_weather(city: str):
    cached = await redis_client.get(f"weather:{city}")
    if cached:
        return json.loads(cached)
    async with httpx.AsyncClient() as client:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=pl'
        response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Nie znaleziono miasta")
        
        data = response.json()
        
        result = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }
        await redis_client.setex(f"weather:{city}", 3600, json.dumps(result))
        return result