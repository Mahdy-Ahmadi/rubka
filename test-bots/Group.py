from rubka.asynco import Robot, Message, filters
import sqlite3,time
import random,asyncio
bot = Robot("",max_msg_age=2000,safeSendMode=True)
bot.start_save_message()

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    chat_id TEXT PRIMARY KEY,
    owner_id TEXT,
    active INTEGER DEFAULT 1
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS mutes (
    chat_id TEXT,
    user_id TEXT,
    mute_time INTEGER,
    mute_duration INTEGER,
    is_permanent INTEGER,
    PRIMARY KEY (chat_id, user_id)
)
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    chat_id TEXT,
    user_id TEXT,
    PRIMARY KEY (chat_id, user_id)
)
""")
conn.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS mutes (
    chat_id TEXT,
    user_id TEXT,
    PRIMARY KEY (chat_id, user_id)
)
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS rules (
    chat_id TEXT,
    rule_key TEXT,
    rule_value INTEGER,
    PRIMARY KEY (chat_id, rule_key)
)
""")
conn.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS group_lock (
    chat_id TEXT PRIMARY KEY,
    is_locked INTEGER DEFAULT 0
)
""")
conn.commit()

def toggle_group_lock(chat_id, is_locked):
    cursor.execute(
        "INSERT OR REPLACE INTO group_lock (chat_id, is_locked) VALUES (?, ?)",
        (chat_id, is_locked)
    )
    conn.commit()

def is_group_locked(chat_id):
    cursor.execute("SELECT is_locked FROM group_lock WHERE chat_id=?", (chat_id,))
    result = cursor.fetchone()
    return result and result[0] == 1
def save_member(chat_id, user_id):
    cursor.execute(
        "INSERT OR IGNORE INTO members (chat_id, user_id) VALUES (?, ?)",
        (chat_id, user_id)
    )
    conn.commit()
def get_members(chat_id):
    cursor.execute(
        "SELECT user_id FROM members WHERE chat_id=?",
        (chat_id,)
    )
    return [i[0] for i in cursor.fetchall()]

TAG_TEXTS,rules_config,RULES_FA = [
    "کجایی رفتی؟",
    "آنلاین نمیشی چرا؟",
    "یه سر بیا!",
    "چرا همیشه دیر میای؟",
    "کی برمی‌گردی؟",
    "هیچ خبری ازت نیست!",
    "منتظرت بودیم!",
    "دیر کردی بیا!",
    "یه پیامی بده دیگه!",
    "گروه رو با بی‌خبری ترک کردی!",
    "باز هم غیب شدی؟",
    "حواست کجاست؟",
    "کجا رفته‌ای که پیدات نمی‌کنیم؟",
    "چرا هیچ‌وقت آنلاین نمی‌شی؟",
    "چطور همیشه ناپدید می‌شی؟",
    "کجایید که هیچ خبری ازتون نیست؟",
    "گروه بدون شما خیلی بی‌روح شده!",
    "منتظریم بیای، خب!",
    "هیچ خبری ازت نیست!",
    "تو که همیشه می‌اومدی، چرا الان نیستی؟",
    "دلمون تنگ شده، بیا دیگه!",
    "منتظر خبری ازت هستیم!",
    "کی از ما خبر می‌گیری؟",
    "گروه بدون شما هیچ جذابیتی نداره!",
    "حواست کجاست که خبری ازت نیست؟",
    "کجا گم شدی؟",
    "بی‌خبری چه معنی می‌ده؟",
    "هرجا که هستی، بیا دیگه!",
    "گروه رو بدون تو نمی‌چرخونه!",
    "یادت رفته گروه رو؟",
    "منتظریم تو بیای تا بحث رو ادامه بدیم!",
    "پیدات نمی‌کنیم اصلاً!",
    "یادته که هنوز اینجا منتظریم؟",
    "منتظریم یه علامت ازت ببینیم!",
    "گروه بدون تو سوت و کوره!",
    "حتی یک پیام هم نمی‌فرستی؟",
    "آیا هنوز تو گروهی؟",
    "کی میای که ادامه بدیم؟",
    "یه سر بزن دیگه!",
    "کی میای تو گروه فعال بشی؟",
    "ما هنوز هم منتظریم!",
    "گروه با حضور تو تکمیل میشه!",
    "ما رو تنها گذاشتی؟",
    "چرا خبری ازت نیست؟",
    "مگه قرار نبود همیشه آنلاین باشی؟"
    "چرا غیب زدی؟",
    "بی‌خبر نرو!",
    "خبری ازت نیست!",
    "پیدات نمیشه اصلاً!",
    "کجا گم شدی؟",
    "دلمون برات تنگ شده!",
    "همیشه غایبی!",
    "چرا جواب نمیدی؟",
    "منتظریم بیای!",
    "کی برمی‌گردی؟",
    "یه پیام بده!",
    "سرت شلوغه؟",
    "حواست به ما نیست!",
    "گروه بدون تو سوت و کوره!",
    "کلاً ناپدید شدی!",
    "چرا سر نمی‌زنی؟",
    "آنلاین میشی یا نه؟",
    "یه علامت بده زنده‌ای!",
    "بازم نیستی!",
    "ما رو یادت رفته؟",
    "چرا اینقدر ساکتی؟",
    "یه سر بزن خب!",
    "کجایی که نیستی؟",
    "تو که همیشه میومدی!",
    "گروه رو ول کردی؟",
    "غیب کامل زدی!",
    "دیگه نمیای؟",
    "منتظر ظهورتیم!",
    "کجایی آخه؟",
    "دلت برای گروه تنگ نشده؟",
    "پیدات نمی‌کنیم!",
    "یه خبری از خودت بده!"
],{
    "link": True,
    "mention": True,
    "hashtag": False,
    "emoji": False,
    "only_emoji": False,
    "number": False,
    "command": False,
    "metadata": True,
    "bold": False,
    "italic": False,
    "underline": False,
    "strike": False,
    "quote": False,
    "spoiler": False,
    "code": False,
    "mono": False,
    "photo": False,
    "video": False,
    "audio": False,
    "voice": False,
    "music": False,
    "document": False,
    "archive": False,
    "executable": False,
    "font": False,
    "sticker": False,
    "forward": True,
    "contact": False,
    "location": False,
    "live_location": False,
    "poll": False,
    "anti_flood": True,
    "gif":True
},{
    "link": "لینک",
    "mention": "منشن",
    "hashtag": "هشتگ",
    "emoji": "ایموجی",
    "only_emoji": "فقط ایموجی",
    "number": "عدد",
    "command": "دستور",
    "metadata": "متادیتا",
    "bold": "بولد",
    "italic": "ایتالیک",
    "underline": "زیرخط",
    "strike": "خط خورده",
    "quote": "کوت",
    "spoiler": "اسپویلر",
    "code": "کد",
    "mono": "مونواسپیس",
    "photo": "عکس",
    "video": "ویدیو",
    "audio": "صوت",
    "voice": "ویس",
    "music": "موزیک",
    "document": "فایل",
    "archive": "فایل فشرده",
    "executable": "فایل اجرایی",
    "font": "فونت",
    "sticker": "استیکر",
    "forward": "فوروارد",
    "contact": "شماره تماس",
    "location": "لوکیشن",
    "live_location": "لوکیشن زنده",
    "poll": "نظرسنجی",
    "anti_flood": "کد هنگی",
    "gif":"گیف"
}
def mute_user_db(chat_id, user_id):
    cursor.execute(
        "INSERT OR IGNORE INTO mutes (chat_id, user_id) VALUES (?, ?)",
        (chat_id, user_id)
    )
    conn.commit()

def unmute_user_db(chat_id, user_id):
    cursor.execute(
        "DELETE FROM mutes WHERE chat_id=? AND user_id=?",
        (chat_id, user_id)
    )
    conn.commit()

def is_muted(chat_id, user_id):
    cursor.execute(
        "SELECT 1 FROM mutes WHERE chat_id=? AND user_id=?",
        (chat_id, user_id)
    )
    return cursor.fetchone() is not None

def get_muted_users(chat_id):
    cursor.execute(
        "SELECT user_id FROM mutes WHERE chat_id=?",
        (chat_id,)
    )
    return [i[0] for i in cursor.fetchall()]

def chat_exists(chat_id):
    cursor.execute("SELECT 1 FROM chats WHERE chat_id=?", (chat_id,))
    return cursor.fetchone()
def set_owner(chat_id, user_id):
    cursor.execute(
        "INSERT INTO chats (chat_id, owner_id) VALUES (?, ?)",
        (chat_id, user_id)
    )
    for k, v in rules_config.items():
        cursor.execute(
            "INSERT INTO rules (chat_id, rule_key, rule_value) VALUES (?, ?, ?)",
            (chat_id, k, int(v))
        )
    conn.commit()
def is_owner(chat_id, user_id):
    cursor.execute(
        "SELECT 1 FROM chats WHERE chat_id=? AND owner_id=?",
        (chat_id, user_id)
    )
    return cursor.fetchone() is not None
def random_tag_text():
    return random.choice(TAG_TEXTS)
def load_rules(chat_id):
    cursor.execute("SELECT rule_key, rule_value FROM rules WHERE chat_id=?", (chat_id,))
    return {k: bool(v) for k, v in cursor.fetchall()}
def toggle_rule(chat_id, rule):
    cursor.execute(
        "UPDATE rules SET rule_value = NOT rule_value WHERE chat_id=? AND rule_key=?",
        (chat_id, rule)
    )
    conn.commit()
def set_all_rules(chat_id, value: bool):
    cursor.execute(
        "UPDATE rules SET rule_value=? WHERE chat_id=?",
        (int(value), chat_id)
    )
    conn.commit()
@bot.on_message(filters.text_contains("قفل گروه"))
async def lock_group(bot: Robot, message: Message):
    if not is_owner(message.chat_id, message.sender_id):return
    try:
        parts = message.text.split()
        if len(parts) >= 3 and parts[2].isdigit():lock_duration = int(parts[2])
        else:return await message.reply("❗ لطفا مدت زمان قفل گروه را به درستی وارد کنید.")
        toggle_group_lock(message.chat_id, 1)
        await message.reply(f"✅ گروه به مدت {lock_duration} ثانیه قفل شد.")
        await asyncio.sleep(lock_duration)
        toggle_group_lock(message.chat_id, 0)
        await message.reply("✅ مدت زمان قفل گروه تمام شد. قفل گروه باز شد.")
        
    except ValueError:
        await message.reply("❗ لطفا مدت زمان قفل گروه را به درستی وارد کنید.")


@bot.on_message(filters.text_equals("باز کردن قفل گروه"))
async def unlock_group(bot: Robot, message: Message):
    if not is_owner(message.chat_id, message.sender_id):return
    toggle_group_lock(message.chat_id, 0)
    await message.reply("✅ قفل گروه باز شد. پیام‌ها قابل ارسال هستند.")

@bot.on_message()
async def check_group_lock(bot: Robot, message: Message):
    if not chat_exists(message.chat_id):return
    if is_group_locked(message.chat_id):
        await message.delete()
@bot.on_message()
async def user_message(bot, message: Message):
    if not chat_exists(message.chat_id):
        return
    save_member(message.chat_id, message.sender_id)
    cursor.execute("SELECT mute_time, mute_duration, is_permanent FROM mutes WHERE chat_id=? AND user_id=?", (message.chat_id, message.sender_id))
    mute_info = cursor.fetchone()
    if mute_info:
        mute_time, mute_duration, is_permanent = mute_info
        if is_permanent == 1:
            await message.delete()
            return
        import time
        remaining_time = mute_time + mute_duration - int(time.time())
        if remaining_time > 0:
            await message.delete()
        else:
            cursor.execute("DELETE FROM mutes WHERE chat_id=? AND user_id=?", (message.chat_id, message.sender_id))
            conn.commit()

@bot.on_message(filters.text_equals("تگ"))
async def tag_users(bot:Robot, message: Message):
    if not is_owner(message.chat_id, message.sender_id):return False
    members = get_members(message.chat_id)
    if not members:return await message.reply("❗ کاربری ذخیره نشده")
    chunk_size = 20
    chunks = [members[i:i + chunk_size] for i in range(0, len(members), chunk_size)]
    for group in chunks:
        text = " , ".join(
    f"[{random_tag_text()}]({uid})"
    for uid in group
)
        await bot.send_message(
            chat_id=message.chat_id,
            text=text,
            reply_to_message_id=message.message_id
        )
@bot.on_message()
async def mute_user(bot: Robot, message: Message):
    if not message.text.startswith("سکوت"): return
    if not is_owner(message.chat_id, message.sender_id):
        return
    try:
        parts = message.text.split()
        if len(parts) == 2:
            try:
                mute_duration = int(parts[1])  
                is_permanent = 0  
            except ValueError:
                if parts[1].lower() == "دائمی":
                    mute_duration = 0 
                    is_permanent = 1
                else:
                    return await message.reply("❗ لطفا مدت زمان سکوت یا 'دائمی' را وارد کنید.")
        elif len(parts) == 3 and parts[1].lower() == "دائمی":
            mute_duration = 0 
            is_permanent = 1
        else:
            return await message.reply("❗ لطفا مدت زمان سکوت یا 'دائمی' را وارد کنید.")
        info = await bot.get_message(message.chat_id, message.reply_to_message_id)
        target_id = info["sender_id"]
        cursor.execute(
            "INSERT OR REPLACE INTO mutes (chat_id, user_id, mute_time, mute_duration, is_permanent) VALUES (?, ?, ?, ?, ?)",
            (message.chat_id, target_id, int(time.time()), mute_duration, is_permanent)
        )
        conn.commit()
        if is_permanent:
            await message.reply(f"✅ [کاربر]({target_id}) برای همیشه سکوت شد.")
        else:
            await message.reply(f"✅ [کاربر]({target_id}) برای {mute_duration} ثانیه سکوت شد.")
        if mute_duration > 0:
            await asyncio.sleep(mute_duration)
            cursor.execute("DELETE FROM mutes WHERE chat_id=? AND user_id=?", (message.chat_id, target_id))
            conn.commit()
            await message.reply(f"⏳ مدت زمان سکوت برای کاربر [کاربر]({target_id}) تمام شد.")
    except ValueError as e:
        print(e)
        await message.reply("❗ لطفا مدت زمان سکوت را به درستی وارد کنید.")

@bot.on_message(filters.text_equals("پاکسازی سکوت"))
async def clear_mute_list(bot: Robot, message: Message):
    if not is_owner(message.chat_id, message.sender_id):return
    cursor.execute("DELETE FROM mutes WHERE chat_id=?", (message.chat_id,))
    conn.commit()
    await message.reply("✅ لیست سکوت پاک شد")

@bot.on_message(filters.text_equals("حذف سکوت"))
async def unmute_command(bot: Robot, message: Message):
    if not is_owner(message.chat_id, message.sender_id):
        return
    if not message.reply_to_message_id:
        return await message.reply("❗ روی پیام کاربر ریپلای کن")
    info = await bot.get_message(message.chat_id, message.reply_to_message_id)
    target_id = info["sender_id"]
    unmute_user_db(message.chat_id, target_id)
    await message.reply(f"🔊 سکوت [کاربر]({target_id}) برداشته شد")
@bot.on_message(filters.text_equals("لیست سکوت"))
async def mute_list(bot: Robot, message: Message):
    if not is_owner(message.chat_id, message.sender_id):
        return
    users = get_muted_users(message.chat_id)
    if not users:
        return await message.reply("✅ لیست سکوت خالی است")
    text = "🔇**کاربران سکوت‌شده** :\n\n"
    text += "\n".join(f">- [کاربر]({uid})" for uid in users)
    await message.reply(text)

@bot.on_message(filters.text_contains_any(["نصب", "فعال", "مالک"]))
async def install(bot, message: Message):
    if chat_exists(message.chat_id):
        return False
    set_owner(message.chat_id, message.sender_id)
    await message.reply(
        f"✅ ربات در گروه {await message.name} نصب شد\n"
        "👑 شما مالک این چت هستید"
    )

def check_rules(message: Message, rules: dict):
    violations = []
    if rules.get("link") and message.has_link:violations.append("لینک")
    if rules.get("mention") and message.is_mention:violations.append("منشن")
    if rules.get("hashtag") and message.is_hashtag:violations.append("هشتگ")
    if rules.get("emoji") and message.is_emoji:violations.append("ایموجی")
    if rules.get("only_emoji") and message.is_pure_emoji:violations.append("فقط ایموجی")
    if rules.get("number") and message.is_number:violations.append("عدد")
    if rules.get("command") and message.is_command:violations.append("استفاده از دستور")
    if rules.get("metadata") and message.has_metadata:violations.append("متادیتا")
    if rules.get("bold") and message.is_bold:violations.append("متن بولد")
    if rules.get("italic") and message.is_italic:violations.append("متن ایتالیک")
    if rules.get("underline") and message.is_underline:violations.append("زیرخط")
    if rules.get("strike") and message.is_strike:violations.append("خط خورده")
    if rules.get("quote") and message.is_quote:violations.append("کوت")
    if rules.get("spoiler") and message.is_spoiler:violations.append("اسپویلر")
    if rules.get("code") and message.is_pre:violations.append("کد")
    if rules.get("mono") and message.is_mono:violations.append("مونواسپیس")
    if rules.get("photo") and message.is_photo:violations.append("عکس")
    if rules.get("video") and message.is_video:violations.append("ویدیو")
    if rules.get("audio") and message.is_audio:violations.append("صوت")
    if rules.get("voice") and message.is_voice:violations.append("ویس")
    if rules.get("music") and message.is_music:violations.append("موزیک")
    if rules.get("document") and message.is_document:violations.append("سند / فایل")
    if rules.get("archive") and message.is_archive:violations.append("فایل فشرده")
    if rules.get("executable") and message.is_executable:violations.append("فایل اجرایی")
    if rules.get("font") and message.is_font:violations.append("فونت")
    if rules.get("sticker") and message.sticker:violations.append("استیکر")
    if rules.get("forward") and message.is_forwarded:violations.append("فوروارد")
    if rules.get("contact") and message.is_contact:violations.append("شماره تماس")
    if rules.get("location") and message.is_location:violations.append("لوکیشن")
    if rules.get("live_location") and message.is_live_location:violations.append("لوکیشن زنده")
    if rules.get("poll") and message.is_poll:violations.append("نظرسنجی")
    if rules.get("gif") and message.is_gif:violations.append("گیف")
    if rules.get("anti_flood") and message.text:
        if message.text.count(".") >= 40:violations.append("کد هنگی")
    return violations

@bot.on_message()
async def user_message(bot, message: Message):
    if not chat_exists(message.chat_id):
        return
    if is_owner(message.chat_id, message.sender_id):
        return
    rules = load_rules(message.chat_id)
    violations = check_rules(message, rules)
    if violations:
        await message.reply(
                f"⛔ **اخطار**\n"
                f">درود [کاربر]({message.sender_id}) عزیز\n"
                f"📌 دلیل : {' و '.join(violations)}\n",
                30
            )
        await message.delete()

@bot.on_message()
async def info(bot, message):
    text = message.text.strip()
    reply_id = message.reply_to_message_id
    if text in ["get", "اطلاعات", "info"] and reply_id:
            info = await bot.get_message(message.chat_id, reply_id)
            return await bot.send_message(chat_id=message.chat_id, text=f"**اطلاعات پیام:**\n>{info}", reply_to_message_id=reply_id)

@bot.on_message()
async def admin_commands(bot, message: Message):
    if not is_owner(message.chat_id, message.sender_id):
        return
    text = message.text.strip()
    if text == "وضعیت":
        rules = load_rules(message.chat_id)
        state = "\n".join(
            f"> {RULES_FA[k]}: {'✅ روشن' if v else '❌ خاموش'}"
            for k, v in rules.items()
        )
        return await message.reply(
            f"📊 وضعیت قوانین گروه :\n\n{state}"
        )
    if text == "خاموش همه":
        set_all_rules(message.chat_id, False)
        return await message.reply("🔕 همه قوانین خاموش شدند")
    if text == "روشن همه":
        set_all_rules(message.chat_id, True)
        return await message.reply("🔔 همه قوانین روشن شدند")
    for k, fa in RULES_FA.items():
        if text in [fa, f"قفل {fa}"]:
            toggle_rule(message.chat_id, k)
            return await message.reply(f"✔️ وضعیت **{fa}** تغییر کرد")
bot.run(sleep_time=0)
