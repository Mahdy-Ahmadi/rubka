import subprocess, sys,asyncio, json, aiohttp
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "rubka"])
from rubka.asynco import Robot, Message, filters

bot = Robot("token")
DATA_FILE = "group_locks.json"


locks_fa = {
    "لینک": "links",
    "عکس": "photo",
    "ویدیو": "video",
    "صوت": "audio",
    "ویس": "voice",
    "استیکر": "stickers",
    "فایل": "document",
    "آرشیو": "archive",
    "اجرایی": "executable",
    "فونت": "font",
    "نظرسنجی": "polls",
    "کانتکت": "contacts",
    "لوکیشن": "locations",
    "فوروارد": "forwarded"
}
default_locks = {v: False for v in locks_fa.values()}

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = load_data()



@bot.on_message_group(filters=filters.text_equals("تنظیم ادمین"))
async def set_admin(_: Robot, message: Message):
    chat_id = message.chat_id
    chat_data = data.get(chat_id, {"locks": default_locks.copy(), "talker": False})
    if "admin" not in chat_data:
        chat_data["admin"] = message.sender_id
        data[chat_id] = chat_data
        save_data(data)
        await message.reply("✅ شما به عنوان ادمین گروه انتخاب شدید!")
    else:
        await message.reply("⚠️ ادمین قبلی هنوز فعال است!")

@bot.on_message_group(filters=filters.text_equals("حذف ادمین"))
async def remove_admin(_: Robot, message: Message):
    chat_id = message.chat_id
    chat_data = data.get(chat_id)
    if not chat_data or "admin" not in chat_data:
        await message.reply("⚠️ هیچ ادمینی برای گروه تنظیم نشده است!")
        return
    if message.sender_id != chat_data["admin"]:
        await message.reply("❌ فقط ادمین فعلی می‌تواند این کار را انجام دهد!")
        return
    del chat_data["admin"]
    data[chat_id] = chat_data
    save_data(data)
    await message.reply("✅ ادمین گروه با موفقیت حذف شد!")


@bot.on_message_group(
    filters=(filters.text_equals("راهنما") |
             filters.is_command.start |
             filters.is_command.help |
             filters.is_command.Start |
             filters.is_command.bot)
)
async def help_command(_: Robot, message: Message):
    chat_name = await bot.get_name(message.chat_id)
    help_text = f"📌 {chat_name} - راهنمای مدیریت قفل‌های گروه 📌\n\n"
    help_text += "✨ برای مشاهده وضعیت قفل‌ها: وضعیت\n"
    help_text += "✨ برای قفل کردن یک مورد: قفل <نام قفل>\n"
    help_text += "✨ برای باز کردن یک مورد: باز <نام قفل>\n"
    help_text += "✨ برای روشن کردن سخنگو: سخنگو روشن\n"
    help_text += "✨ برای خاموش کردن سخنگو: سخنگو خاموش\n\n"
    help_text += "🔹 لیست قفل‌ها:\n"
    for fa_name in locks_fa.keys():
        help_text += f"   • {fa_name}\n"
    help_text += "\n⚠️ فقط ادمین می‌تواند قفل‌ها و سخنگو را مدیریت کند."
    await message.reply(help_text)



@bot.on_message_group()
async def lock_commands(bot: Robot, message: Message):
    chat_id = message.chat_id
    chat_data = data.get(chat_id, {"locks": default_locks.copy(), "talker": False})
    admin_id = chat_data.get("admin")
    if message.sender_id != admin_id:
        return

    text = (message.text or "").strip()

    
    if text == "وضعیت":
        status_text = "📌 وضعیت قفل‌های گروه 📌\n\n"
        for fa_name, key in locks_fa.items():
            status_text += f"🔹 {fa_name}: {'🔒 بسته' if chat_data['locks'].get(key) else '🔓 باز'}\n"
        status_text += f"🔹 سخنگو: {'✅ روشن' if chat_data.get('talker') else '❌ خاموش'}\n"
        status_text += "\n✨ برای قفل کردن: قفل <نام قفل>\n✨ برای باز کردن: باز <نام قفل>"
        await message.reply(status_text)
        return

    
    if text == "سخنگو روشن":
        chat_data["talker"] = True
        data[chat_id] = chat_data
        save_data(data)
        await message.reply("✅ سخنگو روشن شد!")
        return
    elif text == "سخنگو خاموش":
        chat_data["talker"] = False
        data[chat_id] = chat_data
        save_data(data)
        await message.reply("❌ سخنگو خاموش شد!")
        return

    
    for fa_name, key in locks_fa.items():
        if text.startswith(f"قفل {fa_name}"):
            chat_data["locks"][key] = True
            data[chat_id] = chat_data
            save_data(data)
            await message.reply(f"🔒 {fa_name} با موفقیت قفل شد!")
            return
        elif text.startswith(f"باز {fa_name}"):
            chat_data["locks"][key] = False
            data[chat_id] = chat_data
            save_data(data)
            await message.reply(f"🔓 {fa_name} با موفقیت باز شد!")
            return



@bot.on_message_group()
async def group_message_handler(bot: Robot, message: Message):
    chat_id = message.chat_id
    chat_data = data.get(chat_id)
    if not chat_data:
        return

    admin_id = chat_data.get("admin")
    if message.sender_id == admin_id:
        return

    locks = chat_data.get("locks", default_locks)

    
    checks = {
        "links": "has_link",
        "media": "is_media",
        "files": "file",
        "stickers": "sticker",
        "polls": "poll",
        "contacts": "contact_message",
        "locations": ["location", "live_location"],
        "forwarded": "is_forwarded"
    }

    for key, attr in checks.items():
        if isinstance(attr, list):
            if any(getattr(message, a, None) for a in attr) and locks.get(key):
                await message.delete()
                return
        else:
            if getattr(message, attr, None) and locks.get(key):
                await message.delete()
                return

    
    media_types = ["photo", "video", "audio", "voice", "document", "archive", "executable", "font"]
    for mtype in media_types:
        if locks.get(mtype) and getattr(message, f"is_{mtype}", False):
            await message.delete()
            return

    
    if chat_data.get("talker"):
        text = message.text or ""
        if text:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(f"https://api.rubka.ir/ans/?text={text}") as resp:
                        if resp.status == 200:
                            result = await resp.json()
                            response = result.get("response")
                            if response:
                                await message.reply(response)
                except Exception:
                    pass



asyncio.run(bot.run(sleep_time=0.1))
