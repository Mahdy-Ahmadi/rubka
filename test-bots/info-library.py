import aiohttp
import asyncio
from rubka.asynco import Robot
from rubka.context import Message
from rubka.button import InlineBuilder

BOT_TOKEN = "token"
bot = Robot(BOT_TOKEN)

API_IMG = "http://v3.api-free.ir/pypi/?name={pkg}"
API_JSON = "http://v3.api-free.ir/pypi/?name={pkg}&type=json"

user_states = {}

def build_inline_last_days(last_days):
    root = InlineBuilder()

    for day in last_days[:10]:
        date = day["date"]
        downloads = day["downloads"]

        btn_date = InlineBuilder().button_simple(f"date:{date}", date)
        btn_dl = InlineBuilder().button_simple(f"dl:{date}:{downloads}", str(downloads))
        btn_info = InlineBuilder().button_simple(f"info:{date}", "روز و دانلود ها")

        root = root.row(btn_date, btn_dl, btn_info)

    return root.build()

@bot.on_message()
async def handler(bot: Robot, message: Message):
    text = (message.text or "").strip()

    if text == "/start":
        user_states[message.sender_id] = "waiting_package"
        return await message.reply("👋 سلام!\nاسم کتابخونه پایتون رو بفرست تا اطلاعاتشو بدم.")

    if user_states.get(message.sender_id) == "waiting_package" and text:
        package = text
        data_send=await message.reply(f"🔎 در حال دریافت اطلاعات برای {package} ...")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_JSON.format(pkg=package)) as resp:
                    if resp.status != 200:
                        return await bot.edit_message_text(message.chat_id,data_send['data']['message_id'],"❌ دریافت اطلاعات ناموفق بود.")
                    data : dict = await resp.json()
        except Exception:
            return await bot.edit_message_text(message.chat_id,data_send['data']['message_id'],"❌ خطا در اتصال به وب‌سرویس.")
        if data.get("code",{}) == 404:
            return await bot.edit_message_text(message.chat_id,data_send['data']['message_id'],"نام کتابخانه در موارد جستجو شده موجود نیست")
        pkg = data.get("package", package)
        total = data.get("total_downloads", 0)
        last_days = data.get("last_days", [])

        caption = f"📦 پکیج: {pkg}\n📊 دانلود کل: {total:,}"

        inline_keypad = build_inline_last_days(last_days) if last_days else None

        await message.reply_image(
            path=API_IMG.format(pkg=package),
            text=caption,
            inline_keypad=inline_keypad
        )
        await bot.delete_message(message.chat_id,data_send['data']['message_id'])


if __name__ == "__main__":asyncio.run(bot.run())
