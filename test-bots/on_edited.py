import asyncio
from rubka.asynco import Robot, Message

max_msg = 100 #فیلتر زمان پیام های قدیمی (ممکنه بعد از ران کردن مجدد پیام های قبلی رو هم دریافت کنه)

bot = Robot("",max_msg_age=max_msg)

@bot.on_edited_message()
async def on_message_edit(_: Robot, message: Message):
    await message.reply("✏️ پیام شما ویرایش شد.")

@bot.on_message()
async def on_new_message(_: Robot, message: Message):
    if not message.is_edited:
        await message.reply("✅ پیام شما دریافت شد.")

asyncio.run(bot.run())
