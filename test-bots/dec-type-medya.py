import asyncio
from rubka.asynco import Robot
from rubka.context import Message

bot = Robot("TOKEN")

@bot.on_message_text()
async def handle_text(bot: Robot, message: Message):
    await message.reply("📩 این یک پیام متنی است.")

@bot.on_message_file()
async def handle_file(bot: Robot, message: Message):
    await message.reply("📂 این یک فایل است.")
@bot.on_message_forwarded()
async def handle_forward(bot: Robot, message: Message):
    await message.reply("🔁 این پیام فرواردی است.")
@bot.on_message_reply()
async def handle_reply(bot: Robot, message: Message):
    await message.reply("↩️ این پیام ریپلای است.")
@bot.on_message_media()
async def handle_media(bot: Robot, message: Message):
    await message.reply("🖼️ این پیام شامل مدیا است.")
@bot.on_message_sticker()
async def handle_sticker(bot: Robot, message: Message):
    await message.reply("😊 این یک استیکر است.")
@bot.on_message_contact()
async def handle_contact(bot: Robot, message: Message):
    await message.reply("📞 این یک پیام کانتکت است.")
@bot.on_message_location()
async def handle_location(bot: Robot, message: Message):
    await message.reply("📍 این یک لوکیشن است.")
@bot.on_message_poll()
async def handle_poll(bot: Robot, message: Message):
    await message.reply("📊 این یک نظرسنجی است.")

if __name__ == "__main__":
    asyncio.run(bot.run())
