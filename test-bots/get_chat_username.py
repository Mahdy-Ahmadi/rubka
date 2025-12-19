import requests
from rubka.asynco import Robot, Message, filters
from rubka.adaptorrubka import Client
from datetime import datetime
import jdatetime

username_acc = "servers_dev" #یوزرنیم اکانتی که میخواید سلف واردش بشه
Token = "token" #توکن ربات


bot = Robot(Token, show_progress=True)
Client = Client(session=username_acc)
def ts_to_jdate(ts) -> str:
    if not ts:
        return "-"
    try:
        dt = datetime.fromtimestamp(int(ts))
        jd = jdatetime.datetime.fromgregorian(datetime=dt)
        return jd.strftime("%Y/%m/%d")
    except Exception:
        return "-"
def yes_no(value) -> str:
    return "✅ بله" if value else "❌ خیر"
def get_birthday(user: dict, info: dict) -> str:
    for key in ("birth_date", "birthday", "date_of_birth"):
        if user.get(key):
            return ts_to_jdate(user.get(key))
        if info.get(key):
            return ts_to_jdate(info.get(key))
    return "-"
def fetch_profile_info(username: str) -> dict:
    url = f"https://rubka.atlas.fastsub.site/rub/?user={username}"
    response = requests.get(url)
    return response.json()
def format_user_account(data: dict, profile_info: dict,chat_id,sender_id) -> str:
    user = data.get("user") or {}
    info = data.get("user_additional_info") or {}
    avatar = user.get("avatar_thumbnail") or {}
    online = user.get("online_time") or {}
    bio = (user.get("bio") or "").replace("\u200c", "").strip()
    birthday = get_birthday(user, info)
    registration_time = info.get("registration_time")
    profile_data = profile_info.get("profile", {})
    full_name = profile_data.get("name", "-")
    profile_status = profile_data.get("profile_status", "-")
    follower_count = profile_data.get("follower_count", 0)
    following_count = profile_data.get("following_count", 0)
    post_count = profile_data.get("post_count", 0)
    bio_from_api = profile_data.get("bio", "-")
    chat_link = profile_data.get("chat_link", {}).get("open_chat_data", {}).get("object_guid", "-")
    store_id = profile_data.get("store_id", "-")
    tag_post = profile_data.get("tag_post", "-")
    is_top_store = profile_data.get("is_top_store", False)
    track_id = profile_data.get("track_id", "-")
    in_following_list = profile_data.get("in_following_list", False)
    i_request = profile_data.get("i_request", False)
    in_blocked_list = profile_data.get("in_blocked_list", False)
    story_status = profile_data.get("story_status", "-")
    has_live = profile_data.get("has_live", False)
    has_profile_link_item = profile_data.get("has_profile_link_item", False)
    if registration_time:
        activity_section = f"""
**🕒 فعالیت اکانت**

$آخرین وضعیت آنلاین : {online.get("approximate_period", "-")}
تاریخ ثبت‌نام       : {ts_to_jdate(registration_time)}
آخرین تغییر عکس     : {ts_to_jdate(info.get("photo_changed_time"))}
آخرین تغییر نام     : {ts_to_jdate(info.get("name_changed_time"))}$
""".strip()
    else:
        activity_section = f"""
**🕒 فعالیت اکانت**

$برای دریافت اطلاعات بیشتر از اکانت خود
ابتدا یک پیام نقطه به آیدی `{username_acc}` ارسال نمایید$
""".strip()
    output = f"""
**👤 اطلاعات اکانت**

$نام              : {user.get("first_name", "-")}
نام کاربری       : @{user.get("username", "-")}
شناسه کاربر      : `{user.get("user_guid", "-")}`
چت ایدی : `{chat_id}`
سندر ایدی : `{sender_id}`
کشور             : {info.get("country_code", "-")}
تاریخ تولد       : {birthday}
تیک آبی   : {yes_no(user.get("is_verified"))}
قبلا حذف شده : {yes_no(user.get("is_deleted"))}$

**🖼 اطلاعات عکس پروفایل**

$شناسه فایل        : {avatar.get("file_id", "-")}
نوع فایل          : {avatar.get("mime", "-")}
مرکز داده (DC)    : {avatar.get("dc_id", "-")}$

**💬 اطلاعات روبینو**
$
نام کامل         : {full_name}
وضعیت پروفایل    : {profile_status}
تعداد فالوورها    : {follower_count}
تعداد فالوینگ‌ها  : {following_count}
تعداد پست‌ها      : {post_count}
بیوگرافی         : {bio_from_api}
لینک چت           :  [چت با کاربر](https://rubika.ir/{chat_link})
$

**📝 وضعیت فالو کردن و بلاک کردن**
$
در لیست فالوینگ‌ها : {yes_no(in_following_list)}
در لیست درخواست‌ها : {yes_no(i_request)}
در لیست بلاک شده‌ها : {yes_no(in_blocked_list)}
$

{activity_section}

**📝 بیوگرافی**

${bio if bio else "ندارد"}$

**📞 دسترسی‌ها**

>امکان تماس صوتی   : {yes_no(info.get("can_receive_call"))}
>امکان تماس تصویری : {yes_no(info.get("can_video_call"))}
""".strip()

    if avatar.get("file_id", "-"):
        return output, f'https://messenger{avatar.get("dc_id")}.iranlms.ir/InternFile.ashx?id={avatar.get("file_id")}&ach={avatar.get("access_hash_rec")}'
    return output, False

@bot.on_message(filters.is_private & filters.is_command.start)
async def geter(bot: Robot, message: Message):
    info = await message.author_info
    if not info.data.chat.username:return await message.reply(f">**این عملیات برای اکانت های دارای ایدی میباشد**")
    profile_info = fetch_profile_info(info.data.chat.username)
    chat_id = message.chat_id
    sender_id = message.sender_id
    if 'profile_info' in profile_info:
        profile_info_data = profile_info['profile_info']['data']
        data, url = format_user_account(Client.info_username(info.data.chat.username), profile_info_data,chat_id,sender_id)
        if url:return await message.reply_image(url, text=data)
        await message.reply(f"{data}")
    else:await message.reply("اطلاعات پروفایل یافت نشد.")
        
bot.run()
