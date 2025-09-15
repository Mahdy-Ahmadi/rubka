import asyncio
import random
import aiohttp
import json
import os
import time
from rubka.asynco import Robot, Message, filters
from rubka.button import ChatKeypadBuilder


TOKEN = ""  #token
ADMIN_ID = ""  #chat_id admin
BOT_USERNAME = ""  #username bot 



WEBHOOK_URL = "" #web_hook
bot = Robot(TOKEN, web_hook=WEBHOOK_URL)


API_V2RAY = "https://v3.api-free.ir/v2ray/"
API_TELEGRAM = "https://api-free.ir/api/proxy.php"
API_EDIT_V2RAY = "https://v3.api-free.ir/v2ray/edit.php"


CHANNELS_DB_FILE = "channels.json"
SETTINGS_DB_FILE = "settings.json"
USERS_DB_FILE = "users_proxy.json"   


channels_data = {}
app_settings = {}
admin_session_data = {}  
users_data = {}  



def load_data():
    """تمام داده‌ها را از فایل‌های JSON بارگذاری می‌کند."""
    global channels_data, app_settings, users_data

    
    try:
        with open(CHANNELS_DB_FILE, "r", encoding="utf-8") as f:
            channels_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        channels_data = {}
        print(f"'{CHANNELS_DB_FILE}' یافت نشد یا نامعتبر است. با داده‌های خالی کانال مقداردهی اولیه شد.")

    
    try:
        with open(SETTINGS_DB_FILE, "r", encoding="utf-8") as f:
            app_settings = json.load(f)
            
            default_settings = {
                "join_channel_text": (
                    "👋 سلام!\n\n"
                    "برای استفاده از ربات، لازم است در کانال‌های زیر عضو شوید:\n\n"
                    "{} \n\n"
                    "پس از عضویت، روی دکمه «بازگشت به منو» کلیک کنید."
                ),
                "welcome_message": "👋 خوش اومدی!\nاز منو استفاده کن:",
            }
            
            for key, value in default_settings.items():
                if key not in app_settings:
                    app_settings[key] = value
    except (FileNotFoundError, json.JSONDecodeError):
        app_settings = {
            "join_channel_text": (
                "👋 سلام!\n\n"
                "برای استفاده از ربات، لازم است در کانال‌های زیر عضو شوید:\n\n"
                "{} \n\n"
                "پس از عضویت، روی دکمه «بازگشت به منو» کلیک کنید."
            ),
            "welcome_message": "👋 خوش اومدی!\nاز منو استفاده کن:",
        }
        print(f"'{SETTINGS_DB_FILE}' یافت نشد یا نامعتبر است. با تنظیمات پیش‌فرض مقداردهی اولیه شد.")

    
    try:
        with open(USERS_DB_FILE, "r", encoding="utf-8") as f:
            users_data = json.load(f)
            
            if not isinstance(users_data, dict):
                print(f"'{USERS_DB_FILE}' دارای فرمت نامعتبر است. با یک دیکشنری خالی مقداردهی اولیه شد.")
                users_data = {}
    except (FileNotFoundError, json.JSONDecodeError):
        users_data = {}
        print(f"'{USERS_DB_FILE}' یافت نشد یا نامعتبر است. با داده‌های خالی کاربران مقداردهی اولیه شد.")

def save_channels_data():
    """داده‌های کانال‌ها را در CHANNELS_DB_FILE ذخیره می‌کند."""
    try:
        with open(CHANNELS_DB_FILE, "w", encoding="utf-8") as f:
            json.dump(channels_data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"خطا در ذخیره {CHANNELS_DB_FILE}: {e}")

def save_settings():
    """تنظیمات برنامه را در SETTINGS_DB_FILE ذخیره می‌کند."""
    try:
        with open(SETTINGS_DB_FILE, "w", encoding="utf-8") as f:
            json.dump(app_settings, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"خطا در ذخیره {SETTINGS_DB_FILE}: {e}")

def save_users_data():
    """داده‌های کاربران را در USERS_DB_FILE ذخیره می‌کند."""
    try:
        with open(USERS_DB_FILE, "w", encoding="utf-8") as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"خطا در ذخیره {USERS_DB_FILE}: {e}")



async def get_channel_info(channel_guid: str) -> dict:
    """
    برای دریافت اطلاعات کانال. در سناریوی واقعی، از API روبیکا استفاده می‌کنید.
    این تابع فعلا فقط یک placeholder است.
    """
    info = {"guid": channel_guid, "username": None, "link": None}
    try:
        pass  
    except Exception as e:
        print(f"خطا در دریافت اطلاعات کانال {channel_guid}: {e}")
    return info

async def check_user_join(user_guid: str, channels: dict) -> list[dict]:
    """بررسی می‌کند که آیا کاربر عضو تمام کانال‌های مشخص شده است یا خیر."""
    not_joined_channels = []
    for channel_guid, channel_info in channels.items():
        try:
            is_member = await bot.check_join(channel_guid, user_guid)
            if not is_member:
                not_joined_channels.append({
                    "guid": channel_guid,
                    "username": channel_info.get("username"),
                    "link": channel_info.get("link")
                })
        except Exception as e:
            print(f"خطا در بررسی عضویت کاربر {user_guid} در کانال {channel_guid}: {e}")
            
            not_joined_channels.append({
                "guid": channel_guid,
                "username": channel_info.get("username"),
                "link": channel_info.get("link")
            })
    return not_joined_channels

async def get_random_v2ray_proxy():
    """یک پروکسی V2Ray تصادفی از API دریافت می‌کند."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_V2RAY) as resp:
                resp.raise_for_status()  
                data = await resp.json()
                proxies = data.get("proxies", [])
                if not proxies:
                    return None
                return random.choice(proxies)
    except aiohttp.ClientError as e:
        print(f"خطا در دریافت پروکسی V2Ray: {e}")
        return None
    except json.JSONDecodeError:
        print("خطا در رمزگشایی پاسخ API پروکسی V2Ray.")
        return None

async def get_random_telegram_proxy():
    """یک پروکسی تلگرام تصادفی از API دریافت می‌کند."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_TELEGRAM) as resp:
                resp.raise_for_status()
                data = await resp.json()
                proxies = data.get("result", [])
                if not proxies:
                    return None
                return random.choice(proxies)
    except aiohttp.ClientError as e:
        print(f"خطا در دریافت پروکسی تلگرام: {e}")
        return None
    except json.JSONDecodeError:
        print("خطا در رمزگشایی پاسخ API پروکسی تلگرام.")
        return None

async def edit_v2ray_proxy(proxy: str, name: str):
    """یک پروکسی V2Ray را با نام جدید ویرایش می‌کند."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_EDIT_V2RAY}?proxy={proxy}&name={name}") as resp:
                resp.raise_for_status()
                return await resp.json()
    except aiohttp.ClientError as e:
        print(f"خطا در ویرایش پروکسی V2Ray: {e}")
        return {"ok": False, "error": str(e)}
    except json.JSONDecodeError:
        print("خطا در رمزگشایی پاسخ API ویرایش V2Ray.")
        return {"ok": False, "error": "پاسخ JSON نامعتبر"}


proxy_inline_keypad = (ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button("get_telegram_proxy", "📱 پروکسی تلگرام"),
        ChatKeypadBuilder().button("get_v2ray_proxy", "💻 پروکسی V2Ray"))
    .row(
        ChatKeypadBuilder().button("edit_v2ray_name", "✏️ ادیت نام پروکسی V2Ray"))
    .build())



@bot.on_message(filters.is_command.start)
async def start_handler(bot: Robot, msg: Message):
    """دستور /start را هندل می‌کند."""
    user_guid = msg.chat_id
    user_chat_id = msg.chat_id 
    print(user_chat_id)

    
    if user_guid not in users_data:
        users_data[user_guid] = {
            "join_time": int(time.time()),
            "last_active": int(time.time()),
            "name": await bot.get_name(user_chat_id) or "کاربر ناشناس" 
        }
        save_users_data()
    else:
        
        if "name" not in users_data[user_guid]:
            users_data[user_guid]["name"] = await bot.get_name(user_chat_id) or "کاربر ناشناس"
        users_data[user_guid]["last_active"] = int(time.time())
        save_users_data()

    
    not_joined = await check_user_join(user_guid, channels_data)

    if not_joined:
        channel_links_text = ""
        for channel in not_joined:
            if channel.get("link"):
                channel_links_text += f"- {channel['link']}\n"
            elif channel.get("username"):
                channel_links_text += f"- https://rubika.ir/{channel['username']} (عضویت اجباری)\n"
            else:
                channel_links_text += f"- کانال با GUID: {channel['guid']} (عضویت اجباری)\n"
        
        join_text = app_settings.get("join_channel_text", "متن پیش‌فرض جوین").format(channel_links_text)
        
        chat_kb = (
            ChatKeypadBuilder()
            .row(ChatKeypadBuilder().button(id="btn_check_join", text="عضو شدم"))
            .build()
        )
        await msg.reply(
            join_text,
            inline_keypad=chat_kb,
            chat_keypad_type="New"
        )
    else:
        
        welcome_msg = app_settings.get("welcome_message", f"👋 خوش اومدی {await bot.get_name(user_chat_id)} !\nاز منو استفاده کن:")
        await msg.reply(
            welcome_msg,
            inline_keypad=proxy_inline_keypad, 
            chat_keypad_type="New"
        )

@bot.on_callback("btn_check_join")
async def check_join_callback(bot: Robot, msg: Message):
    """هندلر دکمه «عضو شدم» برای تایید عضویت در کانال‌ها."""
    user_guid = msg.chat_id
    not_joined = await check_user_join(user_guid, channels_data)
    
    if not not_joined:
        
        welcome_msg = app_settings.get("welcome_message", f"👋 خوش اومدی {await bot.get_name(msg.chat_id)} !\nاز منو استفاده کن:")
        await msg.reply(
            welcome_msg,
            inline_keypad=proxy_inline_keypad,
            chat_keypad_type="New"
        )
    else:
        
        channel_links_text = ""
        for channel in not_joined:
            if channel.get("link"):
                channel_links_text += f"- {channel['link']}\n"
            elif channel.get("username"):
                channel_links_text += f"- https://rubika.ir/{channel['username']} (عضویت اجباری)\n"
            else:
                channel_links_text += f"- کانال با GUID: {channel['guid']} (عضویت اجباری)\n"
        
        join_text = app_settings.get("join_channel_text", "حتما در کانال جوین شوید").format(channel_links_text)
        await msg.answer(join_text) 

@bot.on_callback("get_telegram_proxy")
async def telegram_proxy_button(bot, msg: Message):
    """هندلر دکمه «پروکسی تلگرام»."""
    proxy = await get_random_telegram_proxy()
    if not proxy:
        await msg.reply("❌ پروکسی تلگرام پیدا نشد.")
        return
    await msg.reply(f"📱 Telegram Proxy:\n{proxy}")

@bot.on_callback("get_v2ray_proxy")
async def v2ray_proxy_button(bot, msg: Message):
    """هندلر دکمه «پروکسی V2Ray»."""
    proxy = await get_random_v2ray_proxy()
    if not proxy:
        await msg.reply("❌ پروکسی V2Ray پیدا نشد.")
        return
    await msg.reply(f"💻 V2Ray Proxy :\n\nType : {proxy.get('type', 'N/A')}\n\nProxy : {proxy.get('proxy', 'N/A')}")

@bot.on_callback("edit_v2ray_name")
async def edit_v2ray_name_button(bot, msg: Message):
    """فرآیند ویرایش نام پروکسی V2Ray را آغاز می‌کند."""

    
    admin_session_data.pop(msg.chat_id, None)
    
    admin_session_data[msg.chat_id] = {'edit_stage': 'await_proxy'}
    await msg.reply("💻 لطفاً ابتدا پروکسی V2Ray را وارد کنید (مثلاً `vmess://...` یا `vless://...`):")



@bot.on_message(filters.is_command.panel)
async def admin_panel(bot: Robot, msg: Message):
    """منوی پنل مدیریت را نمایش می‌دهد."""
    if msg.chat_id != ADMIN_ID:
        print(f"دسترسی غیرمجاز به پنل از {msg.author_guid}")
        return

    admin_kb = (
        ChatKeypadBuilder()
        .row(
            ChatKeypadBuilder().button("btn_manage_channels", "🔗 مدیریت کانال‌ها"),
            ChatKeypadBuilder().button("btn_settings", "⚙️ تنظیمات متنی")
        )
        .row(
            ChatKeypadBuilder().button("btn_view_all_proxies", "👁️ مشاهده پروکسی‌ها (V2Ray)"),
            ChatKeypadBuilder().button("btn_stats", "📊 آمار کاربران") 
        )
        .row(
            ChatKeypadBuilder().button("btn_broadcast", "📢 ارسال همگانی") 
        )
        .build()
    )

    await msg.reply("📌 پنل مدیریت:", inline_keypad=admin_kb)



@bot.on_callback("btn_manage_channels")
async def manage_channels_panel(bot: Robot, msg: Message):
    """پنل مدیریت کانال‌ها را نمایش می‌دهد."""
    if msg.chat_id != ADMIN_ID: return

    if not channels_data:
        channel_list_text = "هیچ کانالی برای عضویت اجباری تعریف نشده است."
    else:
        channel_list_text = "🔗 کانال‌های عضویت اجباری:\n"
        for i, (guid, info) in enumerate(channels_data.items()):
            link = info.get("link", "لینک تعریف نشده")
            username = info.get("username", "نام کاربری تعریف نشده")
            channel_list_text += f"{i+1}. نام: {username} | لینک: {link} | GUID: {guid}\n"

    channel_kb = (
        ChatKeypadBuilder()
        .row(ChatKeypadBuilder().button(id="btn_add_channel_prompt", text="➕ افزودن کانال"))
        .row(
            ChatKeypadBuilder().button("btn_del_channel_prompt", "➖ حذف کانال"),
            ChatKeypadBuilder().button("btn_edit_channel_prompt", "✏️ ویرایش کانال")
        )
        .row(ChatKeypadBuilder().button(id="back_to_admin_panel", text="بازگشت"))
        .build()
    )

    await msg.reply(
        f"🔗 مدیریت کانال‌ها:\n\n{channel_list_text}\n\n"
        "لطفا عملیات مورد نظر خود را انتخاب کنید:",
        inline_keypad=channel_kb
    )

@bot.on_callback("btn_add_channel_prompt")
async def add_channel_prompt(bot: Robot, msg: Message):
    """برای اضافه کردن GUID کانال جدید، درخواست ورودی می‌کند."""
    if msg.chat_id != ADMIN_ID: return
    admin_session_data[msg.chat_id] = {'action': 'add_channel'}
    await msg.answer("✍️ لطفا GUID کانال را وارد کنید (معمولاً با 'c' شروع می‌شود):")

@bot.on_callback("btn_del_channel_prompt")
async def delete_channel_prompt(bot: Robot, msg: Message):
    """برای حذف کانال، شماره آن را درخواست می‌کند."""
    if msg.chat_id != ADMIN_ID: return
    if not channels_data:
        await msg.answer("❌ هیچ کانالی برای حذف وجود ندارد.")
        return
    
    text = "📋 لیست کانال‌ها:\n" + "\n".join([f"{i+1}. {info.get('username', info.get('guid', 'نامعلوم'))}" for i, (guid, info) in enumerate(channels_data.items())])
    await msg.answer(text + "\n\nشماره کانالی که می‌خوای حذف شه رو بفرست:")
    admin_session_data[msg.chat_id] = {'action': 'delete_channel'}

@bot.on_callback("btn_edit_channel_prompt")
async def edit_channel_prompt(bot: Robot, msg: Message):
    """برای ویرایش کانال، شماره آن را درخواست می‌کند."""
    if msg.chat_id != ADMIN_ID: return
    if not channels_data:
        await msg.answer("❌ هیچ کانالی برای ویرایش وجود ندارد.")
        return
    
    text = "📋 لیست کانال‌ها:\n" + "\n".join([f"{i+1}. {info.get('username', info.get('guid', 'نامعلوم'))}" for i, (guid, info) in enumerate(channels_data.items())])
    await msg.answer(text + "\n\nشماره کانالی که می‌خوای ویرایش کنی رو بفرست:")
    admin_session_data[msg.chat_id] = {'action': 'edit_channel'}



@bot.on_callback("btn_settings")
async def settings_panel(bot: Robot, msg: Message):
    """پنل تنظیمات متنی را برای ویرایش پیام‌ها نمایش می‌دهد."""
    if msg.chat_id != ADMIN_ID: return

    settings_text = "⚙️ تنظیمات متنی ربات:\n\n"
    settings_text += "برای ویرایش هر متن، روی دکمه مربوطه کلیک کنید:\n\n"

    settings_kb = ChatKeypadBuilder()
    
    settings_kb.row(ChatKeypadBuilder().button("btn_edit_setting:join_channel_text", "📝 متن جوین اجباری"))
    settings_kb.row(ChatKeypadBuilder().button("btn_edit_setting:welcome_message", "👋 پیام خوش‌آمدگویی"))
    
    settings_kb.row(ChatKeypadBuilder().button(id="back_to_admin_panel", text="بازگشت"))

    await msg.reply(settings_text, inline_keypad=settings_kb.build())

@bot.on_callback("btn_edit_setting:")
async def edit_setting_prompt(bot: Robot, msg: Message):
    """فرآیند ویرایش یک تنظیمات خاص را آغاز می‌کند."""
    if msg.chat_id != ADMIN_ID: return
    parts = msg.aux_data.button_id.split(":")
    if len(parts) == 2:
        setting_key = parts[1]
        current_text = app_settings.get(setting_key, "متنی یافت نشد.")
        
        admin_session_data[msg.chat_id] = {
            'action': 'edit_setting',
            'editing_setting_key': setting_key
        }
        
        await msg.answer(f"✍️ لطفا متن جدید را برای '{setting_key}' وارد کنید:\n\n"
                         f"متن فعلی:\n{current_text}\n\n"
                         "جهت انصراف، دستور /cancel را ارسال کنید.")
    else:
        await msg.answer("خطای داخلی در انتخاب تنظیمات.")


@bot.on_callback("btn_view_all_proxies")
async def view_all_proxies(bot: Robot, msg: Message):
    """
    همه پروکسی‌های V2Ray را دریافت و نمایش می‌دهد.
    نکته: API ارائه شده ظاهراً قابلیتی برای لیست کردن همه پروکسی‌ها یا نام آن‌ها ندارد.
    این تابع یک پیام اطلاع‌رسانی نمایش می‌دهد.
    """
    if msg.chat_id != ADMIN_ID: return
    await msg.reply("در حال حاضر API قابلیت نمایش لیست کامل پروکسی‌ها را ندارد.\n"
                    "برای مشاهده جزئیات، می‌توانید از قابلیت 'ادیت نام پروکسی V2Ray' استفاده کرده و سپس پروکسی را وارد کنید تا اطلاعات آن نمایش داده شود.")


@bot.on_callback("btn_stats")
async def stats_panel(bot: Robot, msg: Message):
    """آمار کاربران را نمایش می‌دهد."""
    if msg.chat_id != ADMIN_ID: return

    total_users = len(users_data)
    if total_users == 0:
        stats_text = "تاکنون هیچ کاربری از ربات استفاده نکرده است."
    else:
        active_users_today = 0
        current_time = int(time.time())
        for user_guid, data in users_data.items():
            if current_time - data.get("last_active", 0) < 24 * 3600: 
                active_users_today += 1

        stats_text = f"📊 آمار کاربران:\n\n"
        stats_text += f"تعداد کل کاربران: {total_users}\n"
        stats_text += f"کاربران فعال امروز: {active_users_today}\n"
        
        
        
        
        
        

    stats_kb = (
        ChatKeypadBuilder()
        .row(ChatKeypadBuilder().button(id="back_to_admin_panel", text="بازگشت به پنل مدیریت"))
        .build()
    )
    await msg.reply(stats_text, inline_keypad=stats_kb)


@bot.on_callback("btn_broadcast")
async def broadcast_prompt(bot: Robot, msg: Message):
    """برای ارسال پیام همگانی، پیام را درخواست می‌کند."""
    if msg.chat_id != ADMIN_ID: return

    admin_session_data[msg.chat_id] = {'action': 'broadcast_message'}
    await msg.answer("📝 لطفا پیامی که می‌خواهید به همه کاربران ارسال شود را وارد کنید:\n\n"
                     "جهت انصراف، دستور /cancel را ارسال کنید.")

async def send_message_to_user(user_guid: str, message_text: str):
    """تلاش برای ارسال پیام به یک کاربر تکی."""
    try:
        await bot.send_message(user_guid, message_text)
        return True
    except Exception as e:
        print(f"ناموفق در ارسال پیام به کاربر {user_guid}: {e}")
        
        
        return False

@bot.on_message(filters.is_text)
async def handle_admin_text_messages(bot: Robot, msg: Message):
    """تمام پیام‌های متنی ورودی برای عملیات ادمین را با استفاده از دیکشنری سراسری admin_session_data هندل می‌کند."""

    
    if msg.chat_id == ADMIN_ID:
        session_data = admin_session_data.get(msg.chat_id)
        action = session_data.get('action') if session_data else None
        text = (msg.text or "").strip()

        
        if text == "/cancel" and action in [
            "add_channel", "delete_channel", "edit_channel",
            "edit_channel_step2", "edit_channel_step3", "edit_setting",
            "broadcast_message", "edit_v2ray_proxy_step1", "edit_v2ray_proxy_step2" 
        ]:
            print(f"لغو عملیات: {action} برای chat_id: {msg.chat_id}")
            admin_session_data.pop(msg.chat_id, None)
            await msg.reply("عملیات لغو شد.")
            return

        

        
        if action == "add_channel":
            channel_guid = text
            if not channel_guid:
                await msg.reply("❌ GUID کانال نمی‌تواند خالی باشد.")
                return

            channel_info = await get_channel_info(channel_guid)

            if channel_guid not in channels_data:
                channels_data[channel_guid] = channel_info
                save_channels_data()
                await msg.reply(f"✅ کانال با GUID '{channel_guid}' اضافه شد.")
                await msg.reply("اگر ربات ادمین کانال نیست یا لینک دعوت عمومی ندارد، لطفا از طریق پنل تنظیمات، لینک و نام کاربری را دستی وارد کنید.")
            else:
                await msg.reply("⚠️ این کانال قبلا اضافه شده است.")

            admin_session_data.pop(msg.chat_id, None)
            await manage_channels_panel(bot, msg) 
            return

        
        elif action == "delete_channel":
            try:
                index_to_delete = int(text) - 1
                if 0 <= index_to_delete < len(channels_data):
                    guids = list(channels_data.keys())
                    channel_guid_to_delete = guids[index_to_delete]
                    removed_info = channels_data.pop(channel_guid_to_delete)
                    save_channels_data()
                    await msg.reply(f"✅ کانال «{removed_info.get('username', channel_guid_to_delete)}» حذف شد.")
                else:
                    await msg.reply("❌ شماره نامعتبره.")
            except ValueError:
                await msg.reply("❌ لطفا فقط شماره را وارد کنید.")
            except Exception as e:
                await msg.reply(f"❌ خطایی رخ داد: {e}")

            admin_session_data.pop(msg.chat_id, None)
            await manage_channels_panel(bot, msg) 
            return

        
        elif action == "edit_channel":
            try:
                index_to_edit = int(text) - 1
                if 0 <= index_to_edit < len(channels_data):
                    guids = list(channels_data.keys())
                    channel_guid_to_edit = guids[index_to_edit]

                    admin_session_data[msg.chat_id] = {
                        'action': 'edit_channel_step2',
                        'editing_channel_guid': channel_guid_to_edit
                    }
                    current_info = channels_data[channel_guid_to_edit]
                    await msg.answer(
                        f"✍️ اطلاعات فعلی کانال:\n"
                        f"نام کاربری: {current_info.get('username')}\n"
                        f"لینک: {current_info.get('link')}\n\n"
                        "لطفا نام کاربری جدید را وارد کنید (اگر نمی‌خواهید تغییر کند، Enter بزنید):"
                    )
                else:
                    await msg.reply("❌ شماره نامعتبره.")
            except ValueError:
                await msg.reply("❌ لطفا فقط شماره را وارد کنید.")
            except Exception as e:
                await msg.reply(f"❌ خطایی رخ داد: {e}")
            return

        
        elif action == "edit_channel_step2":
            editing_channel_guid = session_data.get("editing_channel_guid")
            if not editing_channel_guid:
                await msg.reply("❌ خطای داخلی: GUID کانال ویرایش شونده یافت نشد.")
                admin_session_data.pop(msg.chat_id, None)
                return

            new_username = text
            if not new_username:  
                new_username = channels_data[editing_channel_guid].get("username")

            admin_session_data[msg.chat_id]['action'] = 'edit_channel_step3'
            admin_session_data[msg.chat_id]['new_username'] = new_username

            await msg.answer(
                f"✍️ نام کاربری کانال به '{new_username or 'خالی'}' تنظیم شد.\n"
                "لطفا لینک دعوت جدید را وارد کنید (مثال: https://rubika.ir/joinchat/XXXXXX)\n"
                "اگر نمی‌خواهید تغییر کند، فقط Enter بزنید:"
            )
            return

        
        elif action == "edit_channel_step3":
            editing_channel_guid = session_data.get("editing_channel_guid")
            new_username = session_data.get("new_username")
            new_link = text

            if not editing_channel_guid:
                await msg.reply("❌ خطای داخلی: GUID کانال ویرایش شونده یافت نشد.")
                admin_session_data.pop(msg.chat_id, None)
                return

            if not new_link:  
                new_link = channels_data[editing_channel_guid].get("link")

            channels_data[editing_channel_guid]["username"] = new_username
            channels_data[editing_channel_guid]["link"] = new_link
            save_channels_data()

            await msg.reply("✅ اطلاعات کانال با موفقیت به‌روزرسانی شد.")
            admin_session_data.pop(msg.chat_id, None)
            await manage_channels_panel(bot, msg) 
            return

        
        elif action == "edit_setting":
            setting_key = session_data.get("editing_setting_key")
            if not setting_key:
                await msg.reply("❌ خطای داخلی: کلید تنظیمات یافت نشد.")
                admin_session_data.pop(msg.chat_id, None)
                return

            app_settings[setting_key] = text
            save_settings()
            await msg.reply(f"✅ متن '{setting_key}' با موفقیت به‌روزرسانی شد.")

            admin_session_data.pop(msg.chat_id, None)
            await settings_panel(bot, msg) 
            return

        
        elif action == "broadcast_message":
            broadcast_text = text
            if not broadcast_text:
                await msg.reply("❌ متن پیام همگانی نمی‌تواند خالی باشد.")
                return

            
            success_count = 0
            fail_count = 0
            all_user_guids = list(users_data.keys()) 
            total_users_to_broadcast = len(all_user_guids)

            if total_users_to_broadcast == 0:
                await msg.reply("❌ هیچ کاربری برای ارسال پیام یافت نشد. ابتدا ربات را استارت کنید.")
                admin_session_data.pop(msg.chat_id, None)
                return

            
            await msg.reply(f"درحال ارسال پیام به {total_users_to_broadcast} کاربر...")

            for user_guid in all_user_guids:
                if await send_message_to_user(user_guid, broadcast_text):
                    success_count += 1
                else:
                    fail_count += 1
                await asyncio.sleep(0.1) 

            await msg.reply(f"✅ ارسال پیام همگانی به پایان رسید.\n"
                            f"تعداد پیام‌های موفق: {success_count}\n"
                            f"تعداد پیام‌های ناموفق: {fail_count}")

            admin_session_data.pop(msg.chat_id, None)
            await admin_panel(bot, msg) 
            return

        
        elif action == "edit_v2ray_proxy_step1": 
            session_data['v2ray_proxy'] = text 
            session_data['edit_stage'] = 'edit_v2ray_proxy_step2' 
            await msg.reply("✏️ حالا نام جدید را برای این پروکسی وارد کنید:")

        elif action == "edit_v2ray_proxy_step2": 
            session_data['v2ray_name'] = text 
            
            proxy_text = session_data.get('v2ray_proxy')
            name_text = session_data.get('v2ray_name')
            
            if not proxy_text or not name_text:
                await msg.reply("❌ اطلاعات پروکسی یا نام جدید ناقص است. لطفاً دوباره امتحان کنید.")
                if msg.chat_id in admin_session_data: del admin_session_data[msg.chat_id]
                return

            
            result = await edit_v2ray_proxy(proxy_text, name_text)
            if result.get("ok"):
                edited = result.get("result", "")
                await msg.reply(f"✅ پروکسی با موفقیت ویرایش شد:\n\nEdited : {edited}")
            else:
                error_msg = result.get("error", "خطای ناشناخته")
                await msg.reply(f"❌ خطا در ویرایش پروکسی: {error_msg}")
            
            
            admin_session_data.pop(msg.chat_id, None)
            return 

        
        if action:
            print(f"هشدار: عملیات نامعلوم '{action}' برای chat_id {msg.chat_id}، پاک کردن جلسه.")
            admin_session_data.pop(msg.chat_id, None)

    
    elif msg.chat_id in admin_session_data and admin_session_data[msg.chat_id].get('edit_stage'):
        session_data = admin_session_data[msg.chat_id]
        edit_stage = session_data.get('edit_stage')
        text = (msg.text or "").strip()

        if text == "/cancel":
            if msg.chat_id in admin_session_data: del admin_session_data[msg.chat_id]
            await msg.reply("عملیات لغو شد.")
            return
        
        if edit_stage == 'await_proxy': 
            session_data['v2ray_proxy'] = text
            session_data['edit_stage'] = 'await_name' 
            await msg.reply("✏️ حالا نام جدید را وارد کنید:")
        
        elif edit_stage == 'await_name': 
            session_data['v2ray_name'] = text
            
            proxy_text = session_data.get('v2ray_proxy')
            name_text = session_data.get('v2ray_name')
            
            if not proxy_text or not name_text:
                await msg.reply("❌ اطلاعات پروکسی یا نام جدید ناقص است. لطفاً دوباره امتحان کنید.")
                if msg.chat_id in admin_session_data: del admin_session_data[msg.chat_id]
                return

            
            result = await edit_v2ray_proxy(proxy_text, name_text)
            if result.get("ok"):
                edited = result.get("result", "")
                await msg.reply(f"✅ پروکسی با موفقیت ویرایش شد:\n\nEdited : {edited}")
            else:
                error_msg = result.get("error", "خطای ناشناخته")
                await msg.reply(f"❌ خطا در ویرایش پروکسی: {error_msg}")
            
            
            admin_session_data.pop(msg.chat_id, None)



@bot.on_callback("back_to_admin_panel")
async def back_to_admin(bot: Robot, msg: Message):
    """به پنل اصلی مدیریت برمی‌گردد."""
    if msg.chat_id != ADMIN_ID: return

    admin_kb = (
        ChatKeypadBuilder()
        .row(
            ChatKeypadBuilder().button("btn_manage_channels", "🔗 مدیریت کانال‌ها"),
            ChatKeypadBuilder().button("btn_settings", "⚙️ تنظیمات متنی")
        )
        .row(
            ChatKeypadBuilder().button("btn_view_all_proxies", "👁️ مشاهده پروکسی‌ها (V2Ray)"),
            ChatKeypadBuilder().button("btn_stats", "📊 آمار کاربران")
        )
        .row(
            ChatKeypadBuilder().button("btn_broadcast", "📢 ارسال همگانی")
        )
        .build()
    )
    await msg.reply("📌 پنل مدیریت:", inline_keypad=admin_kb)


async def main():
    await bot.run()
    print("ربات پروکسی متوقف شد.")

if __name__ == "__main__":
    
    load_data()
    asyncio.run(main())
