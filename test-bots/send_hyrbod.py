from rubka.asynco import Robot,Message,filters
import asyncio

bot = Robot("")

@bot.on_message(filters.is_command.start) #شروع با ارسال کامند استارت
async def handle_start(bot: Robot, message: Message):
    sent = await message.reply("سلام") #ارسال پیام

    await asyncio.sleep(3) #انتظار سه ثانیه ای
    await sent.edit("پیام ادیت شد") #ادیت پیام ارسال شده

    await asyncio.sleep(3)# انتظار سه ثانیه ای
    await sent.delete() # حذف پیام ارسال شده

bot.run()
