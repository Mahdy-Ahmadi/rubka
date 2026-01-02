from rubka import Robot, Message, filters
import time,random,asyncio,re,aiohttp,asyncio,jdatetime,aiosqlite



Token = "Token"  #توکن ربات
Data_name = "botdatabase.db"
db_lock = asyncio.Lock()


bot = Robot(Token,max_msg_age=2000,safeSendMode=True)

bot.start_save_message()
async def connect_db():return await aiosqlite.connect(Data_name)
async def create_tables():
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute("PRAGMA journal_mode=WAL;")
        await cursor.execute("PRAGMA synchronous=NORMAL;")
        
        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id TEXT,
            user_id TEXT PRIMARY KEY
        )
        """)
        await db.commit()

        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS speaker_mode (
            chat_id TEXT PRIMARY KEY,
            is_enabled INTEGER DEFAULT 0
        )
        """)
        await db.commit()

        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS warning_threshold (
            chat_id TEXT PRIMARY KEY,
            threshold INTEGER DEFAULT 10
        )
        """)
        await db.commit()

        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS strict_mode (
            chat_id TEXT PRIMARY KEY,
            enabled INTEGER DEFAULT 0
        )
        """)
        await db.commit()

        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            chat_id TEXT PRIMARY KEY,
            owner_id TEXT,
            active INTEGER DEFAULT 1
        )
        """)
        await db.commit()

        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS mutes (
            chat_id TEXT,
            user_id TEXT,
            mute_time INTEGER,
            mute_duration INTEGER,
            is_permanent INTEGER,
            PRIMARY KEY (chat_id, user_id)
        )
        """)
        await db.commit()

        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            chat_id TEXT,
            user_id TEXT,
            warning_count INTEGER DEFAULT 0,
            PRIMARY KEY (chat_id, user_id)
        )
        """)
        await db.commit()

        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            chat_id TEXT,
            user_id TEXT,
            PRIMARY KEY (chat_id, user_id)
        )
        """)
        await db.commit()

        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS rules (
            chat_id TEXT,
            rule_key TEXT,
            rule_value INTEGER,
            PRIMARY KEY (chat_id, rule_key)
        )
        """)
        await db.commit()

        await cursor.execute("DROP TABLE IF EXISTS user_stats")
        await cursor.execute("""
        CREATE TABLE user_stats (
            chat_id TEXT,
            user_id TEXT,
            message_count INTEGER DEFAULT 0,
            date INTEGER,
            PRIMARY KEY (chat_id, user_id)
        )
        """)
        await db.commit()

        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS group_lock (
            chat_id TEXT PRIMARY KEY,
            is_locked INTEGER DEFAULT 0
        )
        """)
        await db.commit()

        await cursor.execute("PRAGMA foreign_keys=off;")
        await db.commit()

        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            chat_id TEXT,
            user_id TEXT,
            PRIMARY KEY (chat_id, user_id)
        )
        """)
        await db.commit()

        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            chat_id TEXT,
            message_id INTEGER,
            timestamp INTEGER,
            PRIMARY KEY (chat_id, message_id)
        )
        """)
        await db.commit()

async def set_strict_mode(chat_id, value: bool):
    db = await connect_db()
    async with db.cursor() as cursor:
        
        await cursor.execute(
            "INSERT OR REPLACE INTO strict_mode (chat_id, enabled) VALUES (?, ?)",
            (chat_id, int(value))
        )
        await db.commit()

async def is_strict_mode(chat_id):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute(
            "SELECT enabled FROM strict_mode WHERE chat_id=?",
            (chat_id,)
        )
        row = await cursor.fetchone()
        return row and row[0] == 1

async def add_admin(chat_id, user_id):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute(
            "INSERT OR IGNORE INTO admins (chat_id, user_id) VALUES (?, ?)",
            (chat_id, user_id)
        )
        await db.commit()

async def remove_admin(chat_id, user_id):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute(
            "DELETE FROM admins WHERE chat_id=? AND user_id=?",
            (chat_id, user_id)
        )
        await db.commit()

async def is_admin(chat_id, user_id):
    if await is_owner(chat_id, user_id):
        return True
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute(
            "SELECT 1 FROM admins WHERE chat_id=? AND user_id=?",
            (chat_id, user_id)
        )
        return await cursor.fetchone() is not None

async def toggle_group_lock(chat_id, is_locked):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute(
            "INSERT OR REPLACE INTO group_lock (chat_id, is_locked) VALUES (?, ?)",
            (chat_id, is_locked)
        )
        await db.commit()

async def is_group_locked(chat_id):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute("SELECT is_locked FROM group_lock WHERE chat_id=?", (chat_id,))
        result = await cursor.fetchone()
        return result and result[0] == 1

async def save_member(chat_id, user_id):
    attempt_count = 0
    while attempt_count < 3:
        try:
            db = await connect_db()
            async with db.cursor() as cursor:
                await cursor.execute(
                    "INSERT OR IGNORE INTO members (chat_id, user_id) VALUES (?, ?)",
                    (chat_id, user_id)
                )
                await db.commit()
            await db.close()
            break
        except aiosqlite.OperationalError as e:
            print(f"Database is locked. Attempt {attempt_count + 1}/3...")
            attempt_count += 1
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break
    else:print("Failed to save member after 3 attempts.")

async def get_members(chat_id):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute(
            "SELECT user_id FROM members WHERE chat_id=?",
            (chat_id,)
        )
        members = await cursor.fetchall()
        return [i[0] for i in members]

async def increase_message_count(chat_id, user_id):
    try:
        db = await connect_db()
        async with db.cursor() as cursor:
            await db.execute('BEGIN TRANSACTION')
            try:
                await cursor.execute("""
                INSERT INTO user_stats (chat_id, user_id, message_count, date)
                VALUES (?, ?, 1, ?)
                ON CONFLICT(chat_id, user_id)
                DO UPDATE SET message_count = message_count + 1, date = ?
                """, (chat_id, user_id, int(time.time()), int(time.time())))
                await db.commit()
            except aiosqlite.DatabaseError as e:
                await db.rollback()
                print(f"Database error occurred: {e}")
    except Exception as e:print(f"An unexpected error occurred: {e}")
    finally:await db.close()

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

async def mute_user_db(chat_id, user_id):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute(
            "INSERT OR IGNORE INTO mutes (chat_id, user_id) VALUES (?, ?)",
            (chat_id, user_id)
        )
        await db.commit()

async def unmute_user_db(chat_id, user_id):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute(
            "DELETE FROM mutes WHERE chat_id=? AND user_id=?",
            (chat_id, user_id)
        )
        await db.commit()

async def is_muted(chat_id, user_id):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute(
            "SELECT 1 FROM mutes WHERE chat_id=? AND user_id=?",
            (chat_id, user_id)
        )
        return await cursor.fetchone() is not None

async def get_muted_users(chat_id):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute(
            "SELECT user_id FROM mutes WHERE chat_id=?",
            (chat_id,)
        )
        muted_users = await cursor.fetchall()
        return [i[0] for i in muted_users]

async def chat_exists(chat_id):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute("SELECT 1 FROM chats WHERE chat_id=?", (chat_id,))
        return await cursor.fetchone()

async def set_owner(chat_id, user_id):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute(
            "INSERT INTO chats (chat_id, owner_id) VALUES (?, ?)",
            (chat_id, user_id)
        )
        for k, v in rules_config.items():
            await cursor.execute(
                "INSERT INTO rules (chat_id, rule_key, rule_value) VALUES (?, ?, ?)",
                (chat_id, k, int(v))
            )
        await db.commit()

async def is_owner(chat_id, user_id):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute(
            "SELECT 1 FROM chats WHERE chat_id=? AND owner_id=?",
            (chat_id, user_id)
        )
        result = await cursor.fetchone()
        return result is not None

async def random_tag_text():
    return random.choice(TAG_TEXTS)

async def load_rules(chat_id):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute("SELECT rule_key, rule_value FROM rules WHERE chat_id=?", (chat_id,))
        return {k: bool(v) for k, v in await cursor.fetchall()}

async def toggle_rule(chat_id, rule):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute(
            "UPDATE rules SET rule_value = NOT rule_value WHERE chat_id=? AND rule_key=?",
            (chat_id, rule)
        )
        await db.commit()

async def set_all_rules(chat_id, value: bool):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute(
            "UPDATE rules SET rule_value=? WHERE chat_id=?",
            (int(value), chat_id)
        )
        await db.commit()

@bot.on_message()
async def save_message_to_db(bot: Robot, message: Message):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute("""
        INSERT OR REPLACE INTO messages (chat_id, message_id, timestamp)
        VALUES (?, ?, ?)
        """, (message.chat_id, message.message_id, int(time.time())))
        await db.commit()

@bot.on_message()
async def speaker_reply(bot: Robot, message: Message):
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute("SELECT is_enabled FROM speaker_mode WHERE chat_id=?", (message.chat_id,))
        is_enabled = await cursor.fetchone()
        if is_enabled and is_enabled[0] == 1:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.rubka.ir/ans/?text={message.text}") as response:
                    data = await response.json()
            if data.get("response"):
                await message.reply(data["response"])

@bot.on_message(filters.text_equals("بن"))
async def ban_user(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    if not message.reply_to_message_id:
        await message.reply("⚠️ لطفاً روی پیام کاربر مورد نظر ریپلای کنید.")
        return
    data = await bot.get_message(
        chat_id=message.chat_id,
        message_id=message.reply_to_message_id
    )
    user_id = data.get("sender_id")
    if not user_id:
        return
    if await bot.ban_member_chat(chat_id=message.chat_id, user_id=user_id):
        await message.reply(
            f">🚫 **[کاربر]({user_id}) با موفقیت از گروه اخراج شد**\n"
        )

@bot.on_message(filters.text_equals("آن بن"))
async def unban_user(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    if not message.reply_to_message_id:
        await message.reply("⚠️ لطفاً روی پیام کاربر مورد نظر ریپلای کنید.")
        return
    data = await bot.get_message(
        chat_id=message.chat_id,
        message_id=message.reply_to_message_id
    )
    user_id = data.get("sender_id")
    if not user_id:
        return
    if await bot.unban_chat_member(chat_id=message.chat_id, user_id=user_id):
        await message.reply(
            f">✅ **[کاربر]({user_id}) از لیست مسدودشده‌ها خارج شد**\n"
        )

@bot.on_message(filters.text_equals("حالت سختگیر روشن"))
async def strict_on(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    await set_strict_mode(message.chat_id, True)
    await message.reply(">🔥 **حالت سخت‌گیر فعال شد**\nهر تخلف = اخراج فوری")

@bot.on_message(filters.text_equals("حالت سختگیر خاموش"))
async def strict_off(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    await set_strict_mode(message.chat_id, False)
    await message.reply(">🟢 **حالت سخت‌گیر غیرفعال شد**")

@bot.on_message(filters.text_equals("سخنگو روشن"))
async def speaker_on(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute("""
        INSERT OR REPLACE INTO speaker_mode (chat_id, is_enabled) 
        VALUES (?, 1)
        """, (message.chat_id,))
        await db.commit()
    await message.reply("🔊 **سخنگو فعال شد**. از این به بعد ربات پاسخ‌ها را از سخنگو دریافت خواهد کرد.")

@bot.on_message(filters.text_equals("سخنگو خاموش"))
async def speaker_off(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute("""
        INSERT OR REPLACE INTO speaker_mode (chat_id, is_enabled) 
        VALUES (?, 0)
        """, (message.chat_id,))
        await db.commit()
    await message.reply("🔇 **سخنگو غیرفعال شد**. ربات دیگر از سخنگو استفاده نخواهد کرد.")

@bot.on_message(filters.text_contains("تعداد اخطار"))
async def set_warning_threshold(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    match = re.search(r'\d+', message.text)
    if not match:
        return await message.reply("❗ لطفاً تعداد اخطارها را به درستی وارد کنید.")
    threshold = int(match.group(0))
    if threshold <= 0:
        return await message.reply("❗ تعداد اخطار باید بزرگتر از صفر باشد.")
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute("""
        INSERT OR REPLACE INTO warning_threshold (chat_id, threshold) 
        VALUES (?, ?)
        """, (message.chat_id, threshold))
        await db.commit()
    await message.reply(f"✅ تعداد اخطارها برای این گروه به {threshold} تغییر یافت.")

@bot.on_message(filters.text_equals("اخطار"))
async def add_warning(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    if not message.reply_to_message_id:
        return await message.reply("❗ لطفاً روی پیام کاربر مورد نظر ریپلای کنید.")
    data = await bot.get_message(
        chat_id=message.chat_id,
        message_id=message.reply_to_message_id
    )
    user_id = data.get("sender_id")
    if not user_id:return
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute("""
        INSERT INTO warnings (chat_id, user_id, warning_count) 
        VALUES (?, ?, 1)
        ON CONFLICT(chat_id, user_id) 
        DO UPDATE SET warning_count = warning_count + 1
        """, (message.chat_id, user_id))
        await db.commit()
        await cursor.execute("SELECT warning_count FROM warnings WHERE chat_id=? AND user_id=?", (message.chat_id, user_id))
        row = await cursor.fetchone()
        warning_count = row[0] if row else 0
        await cursor.execute("SELECT threshold FROM warning_threshold WHERE chat_id=?", (message.chat_id,))
        row = await cursor.fetchone()
        threshold = row[0] if row else 10
        if warning_count >= threshold:
            await bot.ban_member_chat(chat_id=message.chat_id, user_id=user_id)
            await message.reply(f"🚫 [کاربر]({user_id}) به دلیل دریافت {threshold} اخطار از گروه اخراج شد.")
        else:
            await message.reply(f"✅ اخطار به [کاربر]({user_id}) داده شد. تعداد اخطارها: {warning_count}")

@bot.on_message(filters.text_equals("حذف اخطار"))
async def remove_warning(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    if not message.reply_to_message_id:
        return await message.reply("❗ لطفاً روی پیام کاربر مورد نظر ریپلای کنید.")
    data = await bot.get_message(
        chat_id=message.chat_id,
        message_id=message.reply_to_message_id
    )
    user_id = data.get("sender_id")
    if not user_id:
        return
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute("""
        UPDATE warnings SET warning_count = warning_count - 1 
        WHERE chat_id=? AND user_id=? AND warning_count > 0
        """, (message.chat_id, user_id))
        await db.commit()
        await cursor.execute("SELECT warning_count FROM warnings WHERE chat_id=? AND user_id=?", (message.chat_id, user_id))
        row = await cursor.fetchone()
        warning_count = row[0] if row else 0

    await message.reply(f"✅ اخطار از [کاربر]({user_id}) حذف شد. تعداد اخطارها: {warning_count}")

@bot.on_message(filters.text_equals("لیست اخطار"))
async def list_all_warnings(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute("""
        SELECT user_id, warning_count 
        FROM warnings 
        WHERE chat_id=? 
        ORDER BY warning_count DESC
        """, (message.chat_id,))
        warnings = await cursor.fetchall()
    if not warnings:
        return await message.reply("❗ هیچ کاربری هنوز اخطار دریافت نکرده است.")
    text = "🛑 **لیست کاربران با اخطارها**:\n\n"
    for user_id, warning_count in warnings:
        text += f"> [کاربر]({user_id}) — تعداد اخطار: {warning_count}\n"
    await message.reply(text)

@bot.on_message(filters.text_contains("حذف"))
async def delete_messages(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():return
    num_messages = int(parts[1])
    if num_messages <= 0:return await message.reply("❗ تعداد پیام‌ها باید بزرگتر از صفر باشد.")
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute("""
        SELECT message_id FROM messages WHERE chat_id=? ORDER BY timestamp DESC LIMIT ?
        """, (message.chat_id, num_messages))
        messages = await cursor.fetchall()
    if not messages:return await message.reply("❗ هیچ پیام قابل حذف در این گروه وجود ندارد.")
    for (message_id,) in messages:
        try:
            await bot.delete_message(message.chat_id, message_id)
            async with connect_db() as db:
                cursor = await db.cursor()
                await cursor.execute("""
                DELETE FROM messages WHERE chat_id=? AND message_id=?
                """, (message.chat_id, message_id))
                await db.commit()
        except Exception as e:
            print(f"Error deleting message {message_id}: {e}")
    await message.reply(f"✅ {num_messages} پیام اخیر حذف شد.")

@bot.on_message(filters.text_contains("قفل گروه"))
async def lock_group(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    try:
        parts = message.text.split()
        if len(parts) >= 3 and parts[2].isdigit():lock_duration = int(parts[2])
        else:return await message.reply("❗ لطفا مدت زمان قفل گروه را به درستی وارد کنید.")
        await toggle_group_lock(message.chat_id, 1)
        await message.reply(f"✅ گروه به مدت {lock_duration} ثانیه قفل شد.")
        await asyncio.sleep(lock_duration)
        await toggle_group_lock(message.chat_id, 0)
        await message.reply("✅ مدت زمان قفل گروه تمام شد. قفل گروه باز شد.")
    except ValueError:
        await message.reply("❗ لطفا مدت زمان قفل گروه را به درستی وارد کنید.")

@bot.on_message(filters.text_equals("باز کردن قفل گروه"))
async def unlock_group(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    await toggle_group_lock(message.chat_id, 0)
    await message.reply("✅ قفل گروه باز شد. پیام‌ها قابل ارسال هستند.")

@bot.on_message(filters.text_equals("افزودن ادمین"))
async def add_admin_cmd(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    if not message.reply_to_message_id:return await message.reply("❗ روی پیام کاربر ریپلای کن")
    info = await bot.get_message(message.chat_id, message.reply_to_message_id)
    user_id = info["sender_id"]
    await add_admin(message.chat_id, user_id)
    await message.reply(f"✅ [کاربر]({user_id}) ادمین کمکی شد")

@bot.on_message(filters.text_equals("حذف ادمین"))
async def remove_admin_cmd(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    if not message.reply_to_message_id:return await message.reply("❗ روی پیام کاربر ریپلای کن")
    info = await bot.get_message(message.chat_id, message.reply_to_message_id)
    user_id = info["sender_id"]
    await remove_admin(message.chat_id, user_id)
    await message.reply(f"❌ [کاربر]({user_id}) از ادمینی حذف شد")

@bot.on_message(filters.text_equals("لیست ادمین"))
async def list_admins(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute(
            "SELECT user_id FROM admins WHERE chat_id=?",
            (message.chat_id,)
        )
        admins = await cursor.fetchall()
    
    if not admins:
        return await message.reply("❗ ادمین کمکی وجود ندارد")
    
    text = "🛡️ **ادمین‌های کمکی :**\n\n"
    for (uid,) in admins:
        text += f">- [کاربر]({uid})\n"
    await message.reply(text)

@bot.on_message()
async def check_group_lock(bot: Robot, message: Message):
    if not await chat_exists(message.chat_id):
        return
    if await is_group_locked(message.chat_id):
        await message.delete()

@bot.on_message(filters.text_equals("آمار"))
async def user_stats(bot: Robot, message: Message):
    if not message.reply_to_message_id:
        return await message.reply("❗ روی پیام کاربر ریپلای کن")
    info = await bot.get_message(message.chat_id, message.reply_to_message_id)
    user_id = info["sender_id"]
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute("""
        SELECT message_count FROM user_stats
        WHERE chat_id=? AND user_id=?
        """, (message.chat_id, user_id))
        row = await cursor.fetchone()
    count = row[0] if row else 0
    await message.reply(
        f"📊 **آمار کاربر**\n\n"
        f"👤 [کاربر]({user_id})\n"
        f"💬 تعداد پیام‌ها: **{count}**"
    )

@bot.on_message(filters.text_equals("آمار گروه"))
async def group_stats(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    group_name = await message.name
    now = jdatetime.datetime.now()
    time_text = now.strftime("%Y/%m/%d | %H:%M")
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute("SELECT SUM(message_count) FROM user_stats WHERE chat_id=?", (message.chat_id,))
        total_messages_row = await cursor.fetchone()
        total_messages = total_messages_row[0] if total_messages_row else 0
        await cursor.execute("SELECT COUNT(DISTINCT user_id) FROM user_stats WHERE chat_id=?", (message.chat_id,))
        active_users_row = await cursor.fetchone()
        active_users = active_users_row[0] if active_users_row else 0
        await cursor.execute("SELECT COUNT(*) FROM admins WHERE chat_id=?", (message.chat_id,))
        admin_count_row = await cursor.fetchone()
        admin_count = admin_count_row[0] + 1 if admin_count_row else 1
        await cursor.execute("SELECT COUNT(*) FROM mutes WHERE chat_id=?", (message.chat_id,))
        muted_users_row = await cursor.fetchone()
        muted_users = muted_users_row[0] if muted_users_row else 0
        await cursor.execute("SELECT COUNT(*) FROM users WHERE chat_id=?", (message.chat_id,))
        new_members_row = await cursor.fetchone()
        new_members = new_members_row[0] if new_members_row else 0
        past_24_hours = int(time.time()) - 86400
        await cursor.execute("SELECT SUM(message_count) FROM user_stats WHERE chat_id=? AND date > ?", 
                             (message.chat_id, past_24_hours))
        daily_messages_row = await cursor.fetchone()
        daily_messages = daily_messages_row[0] if daily_messages_row else 0
        past_7_days = int(time.time()) - 604800
        await cursor.execute("SELECT SUM(message_count) FROM user_stats WHERE chat_id=? AND date > ?", 
                             (message.chat_id, past_7_days))
        weekly_messages_row = await cursor.fetchone()
        weekly_messages = weekly_messages_row[0] if weekly_messages_row else 0
        today_start = int(time.mktime(jdatetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timetuple()))
        await cursor.execute("SELECT COUNT(DISTINCT user_id) FROM user_stats WHERE chat_id=? AND date >= ?", 
                             (message.chat_id, today_start))
        new_today_count_row = await cursor.fetchone()
        new_today_count = new_today_count_row[0] if new_today_count_row else 0
        await cursor.execute("SELECT user_id, message_count FROM user_stats WHERE chat_id=? ORDER BY message_count DESC LIMIT 3", (message.chat_id,))
        top_users = await cursor.fetchall()
        medals = ["🥇", "🥈", "🥉"]
        top_text = "\n".join(
            f"> {medals[i]} [Account]({uid}) — {count} پیام"
            for i, (uid, count) in enumerate(top_users)
        )
    await message.reply(
        f"📊 **گزارش آماری — “{group_name}”**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🕒 **زمان گزارش :** {time_text}\n"
        f"👥 **اعضای کل در دیتابیس :** {new_members}\n"
        f"👤 **کاربران فعال (دارای سابقه پیام) :** {active_users}\n"
        f"🛡️ **مدیران :** {admin_count}\n"
        f"🔇 **کاربران سکوت‌شده :** {muted_users}\n"
        f"💬 **کل پیام‌ها (تاریخچه) :** {total_messages}\n"
        f"📈 **پیام‌های ۲۴ ساعت گذشته :** {daily_messages}\n"
        f"📅 **پیام‌های ۷ روز گذشته :** {weekly_messages}\n"
        f"🌟 **کاربران پیام‌دهنده امروز :** {new_today_count}\n\n"
        f"🏆 **برترین مشارکت‌کنندگان :**\n{top_text}"
    )
@bot.on_message()
async def user_messages(bot, message: Message):
    if not await chat_exists(message.chat_id):
        return
    await save_member(message.chat_id, message.sender_id)
    await increase_message_count(message.chat_id, message.sender_id)
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute("SELECT mute_time, mute_duration, is_permanent FROM mutes WHERE chat_id=? AND user_id=?", 
                             (message.chat_id, message.sender_id))
        mute_info = await cursor.fetchone()
    if mute_info:
        mute_time, mute_duration, is_permanent = mute_info
        if is_permanent == 1:
            await message.delete()
            return
        remaining_time = mute_time + mute_duration - int(time.time())
        if remaining_time > 0:
            await message.delete()
        else:
            async with connect_db() as db:
                cursor = await db.cursor()
                await cursor.execute("DELETE FROM mutes WHERE chat_id=? AND user_id=?", (message.chat_id, message.sender_id))
                await db.commit()

@bot.on_message(filters.text_contains("تگ"))
async def tag_users(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return False

    members = await get_members(message.chat_id)
    if not members:
        return await message.reply("❗ کاربری ذخیره نشده")

    parts = message.text.split()
    chunk_size = 20
    if len(parts) == 2 and parts[1].isdigit():
        try:
            chunk_size = int(parts[1])
            if chunk_size <= 0:
                return await message.reply("❗ تعداد تگ باید بزرگتر از 0 باشد.")
        except ValueError:
            pass

    if len(members) <= chunk_size:
        chunks = [members]
    else:
        chunks = [members[i:i + chunk_size] for i in range(0, len(members), chunk_size)]

    for group in chunks:
        rand = await random_tag_text()
        text = " , ".join(f"[{rand}]({uid})" for uid in group)
        await bot.send_message(
            chat_id=message.chat_id,
            text=text,
            reply_to_message_id=message.message_id
        )

@bot.on_message()
async def mute_user(bot: Robot, message: Message):
    if not message.text.startswith("سکوت"):
        return
    if not await is_admin(message.chat_id, message.sender_id):return
    try:
        parts = message.text.split()
        print(parts)
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
        print(target_id)
        db = await connect_db()
        cursor = await db.cursor()
        await cursor.execute(
            "INSERT OR REPLACE INTO mutes (chat_id, user_id, mute_time, mute_duration, is_permanent) VALUES (?, ?, ?, ?, ?)",
            (message.chat_id, target_id, int(time.time()), mute_duration, is_permanent)
        )
        await db.commit()
        await db.close()
        if is_permanent:
            await message.reply(f"✅ [کاربر]({target_id}) برای همیشه سکوت شد.")
        else:
            await message.reply(f"✅ [کاربر]({target_id}) برای {mute_duration} ثانیه سکوت شد.")
        if mute_duration > 0:
            await asyncio.sleep(mute_duration)
            db = await connect_db()
            cursor = await db.cursor()
            await cursor.execute("DELETE FROM mutes WHERE chat_id=? AND user_id=?", (message.chat_id, target_id))
            await db.commit()
            await db.close()
            await message.reply(f"⏳ مدت زمان سکوت برای کاربر [کاربر]({target_id}) تمام شد.")
    except ValueError as e:
        print(e)
        await message.reply("❗ لطفا مدت زمان سکوت را به درستی وارد کنید.")

@bot.on_message(filters.text_equals("پاکسازی سکوت"))
async def clear_mute_list(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    db = await connect_db()
    async with db.cursor() as cursor:
        await cursor.execute("DELETE FROM mutes WHERE chat_id=?", (message.chat_id,))
        await db.commit()
    await message.reply("✅ **لیست سکوت با موفقیت پاک شد**")

@bot.on_message(filters.text_equals("حذف سکوت"))
async def unmute_command(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    if not message.reply_to_message_id:
        return await message.reply("❗ **لطفاً روی پیام کاربر مورد نظر ریپلای کنید تا سکوت آن حذف شود**")
    info = await bot.get_message(message.chat_id, message.reply_to_message_id)
    target_id = info["sender_id"]
    await unmute_user_db(message.chat_id, target_id)  
    await message.reply("✅ **سکوت کاربر با موفقیت حذف شد**")
    await message.reply(f"🔊 سکوت [کاربر]({target_id}) برداشته شد")

@bot.on_message(filters.text_equals("لیست سکوت"))
async def mute_list(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    muted_users = await get_muted_users(message.chat_id)  
    if not muted_users:return await message.reply("✅ لیست سکوت خالی است")
    response_text = "🔇 **کاربران سکوت‌شده** :\n\n" + "\n".join(f">- [کاربر]({uid})" for uid in muted_users)
    await message.reply(response_text)

@bot.on_message(filters.text_contains_any(["نصب", "فعال", "مالک"]))
async def install(bot, message: Message):
    if await chat_exists(message.chat_id):  
        return False
    await set_owner(message.chat_id, message.sender_id)  
    await message.reply(f"✅ ربات با موفقیت در گروه {await message.name} نصب شد\n👑 اکنون شما مالک این چت هستید")

async def check_rules(message: Message, rules: dict):
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
async def strict_and_rules_handler(bot: Robot, message: Message):
    if not await chat_exists(message.chat_id):return
    if await is_admin(message.chat_id, message.sender_id):return
    rules = await load_rules(message.chat_id)  
    violations = await check_rules(message, rules)  
    if not violations:return
    if await is_strict_mode(message.chat_id):  
        await bot.ban_member_chat(
            chat_id=message.chat_id,
            user_id=message.sender_id
        )
        await message.reply(
            f"🚫 **اخراج خودکار**\n"
            f"> [کاربر]({message.sender_id}) قوانین را نقض کرد و به دلیل روشن بودن حالت سختگیر از گروه اخراج شد\n"
            f"📌 تخلف صورت گرفته : {' و '.join(violations)}"
        )
        return await message.delete()
    await message.reply(
        f"⛔ **اخطار**\n"
        f"> [کاربر]({message.sender_id}) قوانین را نقض کرد\n"
        f"📌 دلیل: {' و '.join(violations)}",
        30
    )
    await message.delete()

@bot.on_message()
async def info(bot, message: Message):
    text = message.text.strip()
    reply_id = message.reply_to_message_id
    if text in ["get", "اطلاعات", "info"] and reply_id:
        info = await bot.get_message(message.chat_id, reply_id)
        return await bot.send_message(chat_id=message.chat_id, text=f"**اطلاعات پیام:**\n>{info}", reply_to_message_id=reply_id)

@bot.on_message()
async def admin_commands(bot: Robot, message: Message):
    if not await is_admin(message.chat_id, message.sender_id):return
    text = message.text.strip()
    if text == "وضعیت" or text == "قفل ها" or text == "وضعیت":
        rules = await load_rules(message.chat_id)  
        state = "\n".join(
            f"> {RULES_FA[k]}: {'✓ فعال' if v else '× غیرفعال'}"
            for k, v in rules.items()
        )
        return await message.reply(
            f"📊 **وضعیت قوانین گروه ** --{await message.name}-- :\n\n{state}\n\n"
            f"⚙️ برای تغییر وضعیت قوانین، از دستور مثال : `قفل لینک` استفاده کنید."
        )
    if text == "خاموش همه" or text == "همه خاموش":
        await set_all_rules(message.chat_id, False)  
        return await message.reply("🔕 همه قوانین خاموش شدند")
    if text == "روشن همه" or text == "همه روشن":
        await set_all_rules(message.chat_id, True)  
        return await message.reply("🔔 همه قوانین روشن شدند")
    for k, fa in RULES_FA.items():
        if text in [fa, f"قفل {fa}"]:
            await toggle_rule(message.chat_id, k)  
            return await message.reply(f"✔️ وضعیت **{fa}** تغییر کرد")

async def main():
    await create_tables()
    await bot.run(sleep_time=0)
asyncio.run(main())
