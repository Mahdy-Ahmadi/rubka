import os, random, json, aiohttp, asyncio
from rubka.asynco import Robot, Message, filters
from asyncio import Lock
from datetime import datetime, timedelta, timezone

bot = Robot("token")
SETTINGS_FILE = "tts_settings.json"

DEFAULT_SETTINGS = {
    "gender": "fa-IR-DilaraNeural",
    "speed": 0,
    "hzn": 0,
    "volume": 10
}

async def load_settings() -> dict:
    async with Lock():
        if not os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump({}, f)
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

async def save_settings(data: dict):
    async with Lock():
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

async def get_user_settings(user_id: str) -> dict:
    settings = await load_settings()
    if user_id not in settings:
        settings[user_id] = DEFAULT_SETTINGS.copy()
        await save_settings(settings)
    return settings[user_id]

async def update_user_setting(user_id: str, key: str, value):
    settings = await load_settings()
    if user_id not in settings:
        settings[user_id] = DEFAULT_SETTINGS.copy()
    settings[user_id][key] = value
    await save_settings(settings)


@bot.on_message(filters.text_contains_any(["/start","راهنما","ربات","صدا","/help"]))
async def start(bot: Robot, message: Message):
    await message.reply(
        f"""🎧 < {await message.name} >

به دنیای صدا خوش اومدی ! 🔊

برای تنظیم صدا از دستورات زیر استفاده کن:

🧍‍♂️ صدای مرد → صدا مرد  
👩 صدای زن → صدا زن  

⚡ تنظیم سرعت → سرعت 1 تا 20  
🎚 تنظیم هرتز → هرتز -100 تا 100  
🔊 ولوم صدا → ولوم 10 تا 100  

📊 نمایش تنظیمات فعلی → وضعیت  

وقتی تنظیمات رو انجام دادی، فقط بنویس:

بگو سلام دنیا  

تا برات ویس بسازه 🎙️"""
    )


@bot.on_message(filters.text_startswith("صدا"))
async def change_voice_type(bot: Robot, message: Message):
    user_id = message.author_guid
    text = message.text.strip()

    if "مرد" in text:
        await update_user_setting(user_id, "gender", "fa-IR-FaridNeural")
        msg = "🔊 صدای مرد (فرید) فعال شد."
    elif "زن" in text:
        await update_user_setting(user_id, "gender", "fa-IR-DilaraNeural")
        msg = "🔊 صدای زن (دلارا) فعال شد."
    else:
        msg = "❌ لطفاً بنویس: صدا مرد یا صدا زن"
    await message.reply(msg)


@bot.on_message(filters.text_startswith("سرعت"))
async def change_speed(bot: Robot, message: Message):
    user_id = message.author_guid
    parts = message.text.split()

    if len(parts) < 2 or not parts[1].isdigit():
        return await message.reply("❌ لطفاً عددی بین 1 تا 20 وارد کن.")

    speed = int(parts[1])
    if not 0 <= speed <= 20:
        return await message.reply("⚠ سرعت باید بین 1 تا 20 باشد.")

    await update_user_setting(user_id, "speed", speed)
    await message.reply(f"✅ سرعت روی {speed} تنظیم شد.")


@bot.on_message(filters.text_startswith("هرتز"))
async def change_hzn(bot: Robot, message: Message):
    user_id = message.author_guid
    parts = message.text.split()

    try:
        hzn = int(parts[1])
    except (IndexError, ValueError):
        return await message.reply("❌ لطفاً عددی بین -100 تا 100 وارد کن.")

    if not -100 <= hzn <= 100:
        return await message.reply("⚠ هرتز باید بین -100 تا 100 باشد.")

    await update_user_setting(user_id, "hzn", hzn)
    await message.reply(f"✅ هرتز روی {hzn} تنظیم شد.")


@bot.on_message(filters.text_startswith("ولوم"))
async def change_volume(bot: Robot, message: Message):
    user_id = message.author_guid
    parts = message.text.split()

    try:
        volume = int(parts[1])
    except (IndexError, ValueError):
        return await message.reply("❌ لطفاً عددی بین 10 تا 100 وارد کن.")

    if not 10 <= volume <= 100:
        return await message.reply("⚠ ولوم صدا باید بین 10 تا 100 باشد.")

    await update_user_setting(user_id, "volume", volume)
    await message.reply(f"✅ ولوم صدا روی {volume} تنظیم شد.")


@bot.on_message(filters.text_startswith("وضعیت"))
async def show_status(bot: Robot, message: Message):
    user_id = message.author_guid
    settings = await get_user_settings(user_id)
    gender = settings["gender"]
    speed = settings["speed"]
    hzn = settings["hzn"]
    volume = settings["volume"]

    iran_time = datetime.now(timezone.utc) + timedelta(hours=3, minutes=30)
    current_time = iran_time.strftime("%H:%M:%S")
    voice_type = "🧍‍♂️ (فرید)" if "Farid" in gender else "👩 (دلارا)"

    await message.reply(
        f"""✨ وضعیت فعلی تنظیمات شما ✨

🏷 نام چت : {await message.author_name}
⏰ ساعت : {current_time}
🎙 نام گوینده : {voice_type}
⚡ سرعت : {speed}
🎚 هرتز : {hzn}
🔊 ولوم صدا : {volume}

📢 برای تغییر از دستورات زیر استفاده کن:
صدا مرد | صدا زن  
سرعت 1 تا 20  
هرتز -100 تا 100  
ولوم 10 تا 100"""
)


@bot.on_message(filters.text_startswith("بگو"))
async def make_voice(bot: Robot, message: Message):
    asyncio.create_task(handle_voice_request(bot, message))


async def handle_voice_request(bot: Robot, message: Message):
    user_id = message.author_guid
    text = message.text.replace("بگو", "").strip()
    if not text:
        return await message.reply("❗ بعد از کلمه «بگو» متنت رو بنویس.")
    
    settings = await get_user_settings(user_id)
    gender = settings["gender"]
    speed = settings["speed"]
    hzn = settings["hzn"]
    try:volume = settings["volume"]
    except:volume = 10

    url = f"https://v3.api-free.ir/TTS/?q={text}&type={gender}&hzn={hzn}&speed={speed}&volume={volume}"
    status_msg = await message.reply("🎙 در حال ساخت ویس... لطفاً صبر کن.")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
        if not data.get("status"):
            return await status_msg.edit("⚠ مشکلی در ساخت ویس پیش اومد.")
        link = data["data"]["download_link"]
        voice_info = data.get("data", {}).get("voice_info", {})
        caption = f"""🎧 ویس شما :

🎙 نام گوینده : {voice_info.get('LocalName', 'نامشخص')}
⚧ جنسیت : {"زن" if voice_info.get("Gender") == "Female" else "مرد"}
🌍 زبان : {voice_info.get('LocaleName', 'نامشخص')}
💠 نوع صدا : {voice_info.get('VoiceType', 'نامشخص')}
🎧 نرخ نمونه‌برداری : {voice_info.get('SampleRateHertz', 'نامشخص')} Hz
🚀 سرعت گفتار : {voice_info.get('WordsPerMinute', 'نامشخص')} کلمه در دقیقه

< {await message.author_name} >"""
        await message.reply_music(link, text=caption)
        await status_msg.delete()
    except Exception as e:
        await status_msg.edit(f"❌ خطا در ساخت ویس:\n{e}")


asyncio.run(bot.run())
