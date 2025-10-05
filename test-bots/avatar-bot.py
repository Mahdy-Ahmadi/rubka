from rubka.asynco import Robot
import asyncio

bot = Robot("token")

async def main():
    link = await bot.get_avatar_me(save_as=None)
    print("🔗 Link profile Robot : ", link)

asyncio.run(main())
