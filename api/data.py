from prisma import Prisma
from pydantic import BaseModel
from datetime import datetime, timedelta
import csv


class DBData(BaseModel):
    date: str
    region: str
    obstacle: int
    canal: int
    security: int
    sanitary: int
    traffic: int
    road: int
    sidewalk: int
    sewer: int
    flood: int
    bridge: int
    electricWire: int
    light: int
    tree: int


async def addData(data: dict) -> bool:
    prisma = Prisma()
    await prisma.connect()
    isSuccess = False
    
    try:
        await prisma.reporthistory.create(
            data={
                "date": datetime.strptime(data["date"], "%Y-%m-%d"),
                "region": data["region"],
                "obstacle": int(data["obstacle"]),
                "canal": int(data["canal"]),
                "security": int(data["security"]),
                "sanitary": int(data["sanitary"]),
                "traffic": int(data["traffic"]),
                "road": int(data["road"]),
                "sidewalk": int(data["sidewalk"]),
                "sewer": int(data["sewer"]),
                "flood": int(data["flood"]),
                "bridge": int(data["bridge"]),
                "electricWire": int(data["electricWire"]),
                "light": int(data["light"]),
                "tree": int(data["tree"]),
            }
        )
    except Exception as e:
        print(e)
        isSuccess = False
        
    await prisma.disconnect()
    return isSuccess


async def getData():
    prisma = Prisma()
    await prisma.connect()

    data = await prisma.reporthistory.find_many(
        where={"date": {"gte": datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)}}
    )

    await prisma.disconnect()
    return data


async def preloadData() -> bool:
    isSuccess = True
    print("[Database] Preload Data")
    with open("api/data.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            isSuccess = isSuccess & await addData(row)
    return isSuccess
