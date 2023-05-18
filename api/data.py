import asyncio
from prisma import Prisma
from prisma.models import ReportHistory
from datetime import datetime


async def addData(data: dict) -> bool:
    db = Prisma(auto_register=True)
    await db.connect()
    isSuccess = False

    try:
        data = await ReportHistory.prisma().create(
            data={
                "date": data["date"],
                "region": data["region"],
                "obstracle": data["obstracle"],
                "canel": data["canel"],
                "security": data["security"],
                "sanity": data["sanity"],
                "traffic": data["traffic"],
                "road": data["road"],
                "sidewalk": data["sidewalk"],
                "sewer": data["sewer"],
                "flood": data["flood"],
                "bridge": data["bridge"],
                "electricWire": data["electricWire"],
                "light": data["light"],
                "tree": data["tree"],
            }
        )
    except:
        isSuccess = False

    await db.disconnect()
    return isSuccess


asyncio.run(
    addData(
        {
            "date": datetime.strptime("2021-09-02", "%Y-%m-%d"),
            "region": "test",
            "obstracle": 0,
            "canel": 0,
            "security": 0,
            "sanity": 0,
            "traffic": 0,
            "road": 0,
            "sidewalk": 0,
            "sewer": 0,
            "flood": 0,
            "bridge": 0,
            "electricWire": 0,
            "light": 0,
            "tree": 0,
        }
    )
)
