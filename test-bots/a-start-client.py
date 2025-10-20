import asyncio
from rubka.asynco import Robot

bot = Robot("token")

async def main():
    data = await bot.get_me()
    print(data)
    await bot.close()

asyncio.run(main())
