import asyncio
from rubka.asynco import Robot
from rubka.context import Message
from rubka.keypad import ChatKeypadBuilder
from collections import deque, defaultdict
from datetime import datetime, timedelta
import json
import os

bot = Robot(token="token")
# چت ایدی ادمین
ADMIN_ID = "b0HJtFl0Dx60230306be5dd14a713977"

DB_FILE = "user_data.json"
LOG_FILE = "chat_logs.json"

BAN_DURATION = timedelta(hours=1)
REPORT_THRESHOLD = 3
ONLINE_THRESHOLD = timedelta(minutes=5)
DB = {
    "waiting_random": deque(),
    "waiting_gender": {"male": deque(), "female": deque()},
    "active_chats": {},
    "online_users": {},
    "user_info": defaultdict(lambda: {
        "status": "idle",
        "gender": None,
        "report_count": 0,
        "reported_by": set(),
        "is_banned": False,
        "admin_state": "none" 
    })
}


BTN_RANDOM_CHAT = "🎲 اتصال تصادفی"
BTN_GENDER_SEARCH = "👫 جستجو بر اساس جنسیت"
BTN_SET_GENDER = "⚙️ تنظیم جنسیت"
BTN_ONLINE_COUNT = "📊 تعداد آنلاین"
BTN_CANCEL_SEARCH = "✖️ لغو جستجو"
BTN_EXIT_CHAT = "❌ خروج از چت"
BTN_REPORT_USER = "❗️ ریپورت کاربر"
BTN_MALE = "🧔 مرد"
BTN_FEMALE = "👩 زن"
BTN_BACK = "⬅️ بازگشت"

BTN_ADMIN_STATS = "📊 آمار کاربران"
BTN_ADMIN_BROADCAST = "📣 پیام همگانی"
BTN_ADMIN_BAN = "🚫 بن کردن کاربر"
BTN_ADMIN_UNBAN = "✅ آنبن کردن کاربر"



def save_db():
    serializable_info = {}
    for uid, info in DB["user_info"].items():
        info_copy = info.copy()
        info_copy["reported_by"] = list(info.get("reported_by", []))
        serializable_info[uid] = info_copy
        
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(serializable_info, f, ensure_ascii=False, indent=4)

def load_db():
    """اطلاعات کاربران را از فایل JSON بارگذاری می‌کند."""
    if not os.path.exists(DB_FILE):
        return
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            user_data = json.load(f)
            for uid, info in user_data.items():
                info["reported_by"] = set(info.get("reported_by", []))
                DB["user_info"][uid] = info
        except json.JSONDecodeError:
            print("خطا: فایل پایگاه داده خالی یا خراب است.")

async def store_log(log_type: str, sender: str, receiver: str = None, content: str = ""):
    """لاگ‌ها را در فایل متنی ذخیره می‌کند."""
    entry = {
        "timestamp": datetime.now().isoformat(), "type": log_type,
        "from": sender, "to": receiver, "content": content
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def update_activity(uid: str):
    """زمان آخرین فعالیت کاربر را به‌روز می‌کند."""
    DB["online_users"][uid] = datetime.now()

def get_online_users_count() -> int:
    """تعداد کاربران آنلاین در دقایق اخیر را برمی‌گرداند."""
    now = datetime.now()
    online_count = sum(1 for last_seen in DB["online_users"].values() if now - last_seen < ONLINE_THRESHOLD)
    return online_count

async def send_main_menu(uid: str, text: str):
    """منوی اصلی را بر اساس وضعیت کاربر ارسال می‌کند."""
    user_info = DB["user_info"][uid]
    status = user_info["status"]
    
    builder = ChatKeypadBuilder()
    
    if status == "chatting":
        builder.row(builder.button(id="exit", text=BTN_EXIT_CHAT), builder.button(id="report", text=BTN_REPORT_USER))
    elif status.startswith("waiting"):
        builder.row(builder.button(id="cancel", text=BTN_CANCEL_SEARCH))
    else: 
        builder.row(builder.button(id="random", text=BTN_RANDOM_CHAT), builder.button(id="gender", text=BTN_GENDER_SEARCH))
        builder.row(builder.button(id="set_gender", text=BTN_SET_GENDER), builder.button(id="online", text=BTN_ONLINE_COUNT))

    main_keypad = builder.build(resize_keyboard=True)
    await bot.send_message(uid, text, chat_keypad=main_keypad)

async def connect_users(u1: str, u2: str):
    DB["active_chats"][u1] = u2
    DB["active_chats"][u2] = u1
    DB["user_info"][u1]["status"] = "chatting"
    DB["user_info"][u2]["status"] = "chatting"

    await send_main_menu(u1, "✅ چت شروع شد! پیام شما به طرف مقابل ارسال می‌شود.")
    await send_main_menu(u2, "✅ چت شروع شد! پیام شما به طرف مقابل ارسال می‌شود.")
    await store_log("connect", u1, u2)

async def disconnect_users(uid: str, reason_for_peer: str, text_for_user: str = "✅ شما از چت خارج شدید."):
    peer = DB["active_chats"].pop(uid, None)
    if peer:
        DB["active_chats"].pop(peer, None)
        DB["user_info"][peer]["status"] = "idle"
        await send_main_menu(peer, reason_for_peer)

    DB["user_info"][uid]["status"] = "idle"
    await send_main_menu(uid, text_for_user)
    await store_log("disconnect", uid, peer, reason_for_peer)


async def try_match_random():
    while len(DB["waiting_random"]) >= 2:
        u1 = DB["waiting_random"].popleft()
        u2 = DB["waiting_random"].popleft()
        await connect_users(u1, u2)

async def try_match_gender():
    male_q = DB["waiting_gender"]["male"]
    female_q = DB["waiting_gender"]["female"]
    while male_q and female_q:
        u_male = male_q.popleft()
        u_female = female_q.popleft()
        await connect_users(u_male, u_female)



async def send_admin_panel(uid: str):
    """منوی اصلی پنل ادمین را ارسال می‌کند."""
    builder = ChatKeypadBuilder()
    builder.row(builder.button(id="admin_stats", text=BTN_ADMIN_STATS))
    builder.row(builder.button(id="admin_broadcast", text=BTN_ADMIN_BROADCAST))
    builder.row(builder.button(id="admin_ban", text=BTN_ADMIN_BAN), builder.button(id="admin_unban", text=BTN_ADMIN_UNBAN))
    builder.row(builder.button(id="back", text=BTN_BACK))
    
    admin_keypad = builder.build(resize_keyboard=True)
    await bot.send_message(uid, "پنل مدیریت ربات:", chat_keypad=admin_keypad)

async def handle_admin_command(bot: Robot, msg: Message, text: str):
    """دستورات ادمین را پردازش می‌کند."""
    uid = str(msg.chat_id)
    admin_info = DB["user_info"][uid]

    if admin_info["admin_state"] == "awaiting_broadcast_message":
        admin_info["admin_state"] = "none"
        await msg.reply("⏳ در حال ارسال پیام همگانی...")
        all_users = list(DB["user_info"].keys())
        success_count = 0
        fail_count = 0
        for user_id in all_users:
            try:
                await bot.send_message(user_id, text)
                success_count += 1
            except Exception as e:
                fail_count += 1
                print(f"خطا در ارسال پیام به {user_id}: {e}")
        await msg.reply(f"✅ پیام همگانی به {success_count} کاربر ارسال شد.\n❌ خطا در ارسال به {fail_count} کاربر.")
        return

    if admin_info["admin_state"] == "awaiting_ban_id":
        admin_info["admin_state"] = "none"
        target_uid = text
        if target_uid in DB["user_info"]:
            DB["user_info"][target_uid]["is_banned"] = True
            save_db()
            await msg.reply(f"✅ کاربر {target_uid} با موفقیت بن شد.")
        else:
            await msg.reply("❌ کاربری با این شناسه یافت نشد.")
        return

    if admin_info["admin_state"] == "awaiting_unban_id":
        admin_info["admin_state"] = "none"
        target_uid = text
        if target_uid in DB["user_info"]:
            DB["user_info"][target_uid]["is_banned"] = False
            save_db()
            await msg.reply(f"✅ کاربر {target_uid} با موفقیت آنبن شد.")
        else:
            await msg.reply("❌ کاربری با این شناسه یافت نشد.")
        return

    if text == "/admin":
        await send_admin_panel(uid)
    elif text == BTN_ADMIN_STATS:
        total_users = len(DB["user_info"])
        online_now = get_online_users_count()
        in_chat = len(DB["active_chats"]) // 2
        waiting = len(DB["waiting_random"]) + len(DB["waiting_gender"]["male"]) + len(DB["waiting_gender"]["female"])
        stats_text = (
            f"📊 **آمار ربات:**\n\n"
            f"👤 **کل کاربران:** {total_users} نفر\n"
            f"🟢 **کاربران آنلاین (۵ دقیقه اخیر):** {online_now} نفر\n"
            f"💬 **در حال چت:** {in_chat} چت فعال ({in_chat*2} نفر)\n"
            f"⏳ **در صف انتظار:** {waiting} نفر"
        )
        await msg.reply(stats_text)
    elif text == BTN_ADMIN_BROADCAST:
        admin_info["admin_state"] = "awaiting_broadcast_message"
        await msg.reply("لطفاً پیام خود را برای ارسال به همه کاربران وارد کنید:")
    elif text == BTN_ADMIN_BAN:
        admin_info["admin_state"] = "awaiting_ban_id"
        await msg.reply("شناسه کاربری (عددی) فرد مورد نظر برای بن شدن را وارد کنید:")
    elif text == BTN_ADMIN_UNBAN:
        admin_info["admin_state"] = "awaiting_unban_id"
        await msg.reply("شناسه کاربری (عددی) فرد مورد نظر برای آنبن شدن را وارد کنید:")
    elif text == BTN_BACK:
        DB["user_info"][uid]["admin_state"] = "none"
        await send_main_menu(uid, "به منوی اصلی بازگشتید.")
    else:
        await handle_user_message(bot, msg, text)



async def handle_user_message(bot: Robot, msg: Message, text: str):
    """پیام‌های کاربران عادی را پردازش می‌کند."""
    uid = str(msg.chat_id)
    user_info = DB["user_info"][uid]
    status = user_info["status"]
    
    if text == "/start":
        if status == "chatting":
            await disconnect_users(uid, "❌ طرف مقابل چت را ترک کرد.")
        user_info["status"] = "idle"
        await send_main_menu(uid, "👋 سلام! به ربات چت ناشناس خوش آمدی. یکی از گزینه‌ها رو انتخاب کن:")
    
    elif text == "/help":
        help_text = (
            "**راهنمای ربات چت ناشناس:**\n\n"
            "🎲 **اتصال تصادفی:** شما را به یک کاربر اتفاقی وصل می‌کند.\n"
            "👫 **جستجو بر اساس جنسیت:** شما را به یک کاربر از جنس مخالف وصل می‌کند (ابتدا باید جنسیت خود را تنظیم کنید).\n"
            "⚙️ **تنظیم جنسیت:** جنسیت خود را برای استفاده از جستجوی جنسیت مشخص کنید.\n"
            "📊 **تعداد آنلاین:** تعداد کاربران فعال در ربات را نمایش می‌دهد.\n\n"
            "در هنگام چت:\n"
            "❌ **خروج از چت:** به چت فعلی پایان می‌دهد.\n"
            "❗️ **ریپورت کاربر:** اگر کاربر مقابل تخلفی کرد، او را گزارش دهید. با ۳ گزارش، کاربر به طور موقت محدود می‌شود."
        )
        await msg.reply(help_text)

    elif text == BTN_RANDOM_CHAT and status == "idle":
        user_info["status"] = "waiting_random"
        DB["waiting_random"].append(uid)
        await send_main_menu(uid, "⏳ در حال جستجوی یک هم‌صحبت تصادفی...")
        await try_match_random()

    elif text == BTN_GENDER_SEARCH and status == "idle":
        if not user_info["gender"]:
            await msg.reply("لطفا ابتدا جنسیت خود را از منوی '⚙️ تنظیم جنسیت' مشخص کنید.")
            return
        
        user_info["status"] = "waiting_gender"
        target_gender_text = "زن" if user_info["gender"] == "male" else "مرد"
        DB["waiting_gender"][user_info["gender"]].append(uid)
        await send_main_menu(uid, f"⏳ در حال جستجوی یک هم‌صحبت {target_gender_text}...")
        await try_match_gender()

    elif text == BTN_CANCEL_SEARCH and status.startswith("waiting"):
        if status == "waiting_random":
            if uid in DB["waiting_random"]: DB["waiting_random"].remove(uid)
        elif status == "waiting_gender":
            gender = user_info["gender"]
            if gender and uid in DB["waiting_gender"][gender]:
                DB["waiting_gender"][gender].remove(uid)
        
        user_info["status"] = "idle"
        await send_main_menu(uid, "✅ جستجو لغو شد.")

    elif text == BTN_SET_GENDER:
        builder = ChatKeypadBuilder()
        builder.row(builder.button(id="male", text=BTN_MALE), builder.button(id="female", text=BTN_FEMALE))
        gender_keypad = builder.build(resize_keyboard=True)
        await bot.send_message(uid, "جنسیت خود را انتخاب کنید:", chat_keypad=gender_keypad)

    elif text == BTN_ONLINE_COUNT:
        online_count = get_online_users_count()
        await msg.reply(f" هم اکنون {online_count} کاربر آنلاین هستند. 🟢")
        
    elif text in [BTN_MALE, BTN_FEMALE]:
        gender = "male" if text == BTN_MALE else "female"
        user_info["gender"] = gender
        save_db()
        await send_main_menu(uid, f"✅ جنسیت شما به '{'مرد' if gender == 'male' else 'زن'}' تغییر یافت.")

    elif text == BTN_EXIT_CHAT and status == "chatting":
        await disconnect_users(uid, "❌ طرف مقابل چت را ترک کرد.")

    elif text == BTN_REPORT_USER and status == "chatting":
        peer = DB["active_chats"].get(uid)
        if peer:

            await msg.reply("این قابلیت هنوز پیاده سازی نشده است")

    elif status == "chatting":
        peer = DB["active_chats"].get(uid)
        if peer:
            if text:
                await bot.send_message(peer, text)
                await store_log("message", uid, peer, text)
            elif msg.file:
                await bot.send_file(peer, file_id=msg.file.file_id, caption=msg.text)
                await store_log("file", uid, peer, msg.file.file_name)


@bot.on_message()
async def message_handler(bot: Robot, msg: Message):
    print(msg.chat_id)
    """نقطه ورود اصلی برای تمام پیام‌ها."""
    uid = str(msg.chat_id)
    text = msg.text.strip() if msg.text else ""
    

    if uid not in DB["user_info"]:
        print(f"کاربر جدید: {uid}")
    update_activity(uid)
    DB["user_info"][uid] 
    

    if DB["user_info"][uid].get("is_banned", False):
        await msg.reply("شما توسط ادمین از ربات مسدود شده‌اید و اجازه استفاده ندارید.")
        return

    if uid == ADMIN_ID:
        await handle_admin_command(bot, msg, text)
    else:
        await handle_user_message(bot, msg, text)


async def main():
    load_db()
    await bot.run()

if __name__ == "__main__":
    try:asyncio.run(main())
    except KeyboardInterrupt:save_db()
