import asyncio
from rubka.asynco import Robot
from rubka.context import Message

bot = Robot("YOUR_BOT_TOKEN_HERE")

@bot.on_message_group(
    chat_id=["g12345", "g67890"],       # فقط این گروه‌ها
    commands=["start", "help"],         # فقط دستورهای مشخص شده
    filters=lambda msg: "hello" in msg.text.lower() if msg.text else False,  # فقط پیام‌هایی که حاوی "hello" هستند
    sender_id="user_123",               # فقط از این کاربر
    sender_type="admin",                # فقط ادمین‌ها
    allow_forwarded=False,              # پیام‌های فوروارد شده اجازه ندارند
    allow_files=False,                  # فایل اجازه ندارد
    allow_stickers=True,                # استیکر مجاز
    allow_polls=False,                  # نظرسنجی اجازه ندارد
    allow_contacts=True,                # مخاطب مجاز
    allow_locations=False,              # موقعیت مکانی اجازه ندارد
    min_text_length=5,                  # حداقل طول متن ۵ کاراکتر
    max_text_length=50,                 # حداکثر طول متن ۵۰ کاراکتر
    contains="rubika",                  # متن باید شامل "rubika" باشد
    startswith="/",                      # متن باید با / شروع شود
    endswith="!",                        # متن باید با ! تمام شود
    case_sensitive=False                 # بررسی حروف حساس به بزرگ/کوچک بودن نباشد
)
async def handle_group(bot: Robot, message: Message):
    await message.reply(
        f"✅ پیام دریافت شد:\n\n"
        f"متن: {message.text}\n"
        f"از کاربر: {message.sender_id}\n"
        f"در گروه: {message.chat_id}"
    )

# اجرای ربات
asyncio.run(bot.run())
