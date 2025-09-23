import asyncio
from rubka.asynco import Robot, filters, Message

bot = Robot("")

admin_id: str | None = None


@bot.on_message_group(filters=filters.text_regex(r"(https?://|www\.|\.ir|\.com|\.net|t\.me|@\w+)") & filters.text_contains_any(["https","http", "@"]))
async def handle_start(bot: Robot, message: Message):
    if admin_id is not None and message.sender_id == admin_id:
        return
    print(await message.delete())


@bot.on_message_group(filters=filters.is_command.set_admin)
async def set_admin(_: Robot, message: Message):
    global admin_id
    if admin_id is None:
        admin_id = message.sender_id
        await message.reply("✅ شما به عنوان ادمین ربات تنظیم شدید")
    else:
        await message.reply("⚠️ قبلاً یک ادمین برای ربات تنظیم شده است!")


asyncio.run(bot.run())
