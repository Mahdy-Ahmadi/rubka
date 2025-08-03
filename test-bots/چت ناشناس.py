import asyncio
from rubka.asynco import Robot
from rubka.context import Message
from rubka.keypad import ChatKeypadBuilder
from collections import deque, defaultdict
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from typing import Coroutine, Any, Literal, Dict

if not os.path.exists("profile_pics"):
    os.makedirs("profile_pics")

bot = Robot(token="")
ADMIN_ID = "b0HJtFl0Dx60230306be5dd14a713977"

async def set_com():
    print(await bot.set_commands(
        [
            {"command": "start", "description": "فعالسازی ربات"},
            {"command": "admin", "description": "پنل ادمین ربات (مخصوص ادمین‌ها)"},
            {"command": "help", "description": "راهنمای استفاده از ربات"}
        ]
    ))

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
        "admin_state": "none", 
        "profile_state": "none", 
        "tg_first_name": "",
        "nickname": "ناشناس", 
        "age": None,
        "city": None,
        "province": None,
        "height": None,
        "bio": None,
        "profile_photo_path": None,
    })
}

BTN_RANDOM_CHAT = "🎲 اتصال تصادفی"
BTN_GENDER_SEARCH = "👫 جستجو بر اساس جنسیت"
BTN_SET_GENDER = "⚙️ تنظیم جنسیت"
BTN_EDIT_PROFILE = "📝 ویرایش اطلاعات"
BTN_ONLINE_COUNT = "📊 تعداد آنلاین"
BTN_CANCEL_SEARCH = "✖️ لغو جستجو"
BTN_EXIT_CHAT = "❌ خروج از چت"
BTN_REPORT_USER = "❗️ ریپورت کاربر"
BTN_VIEW_PROFILE = "👤 مشاهده پروفایل"
BTN_MALE = "🧔 مرد"
BTN_FEMALE = "👩 زن"
BTN_BACK = "⬅️ بازگشت"

BTN_ADMIN_STATS = "📊 آمار کاربران"
BTN_ADMIN_BROADCAST = "📣 پیام همگانی"
BTN_ADMIN_BAN = "🚫 بن کردن کاربر"
BTN_ADMIN_UNBAN = "✅ آنبن کردن کاربر"
BTN_ADMIN_USER_INFO = "ℹ️ دریافت اطلاعات کاربر"

BTN_SET_NICKNAME = "✏️ تنظیم نام مستعار"
BTN_SET_AGE = "🎂 تنظیم سن"
BTN_SET_CITY = "🏙 تنظیم شهر"
BTN_SET_PROVINCE = "🗺 تنظیم استان"
BTN_SET_HEIGHT = "📏 تنظیم قد"
BTN_SET_BIO = "📝 تنظیم بیوگرافی"
BTN_SET_PHOTO = "🖼 ارسال/تغییر عکس پروفایل"


def save_db():
    """اطلاعات کاربران را برای ذخیره‌سازی آماده کرده و در فایل JSON می‌نویسد."""
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
                for key, value in DB["user_info"]["default"].items():
                    if key not in info:
                        info[key] = value
                DB["user_info"][uid] = info
        except (json.JSONDecodeError, AttributeError):
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
        builder.row(builder.button(id="view_profile", text=BTN_VIEW_PROFILE))
    elif status.startswith("waiting"):
        builder.row(builder.button(id="cancel", text=BTN_CANCEL_SEARCH))
    else: 
        builder.row(builder.button(id="random", text=BTN_RANDOM_CHAT), builder.button(id="gender", text=BTN_GENDER_SEARCH))
        builder.row(builder.button(id="set_gender", text=BTN_SET_GENDER), builder.button(id="edit_profile", text=BTN_EDIT_PROFILE))
        builder.row(builder.button(id="online", text=BTN_ONLINE_COUNT))

    main_keypad = builder.build(resize_keyboard=True)
    await bot.send_message(uid, text, chat_keypad=main_keypad)

async def connect_users(u1: str, u2: str):
    """دو کاربر را به یکدیگر متصل می‌کند."""
    DB["active_chats"][u1] = u2
    DB["active_chats"][u2] = u1
    DB["user_info"][u1]["status"] = "chatting"
    DB["user_info"][u2]["status"] = "chatting"

    u1_nickname = DB["user_info"][u1].get("nickname", "ناشناس")
    u2_nickname = DB["user_info"][u2].get("nickname", "ناشناس")

    await send_main_menu(u1, f"✅ چت با '{u2_nickname}' شروع شد! پیام شما به طرف مقابل ارسال می‌شود.")
    await send_main_menu(u2, f"✅ چت با '{u1_nickname}' شروع شد! پیام شما به طرف مقابل ارسال می‌شود.")
    await store_log("connect", u1, u2)

async def disconnect_users(uid: str, reason_for_peer: str, text_for_user: str = "✅ شما از چت خارج شدید."):
    """اتصال دو کاربر را قطع می‌کند."""
    peer = DB["active_chats"].pop(uid, None)
    if peer:
        DB["active_chats"].pop(peer, None)
        DB["user_info"][peer]["status"] = "idle"
        await send_main_menu(peer, reason_for_peer)

    DB["user_info"][uid]["status"] = "idle"
    await send_main_menu(uid, text_for_user)
    await store_log("disconnect", uid, peer, reason_for_peer)


async def try_match_random():
    """تلاش برای اتصال کاربران در صف تصادفی."""
    while len(DB["waiting_random"]) >= 2:
        u1 = DB["waiting_random"].popleft()
        u2 = DB["waiting_random"].popleft()
        await connect_users(u1, u2)

async def try_match_gender():
    """تلاش برای اتصال کاربران در صف جنسیت."""
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
    builder.row(builder.button(id="admin_user_info", text=BTN_ADMIN_USER_INFO))
    builder.row(builder.button(id="back", text=BTN_BACK))
    
    admin_keypad = builder.build(resize_keyboard=True)
    await bot.send_message(uid, "پنل مدیریت ربات:", chat_keypad=admin_keypad)

async def handle_admin_command(bot: Robot, msg: Message, text: str):
    """دستورات ادمین را پردازش می‌کند."""
    uid = str(msg.chat_id)
    admin_info = DB["user_info"][uid]
    admin_state = admin_info.get("admin_state", "none")

    if admin_state == "awaiting_broadcast_message":
        admin_info["admin_state"] = "none"
        await msg.reply("⏳ در حال ارسال پیام همگانی...")
        all_users = list(DB["user_info"].keys())
        success_count, fail_count = 0, 0
        for user_id in all_users:
            try:
                await bot.send_message(user_id, text)
                success_count += 1
            except Exception as e:
                fail_count += 1
                print(f"خطا در ارسال پیام به {user_id}: {e}")
        await msg.reply(f"✅ پیام همگانی به {success_count} کاربر ارسال شد.\n❌ خطا در ارسال به {fail_count} کاربر.")
        return

    elif admin_state == "awaiting_ban_id":
        admin_info["admin_state"] = "none"
        target_uid = text
        if target_uid in DB["user_info"]:
            DB["user_info"][target_uid]["is_banned"] = True
            save_db()
            await msg.reply(f"✅ کاربر {target_uid} با موفقیت بن شد.")
        else:
            await msg.reply("❌ کاربری با این شناسه یافت نشد.")
        return

    elif admin_state == "awaiting_unban_id":
        admin_info["admin_state"] = "none"
        target_uid = text
        if target_uid in DB["user_info"]:
            DB["user_info"][target_uid]["is_banned"] = False
            save_db()
            await msg.reply(f"✅ کاربر {target_uid} با موفقیت آنبن شد.")
        else:
            await msg.reply("❌ کاربری با این شناسه یافت نشد.")
        return

    elif admin_state == "awaiting_user_info_id":
        admin_info["admin_state"] = "none"
        target_uid = text
        if target_uid in DB["user_info"]:
            user_data = DB["user_info"][target_uid]
            info_text = (
                f"**اطلاعات کاربر:** `{target_uid}`\n"
                f"**نام تلگرام:** {user_data.get('tg_first_name', 'ثبت نشده')}\n"
                f"**نام مستعار:** {user_data.get('nickname', 'ثبت نشده')}\n"
                f"**جنسیت:** {user_data.get('gender', 'ثبت نشده')}\n"
                f"**سن:** {user_data.get('age', 'ثبت نشده')}\n"
                f"**وضعیت بن:** {'بله' if user_data.get('is_banned') else 'خیر'}"
            )
            await msg.reply(info_text)
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
    elif text == BTN_ADMIN_USER_INFO:
        admin_info["admin_state"] = "awaiting_user_info_id"
        await msg.reply("شناسه کاربری مورد نظر را وارد کنید:")
    elif text == BTN_BACK:
        admin_info["admin_state"] = "none"
        await send_main_menu(uid, "به منوی اصلی بازگشتید.")
    else:
        await handle_user_message(bot, msg, text)


async def send_profile_editor_menu(uid: str):
    """منوی ویرایش پروفایل را ارسال می‌کند."""
    builder = ChatKeypadBuilder()
    builder.row(builder.button(id="set_nickname", text=BTN_SET_NICKNAME), builder.button(id="set_age", text=BTN_SET_AGE))
    builder.row(builder.button(id="set_city", text=BTN_SET_CITY), builder.button(id="set_province", text=BTN_SET_PROVINCE))
    builder.row(builder.button(id="set_height", text=BTN_SET_HEIGHT), builder.button(id="set_bio", text=BTN_SET_BIO))
    builder.row(builder.button(id="set_photo", text=BTN_SET_PHOTO))
    builder.row(builder.button(id="back_to_main", text=BTN_BACK))
    keypad = builder.build(resize_keyboard=True)
    await bot.send_message(uid, "کدام بخش از پروفایل خود را می‌خواهید ویرایش کنید؟", chat_keypad=keypad)


async def handle_profile_editing(bot: Robot, msg: Message, text: str):
    """پردازش پیام‌ها در حالت ویرایش پروفایل."""
    uid = str(msg.chat_id)
    user_info = DB["user_info"][uid]
    state = user_info.get("profile_state", "none")
    
    state_map = {
        "awaiting_nickname": ("nickname", "نام مستعار"), "awaiting_age": ("age", "سن"),
        "awaiting_city": ("city", "شهر"), "awaiting_province": ("province", "استان"),
        "awaiting_height": ("height", "قد"), "awaiting_bio": ("bio", "بیوگرافی"),
    }

    if state in state_map:
        field, field_name = state_map[state]
        user_info[field] = text
        user_info["profile_state"] = "none"
        save_db()
        await send_profile_editor_menu(uid)
        await bot.send_message(uid, f"✅ {field_name} شما با موفقیت به '{text}' تغییر یافت.")
        return True

    return False


async def handle_user_message(bot: Robot, msg: Message, text: str):
    """پیام‌های کاربران عادی را پردازش می‌کند."""
    uid = str(msg.chat_id)
    user_info = DB["user_info"][uid]
    status = user_info["status"]

    if await handle_profile_editing(bot, msg, text):
        return
    
    if text == "/start":
        if status == "chatting":
            await disconnect_users(uid, "❌ طرف مقابل ربات را مجددا استارت کرد و از چت خارج شد.")
        user_info["status"] = "idle"
        await send_main_menu(uid, "👋 سلام! به ربات چت ناشناس خوش آمدی. برای شروع یکی از گزینه‌ها رو انتخاب کن:")
    
    elif text == "/help":
        help_text = (
            "**راهنمای ربات چت ناشناس:**\n\n"
            "🎲 **اتصال تصادفی:** شما را به یک کاربر اتفاقی وصل می‌کند.\n"
            "👫 **جستجو بر اساس جنسیت:** شما را به یک کاربر از جنس مخالف وصل می‌کند (ابتدا باید جنسیت خود را تنظیم کنید).\n"
            "📝 **ویرایش اطلاعات:** در این بخش می‌توانید پروفایل خود (نام، سن، عکس و...) را برای نمایش به دیگران تکمیل کنید.\n"
            "📊 **تعداد آنلاین:** تعداد کاربران فعال در ربات را نمایش می‌دهد.\n\n"
            "**در هنگام چت:**\n"
            "❌ **خروج از چت:** به چت فعلی پایان می‌دهد.\n"
            "👤 **مشاهده پروفایل:** اطلاعات و عکس کاربر مقابل را مشاهده کنید.\n"
            "❗️ **ریپورت کاربر:** اگر کاربر مقابل تخلفی کرد، او را گزارش دهید."
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
        target_gender = "male" if user_info["gender"] == "female" else "female"
        target_gender_text = "زن" if user_info["gender"] == "male" else "مرد"
        DB["waiting_gender"][target_gender].append(uid)
        await send_main_menu(uid, f"⏳ در حال جستجوی یک هم‌صحبت {target_gender_text}...")
        await try_match_gender()

    elif text == BTN_CANCEL_SEARCH and status.startswith("waiting"):
        if status == "waiting_random":
            if uid in DB["waiting_random"]: DB["waiting_random"].remove(uid)
        elif status == "waiting_gender":
            for gender_queue in DB["waiting_gender"].values():
                if uid in gender_queue: gender_queue.remove(uid)
        
        user_info["status"] = "idle"
        await send_main_menu(uid, "✅ جستجو لغو شد.")

    elif text == BTN_SET_GENDER:
        builder = ChatKeypadBuilder()
        builder.row(builder.button(id="male", text=BTN_MALE), builder.button(id="female", text=BTN_FEMALE))
        gender_keypad = builder.build(resize_keyboard=True)
        await bot.send_message(uid, "جنسیت خود را انتخاب کنید:", chat_keypad=gender_keypad)

    elif text in [BTN_MALE, BTN_FEMALE]:
        gender = "male" if text == BTN_MALE else "female"
        user_info["gender"] = gender
        save_db()
        await send_main_menu(uid, f"✅ جنسیت شما به '{'مرد' if gender == 'male' else 'زن'}' تغییر یافت.")
    
    elif text == BTN_EDIT_PROFILE:
        user_info["profile_state"] = "editing_menu"
        await send_profile_editor_menu(uid)
    
    elif user_info["profile_state"] == "editing_menu":
        state_map = {
            BTN_SET_NICKNAME: ("awaiting_nickname", "نام مستعار"), BTN_SET_AGE: ("awaiting_age", "سن"),
            BTN_SET_CITY: ("awaiting_city", "شهر"), BTN_SET_PROVINCE: ("awaiting_province", "استان"),
            BTN_SET_HEIGHT: ("awaiting_height", "قد"), BTN_SET_BIO: ("awaiting_bio", "بیوگرافی"),
        }
        if text in state_map:
            state, field_name = state_map[text]
            user_info["profile_state"] = state
            await msg.reply(f"لطفاً {field_name} خود را وارد کنید:")
        elif text == BTN_SET_PHOTO:
            user_info["profile_state"] = "awaiting_photo"
            await msg.reply("لطفاً عکس پروفایل خود را ارسال کنید:")
        elif text == BTN_BACK:
            user_info["profile_state"] = "none"
            await send_main_menu(uid, "به منوی اصلی بازگشتید.")

    elif text == BTN_ONLINE_COUNT:
        online_count = get_online_users_count()
        await msg.reply(f" هم اکنون {online_count} کاربر آنلاین هستند. 🟢")
        
    elif text == BTN_EXIT_CHAT and status == "chatting":
        await disconnect_users(uid, "❌ طرف مقابل چت را ترک کرد.")

    elif text == BTN_VIEW_PROFILE and status == "chatting":
        peer = DB["active_chats"].get(uid)
        if peer:
            peer_info = DB["user_info"][peer]
            profile_text = (
                f"**پروفایل {peer_info.get('nickname', 'ناشناس')}**\n\n"
                f"**سن:** {peer_info.get('age', 'ثبت نشده')}\n"
                f"**قد:** {peer_info.get('height', 'ثبت نشده')}\n"
                f"**استان:** {peer_info.get('province', 'ثبت نشده')}\n"
                f"**شهر:** {peer_info.get('city', 'ثبت نشده')}\n"
                f"**بیوگرافی:** {peer_info.get('bio', 'ثبت نشده')}"
            )
            photo_path = peer_info.get("profile_photo_path")
            if photo_path and os.path.exists(photo_path):
                await bot.send_image(uid, path=photo_path, text=profile_text)
            else:
                await msg.reply(profile_text)

    elif text == BTN_REPORT_USER and status == "chatting":
        await msg.reply("این قابلیت هنوز به طور کامل پیاده‌سازی نشده است.")

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
    uid = str(msg.chat_id)
    text = msg.text.strip() if msg.text else ""
    
    if uid not in DB["user_info"]:
        print(f"کاربر جدید: {uid} - نام: {await bot.get_name(msg.chat_id)}")
        DB["user_info"][uid]["tg_first_name"] = await bot.get_name(msg.chat_id)
        DB["user_info"][uid]["nickname"] = await bot.get_name(msg.chat_id)
        save_db()

    update_activity(uid)
    
    if DB["user_info"][uid].get("is_banned", False):
        await msg.reply("شما توسط ادمین از ربات مسدود شده‌اید و اجازه استفاده ندارید.")
        return

    if msg.file and DB["user_info"][uid].get("profile_state") == "awaiting_photo":
        user_info = DB["user_info"][uid]
        file_id = msg.file.file_id
        file_path = f"profile_pics/{uid}.jpg"
        
        try:
            await bot.download(file_id=file_id, save_as=file_path, verbose=True)
            user_info["profile_photo_path"] = file_path
            user_info["profile_state"] = "none"
            save_db()
            await send_profile_editor_menu(uid)
            await bot.send_message(uid, "✅ عکس پروفایل شما با موفقیت آپلود و ذخیره شد.")
        except Exception as e:
            print(f"خطا در دانلود عکس پروفایل برای {uid}: {e}")
            await msg.reply("❌ مشکلی در ذخیره عکس شما پیش آمد. لطفا دوباره تلاش کنید.")
        return

    if uid == ADMIN_ID:
        await handle_admin_command(bot, msg, text)
    else:
        await handle_user_message(bot, msg, text)


async def main():
    load_db()
    await set_com()
    print("ربات در حال اجرا است...")
    await bot.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nخروج از برنامه... در حال ذخیره اطلاعات کاربران.")
        save_db()
        print("اطلاعات ذخیره شد.")
