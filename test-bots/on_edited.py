import asyncio
from rubka.asynco import Robot, Message

# ساخت ربات با توکن
bot = Robot("")

# هندلر برای پیام‌های ادیت شده
@bot.on_edited_message()
async def on_message_edit(_: Robot, message: Message):
    await message.reply("✏️ پیام شما ویرایش شد.")

# هندلر برای پیام‌های معمولی
@bot.on_message()
async def on_new_message(_: Robot, message: Message):
    if not message.is_edited:
        await message.reply("✅ پیام شما دریافت شد.")

# اجرای ربات
if __name__ == "__main__":
    asyncio.run(bot.run())
