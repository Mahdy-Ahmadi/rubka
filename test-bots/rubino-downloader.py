import json
from pathlib import Path
import requests
from datetime import datetime
from collections import defaultdict
import time
import asyncio

from rubka.asynco import Robot
from rubka.context import Message
from rubka.keypad import ChatKeypadBuilder


BOT_TOKEN = ""  # <<<<! توکن ربات خود را اینجا وارد کنید
ADMIN_CHAT_ID = "b0HJtFl0DWH0808233b473ba66da96bd"  # <<<<! شناسه عددی چت ادمین را اینجا وارد کنید


API_POST_URL = "https://api-free.ir/api/rubino-dl.php"
API_STORY_URL = "https://api-free.ir/api/story_rubino.php"
DATA_FILE = Path("rubino_bot_keyboard_data.json")

user_states = defaultdict(dict)

ID_DL_POST = "📥 دانلود پست"
ID_DL_STORY = "🎬 دانلود استوری"
ID_HISTORY = "📂 تاریخچه دانلودها"
ID_SEND_TICKET = "✉️ ارسال تیکت"
ID_HELP = "❓ راهنما"
ID_BACK = "↪️ بازگشت"

ID_ADMIN_STATS = "admin_stats"
ID_ADMIN_TICKETS = "admin_tickets"
ID_ADMIN_USERS = "admin_users"
ID_ADMIN_BROADCAST = "admin_broadcast"
ID_ADMIN_MAINTENANCE = "admin_maintenance"


def load_data():
    if not DATA_FILE.exists():
        initial_data = {
            "users": {}, "banned_users": [], "tickets": {},
            "bot_settings": {"maintenance_mode": False},
            "stats": {"post_downloads": 0, "story_downloads": 0, "tickets_created": 0}
        }
        save_data(initial_data)
        return initial_data
    try:
        with DATA_FILE.open('r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception):
        return load_data()

def save_data(data):
    with DATA_FILE.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def update_stats(stat_name, count=1):
    data = load_data()
    data["stats"][stat_name] = data["stats"].get(stat_name, 0) + count
    save_data(data)

def add_to_history(user_id, download_type, query, status):
    data = load_data()
    user_data = data["users"].get(str(user_id))
    if "history" not in user_data:
        user_data["history"] = []
    user_data["history"].insert(0, {
        "type": download_type, "query": query, "status": status, "timestamp": datetime.now().isoformat()
    })
    user_data["history"] = user_data["history"][:20]
    data["users"][str(user_id)] = user_data
    save_data(data)

def download_post(url):
    try:
        response = requests.get(API_POST_URL, params={"url": url}, timeout=20)
        return response.json() if response.status_code == 200 and response.json().get("ok") else None
    except Exception:
        return None

def download_story(page_id):
    try:
        response = requests.get(API_STORY_URL, params={"id": page_id}, timeout=20)
        return response.json() if response.status_code == 200 and response.json().get("ok") else None
    except Exception:
        return None


def get_main_menu_keyboard():
    k = ChatKeypadBuilder()
    k.row(k.button(id=ID_DL_POST, text=ID_DL_POST), k.button(id=ID_DL_STORY, text=ID_DL_STORY))
    k.row(k.button(id=ID_HISTORY, text=ID_HISTORY))
    k.row(k.button(id=ID_SEND_TICKET, text=ID_SEND_TICKET), k.button(id=ID_HELP, text=ID_HELP))
    return k.build(resize_keyboard=True, on_time_keyboard=True)

def get_back_keyboard():
    k = ChatKeypadBuilder()
    k.row(k.button(id=ID_BACK, text=ID_BACK))
    return k.build(resize_keyboard=True, on_time_keyboard=True)

def get_admin_panel_keyboard():
    data = load_data()
    open_tickets = len([t for t in data['tickets'].values() if t['status'] == 'open'])
    k = ChatKeypadBuilder()
    k.row(k.button(id=ID_ADMIN_STATS, text="📊 آمار ربات"), k.button(id=ID_ADMIN_TICKETS, text=f"🎫 مدیریت تیکت‌ها ({open_tickets})"))
    k.row(k.button(id=ID_ADMIN_USERS, text="👥 مدیریت کاربران"), k.button(id=ID_ADMIN_BROADCAST, text="📣 ارسال همگانی"))
    k.row(k.button(id=ID_ADMIN_MAINTENANCE, text="⚙️ روشن/خاموش کردن ربات"), k.button(id=ID_BACK, text=ID_BACK))
    return k.build(resize_keyboard=True, on_time_keyboard=True)

bot = Robot(token=BOT_TOKEN)


@bot.on_message()
async def message_handler(bot: Robot, msg: Message):
    global user_states
    chat_id = msg.chat_id
    text = msg.text.strip() if msg.text else ""
    callback_data = msg.aux_data.button_id if msg.aux_data else None
    user_id_str = str(chat_id)
    
    data = load_data()
    is_admin = user_id_str == str(ADMIN_CHAT_ID)

    if data['bot_settings']['maintenance_mode'] and not is_admin:
        await msg.reply("🛠 ربات در حال حاضر در حالت تعمیر است و به زودی فعال خواهد شد.")
        return

    if user_id_str in data.get("banned_users", []):
        await msg.reply("🚫 شما توسط مدیر مسدود شده‌اید.")
        return

    if user_id_str not in data["users"]:
        data["users"][user_id_str] = {"join_date": datetime.now().isoformat(), "history": []}
        save_data(data)
        print(f"کاربر جدید: {chat_id}")

    state = user_states[chat_id].get("state")
    if callback_data:
        user_states[chat_id] = {}

        if callback_data == ID_BACK:
            await msg.reply("منوی اصلی:", chat_keypad=get_main_menu_keyboard())

        elif callback_data == ID_DL_POST:
            user_states[chat_id]["state"] = "awaiting_post_link"
            await msg.reply("🔗 لطفاً لینک پست روبینو را ارسال کنید:", chat_keypad=get_back_keyboard())

        elif callback_data == ID_DL_STORY:
            user_states[chat_id]["state"] = "awaiting_story_id"
            await msg.reply("👤 لطفاً یوزرنیم (ID) پیج مورد نظر را بدون @ ارسال کنید:", chat_keypad=get_back_keyboard())

        elif callback_data == ID_HISTORY:
            history = data['users'][user_id_str].get('history', [])
            if not history:
                await msg.reply("📂 تاریخچه دانلودهای شما خالی است.", chat_keypad=get_main_menu_keyboard())
                return
            history_text = "📂 آخرین دانلودهای شما:\n\n"
            for item in history:
                status_icon = "✅" if item['status'] == 'success' else "❌"
                history_text += f"{status_icon} `{item['type']}`: `{item['query']}`\n"
            await msg.reply(history_text, chat_keypad=get_main_menu_keyboard())

        elif callback_data == ID_SEND_TICKET:
            user_states[chat_id]["state"] = "awaiting_ticket_message"
            await msg.reply("✉️ لطفاً پیام خود را برای ارسال به ادمین بنویسید:", chat_keypad=get_back_keyboard())

        elif callback_data == ID_HELP:
            help_text = "❓ راهنما\n\n- دانلود پست: لینک کامل پست را بفرستید.\n- دانلود استوری: یوزرنیم پیج را بفرستید.\n- تاریخچه: نمایش 20 دانلود آخر.\n- تیکت: ارسال پیام به ادمین."
            await msg.reply(help_text, chat_keypad=get_main_menu_keyboard())
            
        elif is_admin:
            if callback_data == ID_ADMIN_STATS:
                stats = data['stats']
                stats_text = (f"📊 آمار ربات\n\n"
                              f"👥 تعداد کل کاربران: `{len(data['users'])}`\n"
                              f"📥 دانلود پست: `{stats.get('post_downloads', 0)}`\n"
                              f"🎬 دانلود استوری: `{stats.get('story_downloads', 0)}`\n"
                              f"🎫 کل تیکت‌ها: `{stats.get('tickets_created', 0)}`")
                await msg.reply(stats_text)
            
            elif callback_data == ID_ADMIN_BROADCAST:
                user_states[chat_id]['state'] = 'admin_awaiting_broadcast'
                await msg.reply("لطفاً پیام خود را برای ارسال به تمام کاربران وارد کنید:", chat_keypad=get_back_keyboard())
            
            elif callback_data == ID_ADMIN_MAINTENANCE:
                data['bot_settings']['maintenance_mode'] = not data['bot_settings']['maintenance_mode']
                save_data(data)
                status = "روشن ✅" if data['bot_settings']['maintenance_mode'] else "خاموش 🔴"
                await msg.reply(f"حالت تعمیر و نگهداری {status} شد.")
            
    elif text:
        if text == "/start":
            await msg.reply("🌟 به ربات دانلودر روبینو خوش آمدید!", chat_keypad=get_main_menu_keyboard())

        elif text == "/panel" and is_admin:
            await msg.reply("👑 پنل مدیریت", chat_keypad=get_admin_panel_keyboard())
        
        elif state == "awaiting_post_link":
            if "rubika.ir/post/" not in text:
                await msg.reply("❌ لینک نامعتبر است. لطفاً لینک صحیح را ارسال کنید.")
                return
            wait_msg = await msg.reply("⏳ در حال پردازش لینک...")
            result = download_post(text)
            if result:
                update_stats("post_downloads")
                add_to_history(chat_id, "پست", text.split("/")[-1], "success")
                res_data = result['result']
                caption = (
    "✅ دانلود با موفقیت انجام شد!\n\n"
    f"👤 پیج: {res_data['page_username']}\n"
    f"👥 تعداد فالوورها: {res_data['follower_page']}\n"
    f"❤️ لایک‌ها: {res_data['like']}\n"
    f"💬 کامنت‌ها: {res_data['comment']}\n"
    f"👁 بازدیدها: {res_data['view']}\n"
    f"🆔 آیدی پست: {res_data['post_id']}\n\n"
)
                await bot.send_video(msg.chat_id,res_data['url'],text=caption)
            else:
                add_to_history(chat_id, "پست", text.split("/")[-1], "failure")
                await bot.edit_message_text(chat_id, wait_msg['data']['message_id'], "❌ خطایی در دانلود رخ داد.")
            user_states[chat_id] = {}
            await msg.reply("برای دانلود جدید، از منو استفاده کنید:", chat_keypad=get_main_menu_keyboard())

        elif state == "awaiting_story_id":
            page_id = text.replace("@", "")
            wait_msg = await msg.reply(f"⏳ در حال دریافت استوری‌های `{page_id}`...")
            result = download_story(page_id)
            if result and result.get('result'):
                story_links = result['result']
                update_stats("story_downloads", len(story_links))
                add_to_history(chat_id, "استوری", page_id, "success")
                response_text = f"✅ تعداد {len(story_links)} استوری یافت شد.\n\n🔗 لینک‌های دانلود:\n"
                for i, link in enumerate(story_links, 1):
                    response_text += f"{i}. `{link}`\n"
                await bot.edit_message_text(chat_id, wait_msg['data']['message_id'], response_text)
            else:
                add_to_history(chat_id, "استوری", page_id, "failure")
                await bot.edit_message_text(chat_id, wait_msg['data']['message_id'], "❌ استوری‌ای یافت نشد یا پیج خصوصی است.")
            user_states[chat_id] = {}
            await msg.reply("برای دانلود جدید، از منو استفاده کنید:", chat_keypad=get_main_menu_keyboard())
        
        elif state == "awaiting_ticket_message":
            ticket_id = "T" + str(int(time.time()))
            data['tickets'][ticket_id] = {"user_id": chat_id, "message": text, "status": "open"}
            update_stats("tickets_created")
            save_data(data)
            await msg.reply("✅ تیکت شما ثبت و به ادمین ارسال شد.", chat_keypad=get_main_menu_keyboard())
            await bot.send_message(ADMIN_CHAT_ID, f"🎫 تیکت جدید (`{ticket_id}`)\nاز: `{chat_id}`\nپیام: {text}")
            user_states[chat_id] = {}
        
        elif state == "admin_awaiting_broadcast":
             if is_admin:
                user_states[chat_id] = {}
                await msg.reply("⏳ در حال ارسال پیام همگانی...")
                all_users = list(data.get("users", {}).keys())
                sent_count, failed_count = 0, 0
                for user in all_users:
                    try:
                        await bot.send_message(user, text, chat_keypad=get_main_menu_keyboard())
                        sent_count += 1
                        await asyncio.sleep(0.1)
                    except Exception:
                        failed_count += 1
                await msg.reply(f"📣 ارسال تمام شد.\n🟢 موفق: {sent_count}\n🔴 ناموفق: {failed_count}", chat_keypad=get_admin_panel_keyboard())

async def main():
    print("ربات با موفقیت اجرا شد...")
    await bot.run()

if __name__ == "__main__":
    try:
        load_data()
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n...ربات متوقف شد")
