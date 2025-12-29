from rubka import Robot,Message,ChatKeypadBuilder
from collections import deque, defaultdict
from datetime import datetime, timedelta
import json,os,logging,asyncio,sqlite3
from pathlib import Path

BOT_TOKEN = "token" #توکن بات
ADMIN_ID = "b0FnQvV0P3800a2f75e560a02e2b5049" # چت ایدی ادمین
bot = Robot(token=BOT_TOKEN, safeSendMode=True,show_progress=True)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
ONLINE_THRESHOLD = timedelta(minutes=5)
MAX_REPORT_TEXT_LENGTH = 200
DEFAULT_USER_INFO_TEMPLATE = {
    "status": "idle",              
    "gender": None,                
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
    "positive_ratings": 0,         
    "negative_ratings": 0,         
    "last_peer": None,             
    "blocked_users": set(),        
    "interests": set(),            
    "seeking_gender": None,        
    "seeking_age_min": None,
    "seeking_age_max": None,
    "seeking_province": None,
    "seeking_city": None,
    "reports_count": 0,            
}
DB = {
    "waiting_random": deque(),
    "waiting_gender": {"male": deque(), "female": deque()},
    "waiting_province": defaultdict(deque),
    "waiting_city": defaultdict(deque),
    "waiting_interest": defaultdict(deque),

    "active_chats": {},      
    "online_users": {},      

    "user_info": defaultdict(lambda: DEFAULT_USER_INFO_TEMPLATE.copy()),
    "reports": [] 
}
BTN_RANDOM_CHAT = "🎲 گفت‌وگوی تصادفی"
BTN_ADVANCED_SEARCH = "🔎 جستجوی پیشرفته"
BTN_EDIT_PROFILE = "👤 پروفایل من"
BTN_ONLINE_COUNT = "📊 کاربران آنلاین"
BTN_GO_TO_ADMIN = "⚙️ پنل مدیریت"
BTN_SEARCH_GENDER = "👫 جستجو بر اساس جنسیت"
BTN_SEARCH_PROVINCE = "🗺 جستجو بر اساس استان"
BTN_SEARCH_CITY = "🏙 جستجو بر اساس شهر"
BTN_SEARCH_INTERESTS = "🎯 جستجو بر اساس علایق مشترک"
BTN_CANCEL_SEARCH = "✖️ لغو جستجو"
BTN_BACK = "⬅️ بازگشت"
BTN_BACK_TO_MAIN = "🏠 بازگشت به منوی اصلی"
BTN_EXIT_CHAT = "🚪 پایان گفت‌وگو"
BTN_VIEW_PROFILE = "🧑‍💻 مشاهده پروفایل طرف مقابل"
BTN_BLOCK_USER = "🚫 مسدود کردن کاربر"
BTN_REPORT_USER = "🚩 گزارش تخلف"
BTN_SET_GENDER = "🚻 انتخاب جنسیت"
BTN_MALE = "🧔 مرد"
BTN_FEMALE = "👩 زن"
BTN_OTHER_GENDER = "⚧ دیگر"
BTN_SET_NICKNAME = "✏️ نام نمایشی"
BTN_SET_AGE = "🎂 سن"
BTN_SET_CITY = "🏙 شهر"
BTN_SET_PROVINCE = "🗺 استان"
BTN_SET_HEIGHT = "📏 قد"
BTN_SET_BIO = "📝 بیوگرافی"
BTN_SET_PHOTO = "🖼 تغییر عکس پروفایل"
BTN_SET_INTERESTS = "🎯 علایق من"
BTN_SET_SEEKING_PREFERENCES = "🔍 تنظیمات جستجو"
BTN_SEE_MY_INFO = "ℹ️ مشاهده اطلاعات من"
BTN_RATE_POSITIVE = "👍 عالی بود"
BTN_RATE_NEGATIVE = "👎 جالب نبود"
BTN_SKIP_RATING = "⏭ رد کردن"
BTN_ADMIN_STATS = "📊 آمار ربات"
BTN_ADMIN_BROADCAST = "📣 ارسال پیام همگانی"
BTN_ADMIN_BAN = "🚫 مسدود کردن کاربر"
BTN_ADMIN_UNBAN = "✅ رفع مسدودی کاربر"
BTN_ADMIN_USER_INFO = "ℹ️ دریافت اطلاعات کاربر"
BTN_ADMIN_VIEW_REPORTS = "🚩 مشاهده و مدیریت گزارش‌ها"
BTN_ADMIN_CLEAR_QUEUE = "🧹 پاکسازی صف انتظار"
BTN_ADMIN_VIEW_BLOCKED = "👥 لیست کاربران مسدود"

DB_PATH = "bot_v67.db"
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        nickname TEXT DEFAULT 'ناشناس',
        gender TEXT,
        age INTEGER,
        city TEXT,
        province TEXT,
        height INTEGER,
        bio TEXT,
        blocked_users TEXT,
        interests TEXT,
        seeking_gender TEXT,
        seeking_age_min INTEGER,
        seeking_age_max INTEGER,
        seeking_province TEXT,
        seeking_city TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reporter_id TEXT,
        reported_user TEXT,
        reason TEXT,
        timestamp TEXT,
        resolved BOOLEAN,
        resolution_details TEXT
    )
    ''')
    conn.commit()
    conn.close()
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
def load_db():
    if not os.path.exists(DB_PATH):
        logger.warning("دیتابیس یافت نشد. از یک پایگاه داده جدید شروع می‌کنیم.")
        create_tables()
        return
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users_data = cursor.fetchall()
        for user in users_data:
            user_info = dict(user)
            user_info["blocked_users"] = set(json.loads(user_info["blocked_users"]) if user_info["blocked_users"] else [])
            user_info["interests"] = set(json.loads(user_info["interests"]) if user_info["interests"] else [])
            DB["user_info"][user_info["id"]] = user_info
        cursor.execute("SELECT * FROM reports")
        reports_data = cursor.fetchall()
        DB["reports"] = [dict(report) for report in reports_data]
        conn.close()
    except (sqlite3.Error, json.JSONDecodeError) as e:
        logger.error(f"خطا در بارگذاری از دیتابیس: {e}")
        conn.close()
def save_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        for uid, user_info in DB["user_info"].items():
            blocked_users = json.dumps(list(user_info.get("blocked_users", [])))
            interests = json.dumps(list(user_info.get("interests", [])))

            cursor.execute('''
            INSERT OR REPLACE INTO users (id, nickname, gender, age, city, province, height, bio, blocked_users, interests, seeking_gender, seeking_age_min, seeking_age_max, seeking_province, seeking_city)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                uid,
                user_info.get("nickname", "ناشناس"),
                user_info.get("gender"),
                user_info.get("age"),
                user_info.get("city"),
                user_info.get("province"),
                user_info.get("height"),
                user_info.get("bio"),
                blocked_users,
                interests,
                user_info.get("seeking_gender"),
                user_info.get("seeking_age_min"),
                user_info.get("seeking_age_max"),
                user_info.get("seeking_province"),
                user_info.get("seeking_city")
            ))
        for report in DB["reports"]:
            cursor.execute('''
            INSERT INTO reports (reporter_id, reported_user, reason, timestamp, resolved, resolution_details)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                report["reporter_id"],
                report["reported_user"],
                report["reason"],
                report["timestamp"],
                report["resolved"],
                report["resolution_details"]
            ))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logger.error(f"خطا در ذخیره‌سازی داده‌ها در دیتابیس: {e}")
        conn.close()
async def store_log(log_type: str, sender: str, receiver: str = None, content: str = "", details: dict = None):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": log_type,
        "from": sender,
        "to": receiver,
        "content": content,
        "details": details or {}
    }
    try:
        with open("chat_logs_v6.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except IOError as e:
        logger.error(f"خطا در ثبت لاگ: {e}")
def save_reports():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        for report in DB["reports"]:
            cursor.execute('''
            INSERT OR REPLACE INTO reports (id, reporter_id, reported_user, reason, timestamp, resolved, resolution_details)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                report["id"],
                report["reporter"],
                report["reported_user"],
                report["reason"],
                report["timestamp"],
                report["resolved"],
                report["resolution_details"]
            ))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logger.error(f"خطا در ذخیره‌سازی گزارش‌ها در دیتابیس: {e}")

async def add_report(reporter_id: str, reported_id: str, reason: str) -> int:
    report_id = None
    timestamp = datetime.now().isoformat()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO reports (reporter_id, reported_user, reason, timestamp, resolved, resolution_details)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (reporter_id, reported_id, reason, timestamp, False, ""))
    
    conn.commit()
    report_id = cursor.lastrowid
    conn.close()
    DB["user_info"][reporter_id]["reports_count"] += 1
    report = {
        "id": report_id,
        "reporter": reporter_id,
        "reported_user": reported_id,
        "reason": reason,
        "timestamp": timestamp,
        "resolved": False,
        "resolution_details": ""
    }
    DB["reports"].append(report)
    save_reports()
    await store_log("report_added", reporter_id, reported_id, reason, {"report_id": report_id})
    return report_id

def load_reports():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reports")
        reports_data = cursor.fetchall()
        DB["reports"] = [dict(report) for report in reports_data]
        conn.close()
    except sqlite3.Error as e:
        logger.error(f"خطا در بارگذاری گزارش‌ها از دیتابیس: {e}")

def get_online_users_count() -> int:
    now = datetime.now()
    return sum(1 for last_seen in DB["online_users"].values() if now - last_seen < ONLINE_THRESHOLD)

def get_user_info_display(uid: str, for_admin: bool = False) -> str:
    user_data = DB["user_info"][uid]
    gender_map = {'male': '🧔 مرد', 'female': '👩 زن', 'other': '⚧ دیگر', None: 'ثبت نشده'}
    seeking_gender_map = {'male': '🧔 مرد', 'female': '👩 زن', 'other': '⚧ دیگر', None: 'مهم نیست'}

    profile_info = (
    f">👤 **پروفایل کاربر**: `{user_data.get('nickname', 'ناشناس')}`\n"
    f">-----------------------------\n"
    f">🌟 **امتیازها :**\n"
    f">👍 مثبت : {user_data.get('positive_ratings', 0)}\n"
    f">👎 منفی : {user_data.get('negative_ratings', 0)}\n"
    f">🌟 **اطلاعات شخصی :**\n"
    f">🚻 **جنسیت :** {gender_map.get(user_data.get('gender'), 'ثبت نشده')}\n"
    f">🎡 **چت ایدی :** `{uid}`\n"
    f">🎂 **سن :** {user_data.get('age', 'ثبت نشده')} سال\n"
    f">📏 **قد :** {user_data.get('height', 'ثبت نشده')} سانتی‌متر\n"
    f">🗺 **استان :** {user_data.get('province', 'ثبت نشده')}\n"
    f">🏙 **شهر :** {user_data.get('city', 'ثبت نشده')}\n\n"
    f">📝 **بیوگرافی :**\n"
    f">`{user_data.get('bio', 'ثبت نشده')}`\n\n"
    f">🎯 **علایق :** {', '.join(sorted(list(user_data.get('interests', [])))) or 'ثبت نشده'}\n"
    f">-----------------------------\n"
    f">🔍 **تنظیمات جستجو :**\n"
    f">👫 دنبال جنسیت : {seeking_gender_map.get(user_data.get('seeking_gender'), 'مهم نیست')}\n"
    f">🎂 دنبال محدوده سنی : {user_data.get('seeking_age_min', '؟')} تا {user_data.get('seeking_age_max', '؟')} سال\n"
    f">🗺 دنبال استان : {user_data.get('seeking_province') or 'مهم نیست'}\n"
)



    if for_admin:
        admin_part = (
            f"\n\n===== اطلاعات ادمین =====\n"
            f"ID کاربر: `{uid}`\n"
            f"نام روبیکا: {user_data.get('tg_first_name', 'ثبت نشده')}\n"
            f"وضعیت: {'مسدود 🚫' if user_data.get('is_banned') else 'فعال ✅'}\n"
            f"تعداد گزارشات ثبت شده توسط او: {user_data.get('reports_count', 0)}\n"
        )
        profile_info += admin_part
    return profile_info

async def send_main_menu(uid: str, text: str):
    user_info = DB["user_info"][uid]
    status = user_info.get("status", "idle")

    builder = ChatKeypadBuilder()
    if status == "chatting":
        builder.row(builder.button(id="exit_chat", text=BTN_EXIT_CHAT))
        builder.row(
            builder.button(id="view_profile", text=BTN_VIEW_PROFILE),
            builder.button(id="block_user", text=BTN_BLOCK_USER),
            builder.button(id="report_user", text=BTN_REPORT_USER),
        )
    elif status.startswith("waiting"):
        builder.row(builder.button(id="cancel_search", text=BTN_CANCEL_SEARCH))
    elif status == "rating":
        builder.row(builder.button(id="rate_pos", text=BTN_RATE_POSITIVE), builder.button(id="rate_neg", text=BTN_RATE_NEGATIVE))
        builder.row(builder.button(id="skip_rating", text=BTN_SKIP_RATING))
    elif status == "idle":
        builder.row(builder.button(id="random", text=BTN_RANDOM_CHAT), builder.button(id="advanced_search", text=BTN_ADVANCED_SEARCH))
        builder.row(builder.button(id="edit_profile", text=BTN_EDIT_PROFILE), builder.button(id="online_count", text=BTN_ONLINE_COUNT))
        if uid == ADMIN_ID:
            builder.row(builder.button(id="go_to_admin", text=BTN_GO_TO_ADMIN))
            
    await bot.send_message(uid, text, chat_keypad=builder.build(resize_keyboard=True))


async def send_profile_editor_menu(uid: str, text: str = "بخش مورد نظر برای ویرایش یا تکمیل پروفایل را انتخاب کنید:"):
    builder = ChatKeypadBuilder()
    builder.row(builder.button(id="set_nickname", text=BTN_SET_NICKNAME), builder.button(id="set_age", text=BTN_SET_AGE))
    builder.row(builder.button(id="set_gender", text=BTN_SET_GENDER), builder.button(id="set_height", text=BTN_SET_HEIGHT))
    builder.row(builder.button(id="set_province", text=BTN_SET_PROVINCE), builder.button(id="set_city", text=BTN_SET_CITY))
    builder.row(builder.button(id="set_bio", text=BTN_SET_BIO), builder.button(id="set_photo", text=BTN_SET_PHOTO))
    builder.row(builder.button(id="set_interests", text=BTN_SET_INTERESTS), builder.button(id="set_seeking_prefs", text=BTN_SET_SEEKING_PREFERENCES))
    builder.row(builder.button(id="see_my_info", text=BTN_SEE_MY_INFO), builder.button(id="back_to_main", text=BTN_BACK_TO_MAIN))
    await bot.send_message(uid, text, chat_keypad=builder.build(resize_keyboard=True))

async def send_advanced_search_menu(uid: str):
    builder = ChatKeypadBuilder()
    builder.row(builder.button(id="search_gender", text=BTN_SEARCH_GENDER))
    builder.row(builder.button(id="search_province", text=BTN_SEARCH_PROVINCE), builder.button(id="search_city", text=BTN_SEARCH_CITY))
    builder.row(builder.button(id="search_interests", text=BTN_SEARCH_INTERESTS))
    builder.row(builder.button(id="back_to_main", text=BTN_BACK))
    await bot.send_message(uid, "چگونه می‌خواهید هم‌صحبت خود را پیدا کنید؟", chat_keypad=builder.build(resize_keyboard=True))

async def send_gender_selection_menu(uid: str, text: str, for_seeking: bool = False):
    builder = ChatKeypadBuilder()
    builder.row(builder.button(id="male", text=BTN_MALE), builder.button(id="female", text=BTN_FEMALE))
    if for_seeking: 
        builder.row(builder.button(id="cancel", text=BTN_BACK))
    else:
        builder.row(builder.button(id="other_gender", text=BTN_OTHER_GENDER))
        builder.row(builder.button(id="cancel", text=BTN_BACK))
    await bot.send_message(uid, text, chat_keypad=builder.build(resize_keyboard=True))
    
async def send_seeking_preferences_menu(uid: str, text: str = "تنظیمات جستجوی خود را مشخص کنید:"):
    builder = ChatKeypadBuilder()
    builder.row(builder.button(id="set_seeking_gender", text="جنسیت مورد نظر"), builder.button(id="set_seeking_age", text="محدوده سنی"))
    builder.row(builder.button(id="set_seeking_province", text="استان مورد نظر"))
    builder.row(builder.button(id="back_to_profile_editor", text=BTN_BACK))
    await bot.send_message(uid, text, chat_keypad=builder.build(resize_keyboard=True))




def is_blocked(u1: str, u2: str) -> bool:
    return u2 in DB["user_info"][u1].get("blocked_users", set()) or \
           u1 in DB["user_info"][u2].get("blocked_users", set())

async def connect_users(u1: str, u2: str):
    DB["active_chats"][u1] = u2
    DB["active_chats"][u2] = u1
    DB["user_info"][u1]["status"] = "chatting"
    DB["user_info"][u2]["status"] = "chatting"
    
    u1_nickname = DB["user_info"][u1].get("nickname", "ناشناس")
    u2_nickname = DB["user_info"][u2].get("nickname", "ناشناس")

    await send_main_menu(u1, f"✅ گفتگو با '{u2_nickname}' آغاز شد. می‌توانید پیام دهید.")
    await send_main_menu(u2, f"✅ گفتگو با '{u1_nickname}' آغاز شد. می‌توانید پیام دهید.")
    await store_log("connect", u1, u2)

async def disconnect_users(uid: str, reason_for_peer: str, text_for_user: str = "✅ شما از چت خارج شدید."):
    peer = DB["active_chats"].pop(uid, None)
    if peer:
        DB["active_chats"].pop(peer, None)
        DB["user_info"][peer]["status"] = "rating"
        DB["user_info"][peer]["last_peer"] = uid
        await send_main_menu(peer, f"{reason_for_peer}\n\nلطفاً به این گفتگو امتیاز دهید:")

    DB["user_info"][uid]["status"] = "rating"
    DB["user_info"][uid]["last_peer"] = peer
    await send_main_menu(uid, f"{text_for_user}\n\nلطفاً به این گفتگو امتیاز دهید:")
    await store_log("disconnect", uid, peer, reason_for_peer)


async def try_match_users(queue, u1: str):
    """
    برای کاربر u1 در صف داده شده یک هم‌صحبت مناسب بر اساس تنظیمات جستجو پیدا می‌کند.
    """
    user1_info = DB["user_info"][u1]
    
    
    potential_matches = []
    for u2 in list(queue):
        if u1 == u2 or is_blocked(u1, u2):
            continue

        user2_info = DB["user_info"][u2]
        
        
        match_u1_to_u2 = True
        if user1_info.get("seeking_gender") and user1_info["seeking_gender"] != user2_info.get("gender"): match_u1_to_u2 = False
        if user1_info.get("seeking_age_min") and user2_info.get("age") and user2_info["age"] < user1_info["seeking_age_min"]: match_u1_to_u2 = False
        if user1_info.get("seeking_age_max") and user2_info.get("age") and user2_info["age"] > user1_info["seeking_age_max"]: match_u1_to_u2 = False
        if user1_info.get("seeking_province") and user1_info["seeking_province"] != user2_info.get("province"): match_u1_to_u2 = False

        match_u2_to_u1 = True
        if user2_info.get("seeking_gender") and user2_info["seeking_gender"] != user1_info.get("gender"): match_u2_to_u1 = False
        if user2_info.get("seeking_age_min") and user1_info.get("age") and user1_info["age"] < user2_info["seeking_age_min"]: match_u2_to_u1 = False
        if user2_info.get("seeking_age_max") and user1_info.get("age") and user1_info["age"] > user2_info["seeking_age_max"]: match_u2_to_u1 = False
        if user2_info.get("seeking_province") and user2_info["seeking_province"] != user1_info.get("province"): match_u2_to_u1 = False

        if match_u1_to_u2 and match_u2_to_u1:
            potential_matches.append(u2)

    if potential_matches:
        
        u2 = potential_matches[0]
        queue.remove(u2)
        if u1 in queue: queue.remove(u1) 
        await connect_users(u1, u2)
        return True

    
    if u1 not in queue:
        queue.append(u1)
    return False


async def try_match_random():
    queue = DB["waiting_random"]
    while len(queue) >= 2:
        u1 = queue.popleft()
        
        
        
        if await try_match_users(queue, u1):
            continue
        else:
            queue.appendleft(u1) 
            break

async def try_match_gender():
    male_q = DB["waiting_gender"]["male"]
    female_q = DB["waiting_gender"]["female"]
    
    
    if not (male_q and female_q):
        return
    
    
    for male_user in list(male_q):
        if await try_match_users(female_q, male_user):
            if male_user in male_q:
                male_q.remove(male_user)


async def try_match_location(queue_name, key):
    queue = DB[queue_name][key]
    while len(queue) >= 2:
        u1 = queue.popleft()
        if await try_match_users(queue, u1):
            continue
        else:
            queue.appendleft(u1)
            break

async def try_match_interests():
    
    all_users_in_queues = set()
    for interest_queue in DB["waiting_interest"].values():
        all_users_in_queues.update(interest_queue)

    for u1 in list(all_users_in_queues):
        u1_interests = DB["user_info"][u1].get("interests", set())
        
        
        for u2 in list(all_users_in_queues):
            if u1 == u2 or is_blocked(u1, u2): continue

            u2_interests = DB["user_info"][u2].get("interests", set())
            
            
            if u1_interests.intersection(u2_interests):
                 
                 if await try_match_users(deque([u2]), u1):
                    
                    for interest in u1_interests:
                        if u1 in DB["waiting_interest"][interest]: DB["waiting_interest"][interest].remove(u1)
                    for interest in u2_interests:
                        if u2 in DB["waiting_interest"][interest]: DB["waiting_interest"][interest].remove(u2)
                    return 



def reset_user_state(uid: str):
    user_info = DB["user_info"][uid]
    user_info["status"] = "idle"
    user_info["profile_state"] = "none"
    user_info["admin_state"] = "none"
    queues = [
        DB["waiting_random"],
        DB["waiting_gender"]["male"],
        DB["waiting_gender"]["female"]
    ]
    dict_queues = [
        DB["waiting_province"],
        DB["waiting_city"],
        DB["waiting_interest"]
    ]
    for q in queues:
        if uid in q: q.remove(uid)     
    for dq in dict_queues:
        for key in list(dq.keys()):
            if uid in dq[key]:
                dq[key].remove(uid)
@bot.on_message()
async def message_handler(bot: Robot, msg: Message):
    uid = str(msg.chat_id)
    print(uid)
    text = msg.text.strip() if msg.text else ""
    user_info = DB["user_info"][uid]
    if not user_info.get("tg_first_name"):
        user_name = await bot.get_name(msg.chat_id) 
        user_info["tg_first_name"] = user_name or "Unknown"
        user_info["nickname"] = user_name or "ناشناس"
        logger.info(f"کاربر جدید: {uid} - نام: {user_name}")
        save_db()
    DB["online_users"][uid] = datetime.now()
    if user_info.get("is_banned", False):
        await msg.reply("شما توسط ادمین از ربات مسدود شده‌اید و اجازه استفاده ندارید.")
        return
    if uid == ADMIN_ID:
        if await handle_admin_command(bot, msg, text):
            return
    if text in [BTN_BACK, BTN_BACK_TO_MAIN] and user_info["status"] != "chatting":
        reset_user_state(uid)
        await send_main_menu(uid, "به منوی اصلی بازگشتید.")
        return
    if msg.file:
        if user_info["profile_state"] == "awaiting_photo":
            file_id = msg.file.file_id
            profile_dir = Path("profile_pics")
            profile_dir.mkdir(exist_ok=True)
            file_path = profile_dir / f"{uid}.jpg"
            try:
                await bot.download(file_id=file_id, save_as=str(file_path))
                user_info["profile_photo_path"] = str(file_path)
                user_info["profile_state"] = "editing_menu"
                save_db()
                await send_profile_editor_menu(uid, text="✅ عکس پروفایل شما با موفقیت آپلود شد.")
            except Exception as e:
                logger.error(f"خطا در دانلود عکس پروفایل برای {uid}: {e}")
                await msg.reply("❌ مشکلی در ذخیره عکس شما پیش آمد. لطفاً دوباره تلاش کنید.")
            return

        elif user_info["status"] == "chatting":
            peer = DB["active_chats"].get(uid)
            if peer:
                file_caption = msg.text if msg.text else ""
                try:
                    await bot.send_file(peer, file_id=msg.file.file_id, caption=file_caption)
                    await store_log("file_sent", uid, peer, msg.file.file_name, {"caption": file_caption})
                except Exception as e:
                    logger.error(f"Error sending file from {uid} to {peer}: {e}")
                    await msg.reply("❌ خطا در ارسال فایل به هم‌صحبت شما.")
            else:
                user_info["status"] = "idle"
                await send_main_menu(uid, "هم‌صحبت شما از چت خارج شده است. به منوی اصلی بازگشتید.")
            return
    if user_info["status"] == "chatting":
        peer = DB["active_chats"].get(uid)
        if not peer: 
            user_info["status"] = "idle"
            await send_main_menu(uid, "هم‌صحبت شما از چت خارج شده است. به منوی اصلی بازگشتید.")
            return
        if text == BTN_EXIT_CHAT:
            await disconnect_users(uid, "طرف مقابل چت را ترک کرد. 🚪")
        elif text == BTN_VIEW_PROFILE:
            profile_text = get_user_info_display(peer)
            photo_path = DB["user_info"][peer].get("profile_photo_path")
            if photo_path and os.path.exists(photo_path):
                try:
                    await bot.send_image(uid, path=photo_path, text=profile_text)
                except Exception as e:
                    logger.error(f"Error sending image for user {peer} to {uid}: {e}")
                    await msg.reply(f"در نمایش عکس پروفایل {DB['user_info'][peer].get('nickname', 'ناشناس')} مشکلی رخ داد.\n{profile_text}")
            else:
                await msg.reply(profile_text)
        elif text == BTN_BLOCK_USER:
            user_info.get("blocked_users", set()).add(peer)
            save_db()
            await disconnect_users(uid, f"🚫 کاربر '{user_info.get('nickname', 'ناشناس')}' شما را بلاک کرد و از چت خارج شد.",
                                   f"✅ کاربر '{DB['user_info'][peer].get('nickname', 'ناشناس')}' با موفقیت بلاک شد.")
        elif text == BTN_REPORT_USER:
            user_info["status"] = "awaiting_report_reason"
            user_info["last_peer"] = peer
            await msg.reply("لطفاً دلیل گزارش کاربر را بنویسید (حداکثر ۲۰۰ کاراکتر):\nبرای لغو /cancel را ارسال کنید.")
        else: 
            await bot.send_message(peer, text)
            await store_log("message_sent", uid, peer, text)
        return
    if user_info["status"] == "awaiting_report_reason":
        target_peer = user_info.get("last_peer")
        if text == "/cancel":
            user_info["status"] = "chatting" 
            await send_main_menu(uid, "گزارش لغو شد. به گفتگو بازگشتید.")
            return
        if target_peer and target_peer in DB["user_info"]:
            report_content = text[:MAX_REPORT_TEXT_LENGTH]
            report_id = await add_report(uid, target_peer, report_content)
            await msg.reply(f"✅ گزارش شما برای کاربر '{DB['user_info'][target_peer].get('nickname', 'ناشناس')}' با موفقیت ثبت شد (شماره گزارش: {report_id}). از همراهی شما سپاسگزاریم.")
            await disconnect_users(uid, f"🚩 کاربر مقابل به دلیل گزارش شما از چت خارج شد.",
                                   "شما به دلیل ارسال گزارش از چت خارج شدید.")
        else:
            await msg.reply("❌ متاسفانه هم‌صحبت شما دیگر در چت فعال نیست.")
            reset_user_state(uid)
            await send_main_menu(uid, "به منوی اصلی بازگشتید.")
        return
    if user_info["status"] == "rating":
        peer = user_info.get("last_peer")
        if peer and peer in DB["user_info"]:
            if text == BTN_RATE_POSITIVE:
                DB["user_info"][peer]["positive_ratings"] += 1
                await msg.reply("✅ امتیاز مثبت شما ثبت شد.")
            elif text == BTN_RATE_NEGATIVE:
                DB["user_info"][peer]["negative_ratings"] += 1
                await msg.reply("✅ امتیاز منفی شما ثبت شد.")
            elif text == BTN_SKIP_RATING:
                await msg.reply("امتیازدهی رد شد.")
            else:
                await msg.reply("❌ لطفاً یکی از دکمه‌های امتیازدهی را انتخاب کنید.")
                return 
            
            reset_user_state(uid)
            save_db()
            await send_main_menu(uid, "به منوی اصلی بازگشتید.")
        else:
            reset_user_state(uid)
            await send_main_menu(uid, "هم‌صحبت شما پیدا نشد. به منوی اصلی بازگشتید.")
        return
    profile_state = user_info.get("profile_state", "none")
    if profile_state == "awaiting_nickname":
        if 3 < len(text) < 50:
            user_info["nickname"] = text
            user_info["profile_state"] = "editing_menu"
            save_db()
            await send_profile_editor_menu(uid, f"✅ نام مستعار شما به '{text}' تغییر یافت.")
        else: await msg.reply("❌ نام مستعار باید بین ۳ تا ۵۰ کاراکتر باشد.")
        return
    if profile_state == "awaiting_age":
        if text.isdigit() and 12 <= int(text) <= 100:
            user_info["age"] = int(text)
            user_info["profile_state"] = "editing_menu"
            save_db()
            await send_profile_editor_menu(uid, f"✅ سن شما {text} سال ثبت شد.")
        else: await msg.reply("❌ سن باید یک عدد بین ۱۲ تا ۱۰۰ باشد.")
        return
    if profile_state == "awaiting_height":
        if text.isdigit() and 100 <= int(text) <= 250:
            user_info["height"] = int(text)
            user_info["profile_state"] = "editing_menu"
            save_db()
            await send_profile_editor_menu(uid, f"✅ قد شما {text} سانتی‌متر ثبت شد.")
        else: await msg.reply("❌ قد باید یک عدد بین ۱۰۰ تا ۲۵۰ باشد.")
        return
    if profile_state == "awaiting_province":
        user_info["province"] = text
        user_info["profile_state"] = "editing_menu"
        save_db()
        await send_profile_editor_menu(uid, f"✅ استان شما '{text}' ثبت شد.")
        return
    if profile_state == "awaiting_city":
        user_info["city"] = text
        user_info["profile_state"] = "editing_menu"
        save_db()
        await send_profile_editor_menu(uid, f"✅ شهر شما '{text}' ثبت شد.")
        return
    if profile_state == "awaiting_bio":
        if len(text) <= 500:
            user_info["bio"] = text
            user_info["profile_state"] = "editing_menu"
            save_db()
            await send_profile_editor_menu(uid, "✅ بیوگرافی شما با موفقیت ثبت شد.")
        else: await msg.reply("❌ بیوگرافی نباید بیش از ۵۰۰ کاراکتر باشد.")
        return

    if profile_state == "awaiting_interests":
        interests = {i.strip() for i in text.split(',') if i.strip()}
        user_info["interests"] = interests
        user_info["profile_state"] = "editing_menu"
        save_db()
        await send_profile_editor_menu(uid, "✅ علایق شما با موفقیت به‌روز شد.")
        return
        
    if profile_state == "awaiting_seeking_age":
        try:
            min_age, max_age = map(int, text.replace(" ", "").split('-'))
            if 12 <= min_age <= max_age <= 100:
                user_info["seeking_age_min"], user_info["seeking_age_max"] = min_age, max_age
                user_info["profile_state"] = "setting_seeking_prefs"
                save_db()
                await send_seeking_preferences_menu(uid, f"✅ محدوده سنی مورد نظر شما: {min_age}-{max_age} سال.")
            else: raise ValueError
        except (ValueError, TypeError):
            await msg.reply("❌ فرمت نامعتبر است. لطفاً به صورت `حداقل-حداکثر` وارد کنید (مثال: 18-25).")
        return
    if profile_state == "awaiting_seeking_province":
        user_info["seeking_province"] = text
        user_info["profile_state"] = "setting_seeking_prefs"
        save_db()
        await send_seeking_preferences_menu(uid, f"✅ استان مورد نظر شما: '{text}'.")
        return
    if text == "/start":
        if user_info["status"] == "chatting":
            await disconnect_users(uid, "❌ طرف مقابل ربات را مجدداً استارت کرد.")
        reset_user_state(uid)
        await send_main_menu(uid, "👋 سلام! به ربات چت ناشناس خوش آمدی.\nبرای شروع، یکی از گزینه‌ها را انتخاب کن:")
    elif text == "/profile" or text == BTN_EDIT_PROFILE:
        user_info["profile_state"] = "editing_menu"
        await send_profile_editor_menu(uid)
    elif text == BTN_RANDOM_CHAT and user_info["status"] == "idle":
        user_info["status"] = "waiting_random"
        DB["waiting_random"].append(uid)
        await send_main_menu(uid, "⏳ در حال جستجوی یک هم‌صحبت تصادفی... لطفاً شکیبا باشید.")
        asyncio.create_task(try_match_random())
    elif text == BTN_ONLINE_COUNT:
        await msg.reply(f"📊 هم اکنون {get_online_users_count()} کاربر فعال هستند.")
    elif text == BTN_CANCEL_SEARCH and user_info["status"].startswith("waiting"):
        reset_user_state(uid)
        await send_main_menu(uid, "✅ جستجو لغو شد.")
    elif text == BTN_ADVANCED_SEARCH:
        await send_advanced_search_menu(uid)
    elif text == BTN_SEARCH_GENDER:
        if not user_info.get("gender"):
            await msg.reply("❌ ابتدا باید جنسیت خود را در بخش 'پروفایل من' مشخص کنید.")
            return
        seeking_gender = "female" if user_info["gender"] == "male" else "male"
        user_info["seeking_gender"] = seeking_gender 
        user_info["status"] = "waiting_gender"
        DB["waiting_gender"][user_info["gender"]].append(uid)
        await send_main_menu(uid, f"⏳ در حال جستجوی هم‌صحبت '{'خانم' if seeking_gender=='female' else 'آقا'}'...")
        asyncio.create_task(try_match_gender())
    elif text == BTN_SEARCH_PROVINCE:
        province = user_info.get("province")
        if not province:
            await msg.reply("❌ ابتدا باید استان خود را در پروفایل ثبت کنید.")
            return
        user_info["status"] = f"waiting_province"
        DB["waiting_province"][province].append(uid)
        await send_main_menu(uid, f"⏳ در حال جستجوی هم‌صحبت از استان '{province}'...")
        asyncio.create_task(try_match_location("waiting_province", province))
    elif text == BTN_SEARCH_CITY:
        city = user_info.get("city")
        if not city:
            await msg.reply("❌ ابتدا باید شهر خود را در پروفایل ثبت کنید.")
            return
        user_info["status"] = f"waiting_city"
        DB["waiting_city"][city].append(uid)
        await send_main_menu(uid, f"⏳ در حال جستجوی هم‌صحبت از شهر '{city}'...")
        asyncio.create_task(try_match_location("waiting_city", city))
    elif text == BTN_SEARCH_INTERESTS:
        interests = user_info.get("interests")
        if not interests:
            await msg.reply("❌ ابتدا باید علایق خود را در پروفایل ثبت کنید.")
            return
        user_info["status"] = "waiting_interest"
        for interest in interests:
            DB["waiting_interest"][interest].append(uid)
        await send_main_menu(uid, f"⏳ در حال جستجوی هم‌صحبت با علایق مشترک...")
        asyncio.create_task(try_match_interests())
    elif user_info["profile_state"] == "editing_menu":
        if text == BTN_SET_NICKNAME:
            user_info["profile_state"] = "awaiting_nickname"
            await msg.reply("نام مستعار جدید خود را وارد کنید:")
        elif text == BTN_SET_AGE:
            user_info["profile_state"] = "awaiting_age"
            await msg.reply("سن خود را به عدد وارد کنید:")
        elif text == BTN_SET_GENDER:
            user_info["profile_state"] = "awaiting_gender_self"
            await send_gender_selection_menu(uid, "جنسیت خود را انتخاب کنید:", for_seeking=False)
        elif text == BTN_SET_PHOTO:
            user_info["profile_state"] = "awaiting_photo"
            await msg.reply("🖼️ عکس پروفایل جدید خود را ارسال کنید:")
        elif text == BTN_SEE_MY_INFO:
            await msg.reply(get_user_info_display(uid, for_admin=(uid == ADMIN_ID)))
        elif text == BTN_SET_SEEKING_PREFERENCES:
            user_info["profile_state"] = "setting_seeking_prefs"
            await send_seeking_preferences_menu(uid)
        else: 
            state_map = {
                BTN_SET_PROVINCE: ("awaiting_province", "استان"), BTN_SET_CITY: ("awaiting_city", "شهر"),
                BTN_SET_HEIGHT: ("awaiting_height", "قد"), BTN_SET_BIO: ("awaiting_bio", "بیوگرافی"),
                BTN_SET_INTERESTS: ("awaiting_interests", "علایق"),
            }
            if text in state_map:
                state, field_name = state_map[text]
                user_info["profile_state"] = state
                prompt = f"لطفاً {field_name} خود را وارد کنید"
                if state == "awaiting_interests":
                    current = ", ".join(user_info.get("interests", []))
                    prompt += f" (با کاما جدا کنید).\nعلایق فعلی: {current or 'ندارید'}"
                await msg.reply(prompt)
    elif text in [BTN_MALE, BTN_FEMALE, BTN_OTHER_GENDER]:
        gender_map = {BTN_MALE: "male", BTN_FEMALE: "female", BTN_OTHER_GENDER: "other"}
        selected_gender = gender_map[text]
        if user_info["profile_state"] == "awaiting_gender_self":
            user_info["gender"] = selected_gender
            user_info["profile_state"] = "editing_menu"
            save_db()
            await send_profile_editor_menu(uid, f"✅ جنسیت شما '{text}' ثبت شد.")
        elif user_info["profile_state"] == "awaiting_seeking_gender":
            user_info["seeking_gender"] = selected_gender
            user_info["profile_state"] = "setting_seeking_prefs"
            save_db()
            await send_seeking_preferences_menu(uid, f"✅ جنسیت مورد نظر شما '{text}' تعیین شد.")
    elif user_info["profile_state"] == "setting_seeking_prefs":
        if text == "جنسیت مورد نظر":
            user_info["profile_state"] = "awaiting_seeking_gender"
            await send_gender_selection_menu(uid, "جنسیت مورد نظر خود را برای جستجو انتخاب کنید:", for_seeking=True)
        elif text == "محدوده سنی":
            user_info["profile_state"] = "awaiting_seeking_age"
            await msg.reply("محدوده سنی مورد نظر را وارد کنید (مثال: 18-25):")
        elif text == "استان مورد نظر":
            user_info["profile_state"] = "awaiting_seeking_province"
            await msg.reply("نام استان مورد نظر را وارد کنید (برای حذف، `حذف` را بفرستید):")
        elif text == BTN_BACK:
            user_info["profile_state"] = "editing_menu"
            await send_profile_editor_menu(uid)
async def send_admin_panel(uid: str):
    builder = ChatKeypadBuilder()
    builder.row(builder.button(id="admin_stats", text=BTN_ADMIN_STATS))
    builder.row(builder.button(id="admin_broadcast", text=BTN_ADMIN_BROADCAST))
    builder.row(builder.button(id="admin_ban", text=BTN_ADMIN_BAN), builder.button(id="admin_unban", text=BTN_ADMIN_UNBAN))
    builder.row(builder.button(id="admin_user_info", text=BTN_ADMIN_USER_INFO), builder.button(id="admin_view_blocked", text=BTN_ADMIN_VIEW_BLOCKED))
    builder.row(builder.button(id="admin_view_reports", text=BTN_ADMIN_VIEW_REPORTS))
    builder.row(builder.button(id="admin_clear_queue", text=BTN_ADMIN_CLEAR_QUEUE))
    builder.row(builder.button(id="back_to_main", text=BTN_BACK_TO_MAIN))
    await bot.send_message(uid, "⚙️ به پنل مدیریت ربات خوش آمدید.", chat_keypad=builder.build(resize_keyboard=True))

async def handle_admin_command(bot: Robot, msg: Message, text: str) -> bool:
    uid = str(msg.chat_id)
    admin_info = DB["user_info"][uid]
    admin_state = admin_info.get("admin_state", "none")
    if admin_state == "awaiting_broadcast":
        admin_info["admin_state"] = "none"
        await msg.reply("⏳ در حال ارسال پیام همگانی...")
        success, failed = 0, 0
        for user_id in DB["user_info"]:
            try:
                await bot.send_message(user_id, f"📣 پیام از طرف مدیریت:\n\n{text}")
                success += 1
                await asyncio.sleep(0.05)
            except Exception as e:
                failed += 1
                logger.warning(f"Failed to send broadcast to {user_id}: {e}")
        await msg.reply(f"✅ پیام به {success} کاربر ارسال شد.\n❌ خطا در ارسال به {failed} کاربر.")
        return True
    if admin_state == "awaiting_ban_id":
        target_uid = text
        if target_uid in DB["user_info"]:
            DB["user_info"][target_uid]["is_banned"] = True
            save_db()
            await msg.reply(f"✅ کاربر {target_uid} با موفقیت مسدود شد.")
        else:
            await msg.reply("❌ کاربری با این شناسه یافت نشد.")
        admin_info["admin_state"] = "none"
        return True
    if admin_state == "awaiting_unban_id":
        target_uid = text
        if target_uid in DB["user_info"]:
            DB["user_info"][target_uid]["is_banned"] = False
            save_db()
            await msg.reply(f"✅ کاربر {target_uid} با موفقیت رفع مسدودی شد.")
        else:
            await msg.reply("❌ کاربری با این شناسه یافت نشد.")
        admin_info["admin_state"] = "none"
        return True
    if admin_state == "awaiting_user_info_id":
        target_uid = text
        if target_uid in DB["user_info"]:
            await msg.reply(get_user_info_display(target_uid, for_admin=True))
        else:
            await msg.reply("❌ کاربری با این شناسه یافت نشد.")
        admin_info["admin_state"] = "none"
        return True
    if admin_state == "awaiting_report_action":
        if text.lower() == "لغو":
            admin_info["admin_state"] = "none"
            await send_admin_panel(uid)
            return True
        try:
            report_id_to_resolve = int(text)
            report_found = None
            for r in DB["reports"]:
                if r["id"] == report_id_to_resolve and not r.get("resolved"):
                    report_found = r
                    break
            if report_found:
                report_found["resolved"] = True
                report_found["resolution_details"] = f"Resolved by admin {uid} at {datetime.now().isoformat()}"
                save_reports()
                reporter = report_found['reporter']
                reported_user = report_found['reported_user']
                await msg.reply(f"✅ گزارش شماره {report_id_to_resolve} برای کاربر `{reported_user}` رسیدگی شد.")
                try: 
                    await bot.send_message(reporter, f"کاربر گرامی، گزارش شما با شماره {report_id_to_resolve} بررسی و توسط ادمین رسیدگی شد. از همکاری شما سپاسگزاریم.")
                except Exception: pass
            else:
                await msg.reply(f"❌ گزارش رسیدگی نشده با شماره {report_id_to_resolve} یافت نشد.")
        except ValueError:
            await msg.reply("❌ لطفاً یک شماره گزارش معتبر وارد کنید.")
        admin_info["admin_state"] = "none"
        return True
    if text == "/admin" or text == BTN_GO_TO_ADMIN:
        await send_admin_panel(uid)
        return True
    if text == BTN_ADMIN_STATS:
        total_users = len(DB['user_info'])
        active_chats_count = len(DB['active_chats']) // 2
        unresolved_reports = sum(1 for r in DB.get('reports', []) if not r.get('resolved'))
        await msg.reply(
            f"📊 آمار ربات:\n\n"
            f"👤 کل کاربران: {total_users}\n"
            f"🟢 آنلاین (۵ دقیقه اخیر): {get_online_users_count()}\n"
            f"💬 چت‌های فعال: {active_chats_count}\n"
            f"🚩 گزارشات رسیدگی نشده: {unresolved_reports} / {len(DB.get('reports',[]))}"
        )
        return True
    if text == BTN_ADMIN_BROADCAST:
        admin_info["admin_state"] = "awaiting_broadcast"
        await msg.reply("پیام خود برای ارسال به همه کاربران را وارد کنید:")
        return True
    if text == BTN_ADMIN_BAN:
        admin_info["admin_state"] = "awaiting_ban_id"
        await msg.reply("شناسه کاربری فرد مورد نظر برای مسدودسازی را وارد کنید:")
        return True
    if text == BTN_ADMIN_UNBAN:
        admin_info["admin_state"] = "awaiting_unban_id"
        await msg.reply("شناسه کاربری فرد مورد نظر برای رفع مسدودی را وارد کنید:")
        return True
    if text == BTN_ADMIN_USER_INFO:
        admin_info["admin_state"] = "awaiting_user_info_id"
        await msg.reply("شناسه کاربری فرد مورد نظر را وارد کنید:")
        return True
    if text == BTN_ADMIN_VIEW_REPORTS:
        unresolved_reports = [r for r in DB["reports"] if not r.get("resolved")]
        if not unresolved_reports:
            await msg.reply("هیچ گزارش رسیدگی نشده‌ای وجود ندارد.")
            return True
        response = "📜 لیست گزارش‌های رسیدگی نشده:\n\n"
        for r in unresolved_reports:
            response += (
                f"ID: {r['id']}\n"
                f"  - گزارش دهنده: `{r['reporter']}`\n"
                f"  - گزارش شده: `{r['reported_user']}`\n"
                f"  - دلیل: `{r['reason']}`\n\n"
            )
        response += "لطفاً شماره گزارشی که می‌خواهید رسیدگی کنید را وارد نمایید یا `لغو` را بفرستید."
        admin_info["admin_state"] = "awaiting_report_action"
        await msg.reply(response)
        return True
    if text == BTN_ADMIN_CLEAR_QUEUE:
        waiting_users = set()
        cleared_count = len(waiting_users)
        for user_id in waiting_users:
            reset_user_state(user_id)
        await msg.reply(f"✅ صف‌های انتظار با موفقیت پاکسازی شدند. ({cleared_count} کاربر حذف شد).")
        return True
    if text == BTN_ADMIN_VIEW_BLOCKED:
        blocked_list = [f"`{uid}` ({info.get('nickname')})" for uid, info in DB["user_info"].items() if info.get('is_banned')]
        if not blocked_list:
            await msg.reply("هیچ کاربری مسدود نیست.")
        else:
            await msg.reply("👥 لیست کاربران مسدود:\n" + "\n".join(blocked_list))
        return True
    return False
async def main():
    global bot
    load_db()
    load_reports()
    await bot.set_commands([
        {"command": "start", "description": "شروع به کار با ربات"},
        {"command": "profile", "description": "ویرایش پروفایل شخصی"}
    ])
    me = await bot.get_me()
    logger.info(f"Run {me.data.bot.bot_title})")
    await bot.run()
asyncio.run(main())
