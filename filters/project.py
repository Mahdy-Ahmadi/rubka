import asyncio
from rubka.asynco import Robot, filters
from rubka.context import Message

# توکن ربات خود را اینجا قرار دهید

BOT_TOKEN = "YOUR_BOT_TOKEN"

bot = Robot(BOT_TOKEN)


# 1. دریافت پیام‌های متنی در چت‌های خصوصی
@bot.on_message(filters.is_private & filters.is_text)
async def handle_private_text_message(bot, msg: Message):
    await msg.reply(f"پیام خصوصی شما دریافت شد: '{msg.text}'.")

# 2. دریافت پیام‌های متنی در گروه‌ها و سوپرگروه‌ها
@bot.on_message(filters.chat_type_in(['group']) & filters.is_text)
async def handle_group_text_message(bot, msg: Message):
    # پاسخ فقط در صورتی که پیام یک دستور نباشد
    if not filters.is_command(msg):
        await msg.reply("پیام متنی در گروه دریافت شد.")

# 3. واکنش به دستور /start در هر نوع چتی
@bot.on_message(filters.is_command("start")) # filters.is_command("start") معادل filters.text("/start") است
async def handle_start_command(bot, msg: Message):
    await msg.reply("سلام! به ربات خوش آمدید. از /help برای دیدن دستورات استفاده کنید.")

# 4. واکنش به دستور /help در چت‌های خصوصی
@bot.on_message(filters.is_private & filters.is_command("help"))
async def handle_help_command_private(bot, msg: Message):
    help_text = """
دستورات موجود:
/start - خوش آمدگویی
/help - نمایش این پیام
/info - اطلاعات چت
/send_photo - ارسال یک عکس نمونه
"""
    await msg.reply(help_text)

# 5. نمایش اطلاعات چت در صورت ارسال دستور /info
@bot.on_message(filters.is_command("info"))
async def handle_chat_info(bot, msg: Message):
    chat_id = msg.chat.id
    chat_type = msg.chat.type
    chat_title = msg.chat.title or msg.chat.username or "N/A"
    member_count = msg.chat.members_count if msg.chat.members_count else "N/A"

    await msg.reply(f"**اطلاعات چت:**\n"
                    f"ID: `{chat_id}`\n"
                    f"Type: `{chat_type}`\n"
                    f"Title/Username: `{chat_title}`\n"
                    f"Member Count: `{member_count}`")

# 6. ارسال یک عکس نمونه با استفاده از فیلتر file_extension
@bot.on_message(filters.is_command("send_photo") & filters.is_private)
async def send_sample_photo(bot, msg: Message):
    # فرض کنید یک عکس با نام 'sample.jpg' در کنار فایل ربات شما قرار دارد
    # یا از file_id یک عکس موجود استفاده کنید.
    # برای مثال، از file_id یک عکس موجود استفاده می‌کنیم:
    # اگر از file_id استفاده می‌کنید، آن را اینجا قرار دهید:
    # photo_file_id = "AgACAgIAAxkBAAIB-WV5u-zO_uG_s-hMh_2iJ6t6i8uPAAJ4vDEbKk8iS-5B6yZ_p-lEAQ"
    # await bot.send_photo(msg.chat.id, photo=photo_file_id, caption="این یک عکس نمونه است.")

    # اگر میخواهید خود ربات عکس را آپلود کند (نیاز به مسیر فایل دارد):
    try:
        # برای تست، فرض می‌کنیم عکس sample.jpg در همان پوشه ربات باشد
        await bot.send_photo(msg.chat.id, photo="sample.jpg", caption="این یک عکس نمونه است.")
    except FileNotFoundError:
        await msg.reply("فایل `sample.jpg` پیدا نشد. لطفا آن را در پوشه ربات قرار دهید یا file_id صحیح را وارد کنید.")
    except Exception as e:
        await msg.reply(f"خطا در ارسال عکس: {e}")


# 7. واکنش به پیام‌های فوروارد شده از چت‌های خصوصی
@bot.on_message(filters.is_forwarded & filters.is_private)
async def handle_forwarded_from_private(bot, msg: Message):
    # بررسی می‌کنیم که منبع فوروارد هم یک کاربر بوده است
    if msg.forward_from and filters.is_user(msg.forward_from):
        await msg.reply(f"این پیام از کاربر {msg.forward_from.first_name} فوروارد شده است.")
    else:
        await msg.reply("یک پیام فوروارد شده از یک چت خصوصی دریافت شد.")

# 8. واکنش به فایل‌های صوتی (MP3) در هر نوع چتی
@bot.on_message(filters.is_file & filters.file_extension(".mp3"))
async def handle_mp3_files(bot, msg: Message):
    await msg.reply("یک فایل صوتی MP3 دریافت شد.")

# 9. واکنش به پیام‌های متنی که دقیقا "بله" یا "خیر" هستند
@bot.on_message(filters.text_equals("بله") | filters.text_equals("خیر"))
async def handle_yes_no(bot, msg: Message):
    await msg.reply(f"شما پاسخ دادید: {msg.text}")

# 10. واکنش به پیام‌های متنی که حاوی اعداد 10 رقمی هستند (به عنوان شماره تلفن)
@bot.on_message(filters.text_regex(r"\d{10}"))
async def handle_10_digit_number(bot, msg: Message):
    await msg.reply("این پیام حاوی یک شماره 10 رقمی است.")

# 11. واکنش به فایل‌های با حجم کمتر از 100 کیلوبایت
@bot.on_message(filters.is_file & filters.file_size_lt(100 * 1024))
async def handle_small_files(bot, msg: Message):
    await msg.reply("فایل ارسالی شما حجمی کمتر از 100KB دارد.")

# 12. خوش‌آمدگویی در گروه‌هایی که بیش از 500 عضو دارند
@bot.on_message(filters.is_group & filters.chat_member_count_gt(500))
async def handle_large_groups_welcome(bot, msg: Message):
    await msg.reply("سلام! به این گروه بزرگ خوش آمدید!")

# 13. پردازش پیام‌هایی که دقیقا "rubka" هستند و از کاربر خصوصی ارسال شده‌اند
@bot.on_message(filters.is_private & filters.text_equals("rubka"))
async def handle_rubka_command_private(bot, msg: Message):
    await msg.reply("شما با کتابخانه Rubka کار می‌کنید!")

# 14. واکنش به پیام‌های حاوی استیکر
@bot.on_message(filters.is_sticker)
async def handle_any_sticker(bot, msg: Message):
    await msg.reply("یک استیکر زیبا دریافت شد!")

# 15. واکنش به پیام‌هایی که فوروارد شده‌اند و از کانال آمده‌اند
@bot.on_message(filters.is_forwarded & filters.is_channel)
async def handle_forwarded_from_channel(bot, msg: Message):
    await msg.reply("این پیام از یک کانال فوروارد شده است.")


# --- اجرای ربات ---
if __name__ == "__main__":
    print("ربات در حال اجراست...")
    asyncio.run(bot.run())
