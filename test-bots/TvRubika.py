import asyncio
from rubka import TvRubika

AUTH_TOKEN = "auth" #m.rubika.ir

async def main():
    async with TvRubika(AUTH_TOKEN) as bot:
        account_info = await bot.get_me()
        print(account_info)
        search_results = await bot.search_video("مرد عنکبوتی")
        print(search_results)

asyncio.run(main())
