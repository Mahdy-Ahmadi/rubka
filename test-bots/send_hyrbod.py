import asyncio
from rubka.asynco import Robot,Message

bot = Robot("")

@bot.on_message(commands=['start'])
async def handle_start(bot: Robot, message: Message):
    sent = await message.reply("سلام") #ارسال پیام

    await asyncio.sleep(3) #انتظار سه ثانیه ای
    await sent.edit("پیام ادیت شد") #ادیت پیام ارسال شده

    await asyncio.sleep(3)# انتظار سه ثانیه ای
    await sent.delete() # حذف پیام ارسال شده

asyncio.run(bot.run())
