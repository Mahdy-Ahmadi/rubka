import asyncio
from rubka.asynco import Robot, Message

bot = Robot("")

bot.start_save_message() #این متود به معنای شروع شنود پیام ها توسط ربات هست برای استفاده داخل متود گت مسیج

@bot.on_message()
async def info(bot: Robot, message: Message):
    if message.text == "info":
        data = await bot.get_message(message.chat_id, message.reply_to_message_id or message.message_id) #متود گت مسیج
        await message.reply(f"{data}")

asyncio.run(bot.run())
