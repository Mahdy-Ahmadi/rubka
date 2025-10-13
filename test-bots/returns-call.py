import asyncio
from rubka.asynco import Robot,Message

bot = Robot("")

@bot.on_message(commands=['start'])
async def handle_start(bot: Robot, message: Message):
    name = await message.name #دریافت نام
    info = await message.author_info # دریافت اطلاعات شخص
    await message.reply(f"your Name : {name}",delete_after=10) # ورودی delete_after برای حذف خودکار
    await message.reply(f"your info : {info}",delete_after=9) # ورودی delete_after برای حذف خودکار

asyncio.run(bot.run())
