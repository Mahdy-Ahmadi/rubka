from rubka import Robot
from rubka.context import Message
from collections import deque
from datetime import datetime, timedelta
import json

bot = Robot(token="0.")

waiting = deque()
active_chats = {}
online_users = {}
started_users = set()
user_status = {}
user_gender = {}
reported_users = {}

LOG_FILE = "chat_logs.json"
INACTIVITY = timedelta(minutes=5)

# ابزارهای کاربردی
def store_json(type_, sender, receiver, content):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": type_,
        "from": sender,
        "to": receiver,
        "content": content
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def update_activity(uid):
    online_users[uid] = datetime.now()

def cleanup_inactive():
    now = datetime.now()
    for uid, last in list(online_users.items()):
        if now - last > INACTIVITY:
            online_users.pop(uid, None)
            peer = active_chats.pop(uid, None)
            if peer:
                active_chats.pop(peer, None)
                set_status(peer, "idle")
                bot.send_message(peer, "⚠️ طرف مقابل غیرفعال شد.")
                store_json("disconnect", peer, uid, "partner inactive")

def set_status(uid, status):
    user_status[uid] = status

def get_status(uid):
    return user_status.get(uid, "idle")

# پیام‌های ورودی
@bot.on_message()
def handle(bot: Robot, msg: Message):
    uid = str(msg.chat_id)
    update_activity(uid)
    cleanup_inactive()
    peer = active_chats.get(uid)

    if msg.text and msg.text.strip() == "/start":
        started_users.add(uid)
        set_status(uid, "idle")

        rows = [
            {"buttons": [{"id": "random", "type": "Simple", "button_text": "اتصال تصادفی"}]},
            {"buttons": [{"id": "online", "type": "Simple", "button_text": "نمایش آنلاین‌ها"}]},
            {"buttons": [{"id": "gender", "type": "Simple", "button_text": "تنظیم جنسیت"}]}
        ]
        if peer:
            rows.append({"buttons": [{"id": "exit", "type": "Simple", "button_text": "خروج از چت"}]})
            rows.append({"buttons": [{"id": "report", "type": "Simple", "button_text": "ریپورت کاربر"}]})

        bot.send_message(
            uid,
            "🤖 خوش آمدی! یکی از گزینه‌ها رو انتخاب کن:",
            chat_keypad_type="New",
            chat_keypad={
                "rows": rows,
                "resize_keyboard": True,
                "on_time_keyboard": False
            }
        )
        store_json("command", uid, None, "/start")
        return

    # انتقال پیام یا فایل
        # انتقال پیام یا تصویر
    if msg.text == "/exit":
            if peer:
                active_chats.pop(uid, None)
                active_chats.pop(peer, None)
                set_status(uid, "idle")
                set_status(peer, "idle")
                bot.send_message(uid, "✅ شما از چت خارج شدید.")
                bot.send_message(peer, "❌ طرف مقابل چت را ترک کرد.")
                store_json("exit", uid, peer, "/exit")
            else:
                bot.send_message(uid, "❌ شما در هیچ چتی نیستید.")
            return
    if peer:
        print(peer)
        if msg.text:
            bot.send_message(peer, msg.text.strip())
            store_json("message", uid, peer, msg.text.strip())
        
        elif msg.file:
            file_name = msg.file.file_name.lower()
            file_id = msg.file.file_id

            if file_name.endswith((".jpg", ".jpeg", ".png", ".webp", ".bmp")):
                rows = [
            {"buttons": [{"id": "random", "type": "Simple", "button_text": "اتصال تصادفی"}]},
            {"buttons": [{"id": "online", "type": "Simple", "button_text": "نمایش آنلاین‌ها"}]},
            {"buttons": [{"id": "gender", "type": "Simple", "button_text": "تنظیم جنسیت"}]}
        ]
                print(bot.send_image(peer, file_id=file_id,chat_keypad=rows,chat_keypad_type="New",file_name="as.jpg"))
                store_json("image", uid, peer, file_name)
            else:
                bot.send_message(uid, "❌ فقط فایل‌های تصویری (jpg/png/...) قابل ارسال هستند.")
                store_json("invalid_file", uid, None, file_name)



# هندل کردن دکمه‌ها
@bot.on_callback()
def callback_handler(bot: Robot, message: Message):
    uid = str(message.chat_id)
    data = message.aux_data.button_id
    peer = active_chats.get(uid)

    update_activity(uid)
    cleanup_inactive()

    if data == "random":
        if uid not in waiting:
            waiting.append(uid)
            set_status(uid, "waiting")
            message.reply("⌛️ در صف اتصال هستی...")

        while len(waiting) >= 2:
            u1, u2 = waiting.popleft(), waiting.popleft()
            active_chats[u1] = u2
            active_chats[u2] = u1
            set_status(u1, "chatting")
            set_status(u2, "chatting")
            bot.send_message(u1, "✅ چت بین شما آغاز شد! برای خروج: /exit")
            bot.send_message(u2, "✅ چت بین شما آغاز شد! برای خروج: /exit")
            store_json("connected", u1, u2, "random_match")

    elif data == "online":
        users = [u for u in online_users if u != uid and u not in active_chats]
        if users:
            rows = [{"buttons": [{"id": f"connect:{u}", "type": "Simple", "button_text": f"اتصال به {u}"}]} for u in users]
            bot.send_message(
                uid,
                f"🟢 کاربران آنلاین ({len(users)} نفر):",
                chat_keypad_type="New",
                chat_keypad={"rows": rows, "resize_keyboard": True, "on_time_keyboard": False}
            )
        else:
            message.reply("⚠️ کسی آنلاین نیست.")
        store_json("command", uid, None, {"online_list": users})

    elif data.startswith("connect:"):
        target = data.replace("connect:", "")
        if target == uid:
            message.reply("❌ نمی‌تونی با خودت چت کنی.")
        elif target not in online_users:
            message.reply("❌ کاربر آفلاین است.")
        elif target in active_chats:
            message.reply("❌ کاربر مشغول است.")
        else:
            active_chats[uid] = target
            active_chats[target] = uid
            set_status(uid, "chatting")
            set_status(target, "chatting")
            message.reply("✅ به طرف مقابل وصل شدید!")
            bot.send_message(target, "✅ یک نفر به شما وصل شد!")
            store_json("connected", uid, target, "manual_match")

    elif data == "gender":
        bot.send_message(uid, "جنسیت خود را انتخاب کن:", chat_keypad_type="New", chat_keypad={
            "rows": [
                {"buttons": [{"id": "gender:مرد", "type": "Simple", "button_text": "🧔 مرد"}]},
                {"buttons": [{"id": "gender:زن", "type": "Simple", "button_text": "👩 زن"}]}
            ],
            "resize_keyboard": True,
            "on_time_keyboard": False
        })

    elif data.startswith("gender:"):
        gender = data.split("gender:")[1]
        user_gender[uid] = gender
        message.reply(f"✅ جنسیت شما تنظیم شد به: {gender}")
        store_json("gender_set", uid, None, gender)

    elif data == "report" and peer:
        reported_users.setdefault(peer, []).append(uid)
        message.reply("❗️ کاربر مقابل گزارش شد.")
        store_json("report", uid, peer, "user_reported")

    elif data == "exit" or data == "/exit":
        if peer:
            active_chats.pop(uid, None)
            active_chats.pop(peer, None)
            set_status(uid, "idle")
            set_status(peer, "idle")
            bot.send_message(peer, "❌ طرف مقابل گفت‌وگو را ترک کرد.")
            message.reply("✅ خارج شدید.")
            store_json("exit", uid, peer, "chat_ended")
        else:
            message.reply("❌ در چتی نیستی.")

    else:
        message.reply(f"⚠️ دکمه ناشناخته: {data}")

# اجرای ربات
if __name__ == "__main__":
    print("🤖 ربات با دکمه‌های callback اجرا شد!")
    bot.run()
