from rubka import Robot
from rubka.context import Message
from rubka.keypad import ChatKeypadBuilder
import json, os, subprocess, sys


bot = Robot("token")


try:
    import psutil
except ImportError:
    print("pip install psutil")
    exit(1)

BOT_DATA_FILE = "bots_data.json"
if not os.path.exists(BOT_DATA_FILE):
    with open(BOT_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

def load_bots():
    with open(BOT_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_bots(data):
    with open(BOT_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

bots = load_bots()
if not os.path.exists("bots"):
    os.makedirs("bots")
keypad_start = (
    ChatKeypadBuilder()
    .row(ChatKeypadBuilder().button("activate_bot", "🤖 فعال‌سازی ربات"))
    .row(ChatKeypadBuilder().button("bot_status", "📊 وضعیت ربات"))
    .row(ChatKeypadBuilder().button("disable_bot", "❌ غیرفعال‌سازی ربات"))
    .build()
)
for uid, info in bots.items():
    if info.get("active"):
        user_bot_file = f"bots/bot_{uid}.py"
        if os.path.exists(user_bot_file):
            process = subprocess.Popen([sys.executable, user_bot_file])
            bots[uid]["pid"] = process.pid
save_bots(bots)



def mask_token(token, hide_len=8):
    if len(token) <= hide_len + 4:
        return "*" * len(token)
    start = token[: (len(token) - hide_len) // 2]
    end = token[(len(token) + hide_len) // 2 :]
    return start + ("*" * hide_len) + end

def main_keypad(has_bot_active: bool):
    kb = ChatKeypadBuilder()
    kb.row(kb.button("activate_bot", "🤖 فعال‌سازی ربات"))
    kb.row(kb.button("bot_status", "📊 وضعیت ربات"))
    if has_bot_active:
        kb.row(kb.button("disable_bot", "❌ غیرفعال‌سازی ربات"))
    return kb.build()

@bot.on_message()
def panel_handler(bot: Robot, message: Message):
    user_id = str(message.sender_id)
    text = message.text or ""
    bots = load_bots()
    data = getattr(message.aux_data, "button_id", None)
    has_bot = user_id in bots and bots[user_id].get("active")

    if text == "/start" or text == "":
        return message.reply_keypad(
            "سلام 👋\nاز دکمه‌های زیر برای مدیریت ربات خود استفاده کنید:",
            keypad=main_keypad(has_bot),
        )

    if data == "activate_bot":
        if has_bot:
            return message.reply("⛔ شما قبلاً یک ربات فعال دارید.")
        else:
            return message.reply("لطفاً توکن ربات روبیکای خود را ارسال کنید:")

    if data == "bot_status":
        user_bot = bots.get(user_id)
        if user_bot:
            status = "فعال ✅" if user_bot.get("active") else "غیرفعال ❌"
            me_info = Robot(user_bot['token']).get_me()
            if me_info.get("status") == "OK":
                bot_data = me_info.get("data", {}).get("bot", {})
                bot_title = bot_data.get("bot_title", "نامشخص")
                bot_id = bot_data.get("bot_id", "نامشخص")
                username = bot_data.get("username", "نامشخص")
                description = bot_data.get("description", "ندارد")
                start_message = bot_data.get("start_message", "ندارد")
                share_url = bot_data.get("share_url", "ندارد")
            else:
                bot_title = bot_id = username = description = start_message = share_url = "اطلاعات در دسترس نیست"

            status_text = "فعال ✅" if user_bot.get("active") else "غیرفعال ❌"

            text = (
                f"🤖 اطلاعات ربات شما:\n\n"
                f"توکن: {mask_token(user_bot['token'])}\n"
                f"وضعیت: {status_text}\n\n"
                f"نام ربات: {bot_title}\n"
                f"شناسه ربات: {bot_id}\n"
                f"نام کاربری: @{username}\n"
                f"توضیحات: {description}\n"
                f"پیام شروع: {start_message}\n"
                f"لینک اشتراک: {share_url}\n\n"
                f"برای بازگشت به منوی اصلی، /start را ارسال کنید."
            )
            return message.reply(text)
        else:
            return message.reply("⛔ شما هیچ ربات فعالی ندارید.")

    if data == "disable_bot":
        if has_bot:
            pid = bots[user_id].get("pid")
            if pid:
                try:
                    p = psutil.Process(pid)
                    p.terminate()
                    p.wait(timeout=5)
                except Exception as e:
                    print(f"خطا در بستن پروسس ربات کاربر {user_id}: {e}")

            bots[user_id]["active"] = False
            save_bots(bots)
            return message.reply_keypad("❌ ربات شما با موفقیت غیرفعال شد.",main_keypad(has_bot))
        else:
            return message.reply("⛔ شما هیچ ربات فعالی ندارید.")

    if text.startswith("B"):
        if has_bot:
            return message.reply("⛔ شما قبلاً یک ربات فعال دارید. برای غیرفعال‌سازی از دکمه مربوطه استفاده کنید.")
        bots[user_id] = {
            "token": text.strip(),
            "active": True
        }
        save_bots(bots)

        if not os.path.exists("bots"):
            os.makedirs("bots")
        user_bot_file = f"bots/bot_{user_id}.py"

        with open(user_bot_file, "w", encoding="utf-8") as f:
            f.write(create_user_bot_code(text.strip()))

        process = subprocess.Popen([sys.executable, user_bot_file])
        bots[user_id]["pid"] = process.pid
        save_bots(bots)

        return message.reply_keypad("✅ ربات شما با موفقیت راه‌اندازی شد.\n\nبرای مشاهده وضعیت، دکمه «وضعیت ربات» را بزنید.",keypad_start)

def create_user_bot_code(token: str) -> str:
    return f'''
from rubka import Robot
from rubka.context import Message
import requests

bot = Robot(token="{token}")

@bot.on_message()
def message_handler(bot, message: Message):
    user_id = message.sender_id
    text = message.text or ""

    if text == "/start":
        return message.reply("سلام! 👋\\nلطفاً لینک پست روبینو را بفرستید:")

    if text.startswith("https://rubika.ir/post/"):
        try:
            res = requests.get("https://api-free.ir/api/rubino-dl.php?url=" + text).json()
            if not res.get("ok"):
                return message.reply("❌ خطا در دریافت اطلاعات.")
            r = res["result"]
            return message.reply_image(
                path=r["thumb"],
                text=f"❤️ لایک: {{r['like']}}\\n💬 نظر: {{r['comment']}}\\n👀 بازدید: {{r['view']}}\\n\\n🎬 دانلود مستقیم: {{r['url']}}"
            )
        except Exception as e:
            return message.reply(f"⚠️ خطا: {{e}}")

    else:
        return message.reply("⛔ لطفاً یک لینک معتبر روبینو بفرستید که با https://rubika.ir/post/ شروع شود.")

bot.run()
'''

bot.run()
