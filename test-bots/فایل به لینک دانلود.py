import asyncio, aiohttp, random, sqlite3, os
from rubka.asynco import Robot, Message, filters
from rubka.button import ChatKeypadBuilder
from datetime import datetime

DB_FILE = "database.db"
ADMIN_ID = "chat_id_admin"

bot = Robot("token")


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users(
                    user_id TEXT PRIMARY KEY,
                    name TEXT
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS files(
                    id TEXT PRIMARY KEY,
                    user_id TEXT,
                    name TEXT,
                    file_name TEXT,
                    type TEXT,
                    size TEXT,
                    time TEXT,
                    url TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )""")
    conn.commit()
    conn.close()

def add_user(user_id, name=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users(user_id, name) VALUES(?, ?)", (str(user_id), name))
    conn.commit()
    conn.close()

def add_file(file_info: dict):
    add_user(file_info["user_id"], file_info["name"])
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""INSERT OR REPLACE INTO files(id, user_id, name, file_name, type, size, time, url)
                 VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
                 (file_info["id"], file_info["user_id"], file_info["name"],
                  file_info["file_name"], file_info["type"], file_info["size"],
                  file_info["time"], file_info["url"]))
    conn.commit()
    conn.close()

def get_last_files(limit=5):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, user_id, name, file_name, type, size, time, url FROM files ORDER BY ROWID DESC LIMIT ?", (limit,))
    files = [dict(zip([column[0] for column in c.description], row)) for row in c.fetchall()]
    conn.close()
    return files

def get_stats():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM files")
    files_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM users")
    users_count = c.fetchone()[0]
    conn.close()
    return files_count, users_count

def get_file(file_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, user_id, name, file_name, type, size, time, url FROM files WHERE id=?", (file_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return dict(zip(["id", "user_id", "name", "file_name", "type", "size", "time", "url"], row))
    return None


def get_type(message: Message):
    return (
        "Image" if message.is_photo else
        "Video" if message.is_video else
        "Voice" if message.is_voice else
        "Music" if message.is_audio else
        "File"
    )

def get_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

async def shorten(url: str) -> str:
    api_url = f"https://v3.api-free.ir/cut/?url={url}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                data = await response.json()
                if data.get("ok") and data.get("result"):
                    return data["result"]
    except:
        pass
    return url

async def reply_file_info(bot: Robot, message: Message, file_id: str):
    file_info = get_file(file_id)
    if not file_info:
        await message.reply("❌ File not found!")
        return
    await message.reply(
        f"✅ File information:\n\n"
        f"🆔 File ID : {file_info['id']}\n"
        f"👤 Sender : {file_info['name']}\n"
        f"📄 File Name : {file_info['file_name']}\n"
        f"🗂 File Type : {file_info['type']}\n"
        f"📏 File Size : {file_info['size']}\n"
        f"⏰ Upload Time : {file_info['time']}\n"
        f"🔗 Download Link : {file_info['url']}"
    )


waiting_broadcast = {}
admin_keypad = (
    ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button(id="btn_last_files", text="📂 ۵ فایل آخر"),
        ChatKeypadBuilder().button(id="btn_stats", text="📊 آمار ربات")
    )
    .row(
        ChatKeypadBuilder().button(id="btn_broadcast", text="📣 پیام همگانی")
    )
    .build()
)


@bot.on_message(commands=['start', "Start"])
async def start(bot: Robot, message: Message):
    name = await message.author_name
    add_user(message.chat_id, name)
    await message.reply("""✨ خوش اومدی به ربات تبدیل فایل به لینک دانلود ✨

📦 با این ربات می‌تونی هر فایلی مثل
🎬 ویدیو، 🖼 عکس، 🎵 آهنگ یا 📄 سند رو
مستقیم بفرستی یا از چت‌های دیگه فوروارد کنی 🔄

🚀 فقط فایلتو بفرست تا لینک مخصوصت رو تحویل بگیری 💎
""")

@bot.on_message_file()
async def handle_file(bot: Robot, message: Message):
    send = await message.reply(f"⏳ منتظر بمانید...")
    await send.edit("⬇️ دریافت لینک دانلود فایل...")
    data_down = await bot.get_url_file(message.file.file_id)
    await send.edit("📝 شناسایی نوع فایل...")
    type_file = get_type(message)
    await send.edit("📏 محاسبه حجم فایل...")
    size_file = get_size(message.file.size)
    await send.edit("👤 دریافت اطلاعات ارسال‌کننده و فایل...")
    name = await message.author_name
    file_name = message.file.file_name
    time_up = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
    await send.edit("🔗 کوتاه کردن لینک دانلود...")
    url = await shorten(data_down)
    
    file_id = str(random.randint(1000, 9999))

    add_file({
        "id": file_id,
        "user_id": message.chat_id,
        "name": name,
        "file_name": file_name,
        "type": type_file,
        "size": size_file,
        "time": time_up,
        "url": url
    })

    await send.delete()
    await message.reply(
        f"✅ Your file is ready!\n\n"
        f"🆔 File ID : /file_{file_id}\n\n"
        f"👤 Sender : {name}\n\n"
        f"📄 File Name : {file_name}\n\n"
        f"🗂 File Type : {type_file}\n\n"
        f"📏 File Size : {size_file}\n\n"
        f"⏰ Upload Time : {time_up}\n\n"
        f"🔗 Download Link : {url}"
    )

@bot.on_message(filters.text_startswith("/file_"))
async def file_info_command(bot: Robot, message: Message):
    file_id = message.text.split("_", 1)[1]
    await reply_file_info(bot, message, file_id)


@bot.on_message(commands=["admin"])
async def admin_panel(bot: Robot, message: Message):
    if str(message.chat_id) != str(ADMIN_ID):
        return await message.reply("❌ شما ادمین نیستید!")
    await message.reply("👋 خوش آمدید به پنل ادمین", chat_keypad=admin_keypad, chat_keypad_type="New")

@bot.on_callback("btn_last_files")
async def last_files(bot: Robot, message: Message):
    if str(message.object_guid) != str(ADMIN_ID):
        return await message.answer("❌ شما ادمین نیستید!")
    files = get_last_files()
    if not files:
        return await message.answer("📂 هیچ فایلی هنوز آپلود نشده.")
    text = "📂 ۵ فایل آخر:\n" + "\n".join(
        [f"🆔 {f['id']} | {f['file_name']} | {f['type']} | {f['size']}" for f in files]
    )
    await message.answer(text)

@bot.on_callback("btn_stats")
async def stats(bot: Robot, message: Message):
    if str(message.chat_id) != str(ADMIN_ID):
        return await message.answer("❌ شما ادمین نیستید!")
    files_count, users_count = get_stats()
    await message.answer(f"📊 آمار ربات:\n- تعداد فایل‌ها: {files_count}\n- تعداد کاربران: {users_count}")

@bot.on_callback("btn_broadcast")
async def broadcast_prompt(bot: Robot, message: Message):
    if str(message.chat_id) != str(ADMIN_ID):
        return await message.answer("❌ شما ادمین نیستید!")
    waiting_broadcast[message.chat_id] = True
    await message.answer("📌 لطفا متن پیام همگانی را ارسال کنید:")

@bot.on_message()
async def handle_broadcast(bot: Robot, message: Message):
    if waiting_broadcast.get(message.chat_id):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT user_id FROM users")
        users = [row[0] for row in c.fetchall()]
        conn.close()

        send_bro = await message.reply("فرآیند آغاز شد...")
        count = 0
        for user in users:
            try:
                await bot.send_message(user, message.text)
                count += 1
                await send_bro.edit(f"ارسال به {count} کاربر")
            except:
                pass
        await send_bro.delete()
        await message.reply(f"✅ پیام همگانی به {len(users)} کاربر ارسال شد.")
        waiting_broadcast.pop(message.chat_id)

init_db()
asyncio.run(bot.run())
