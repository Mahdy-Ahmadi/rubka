import asyncio,os,importlib,subprocess,sys
from rubka.asynco import Robot, Message, filters
from rubka.button import ChatKeypadBuilder
try:
    PyPi = importlib.import_module("pypi").PyPi
except ModuleNotFoundError:
    print(f"pypiget not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypiget"])
    PyPi = importlib.import_module("pypi").PyPi


TOKEN = ""
web_hook = "" #اگر وب هوک ندارید خالی بزار تا از دکمه کیبوردی استفاده کنه
# اگه میخواین از پیام شیشه ای بجای دکمه کیبوردی استفاده کنید نیاز به وب هوک داره و میتونید از panel.rubka.ir دریافت کنین وب هوک رایگان رو
bot = Robot(TOKEN, web_hook=web_hook)
session = PyPi()
user_last_sent = {}


user_pages = {}
user_states = {}  

inline_keypad = (
    ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button("get_pypi_package", "🔎 جستجوی پکیج PyPI")
    )
    .build()
)


@bot.on_message(filters.is_command.start)
async def start_handler(bot: Robot, msg: Message):
    print(msg.raw_data)
    await msg.reply(
        "👋 سلام! برای جستجوی پکیج PyPI روی دکمه زیر کلیک کن:",
        inline_keypad=inline_keypad if web_hook else None,
        chat_keypad=None if web_hook else inline_keypad
    )


@bot.on_callback("get_pypi_package")
async def get_pypi_package_button(bot, msg: Message):
    user_states[msg.chat_id] = 'await_package'
    await msg.reply("🔎 اسم پکیج مورد نظر را وارد کنید:")


@bot.on_callback("start")
async def handel_shoroe(bot, msg: Message):
    user_states[msg.chat_id] = 'await_package'
    await msg.reply(
        "👋 سلام! برای جستجوی پکیج PyPI روی دکمه زیر کلیک کن:",
        inline_keypad=inline_keypad if web_hook else None,
        chat_keypad=None if web_hook else inline_keypad
    )

@bot.on_message(filters.is_text)
async def handle_pypi(bot: Robot, msg: Message):
    if user_states.get(msg.chat_id) == 'await_package':
        package_name = msg.text.strip()
        try:
            data = await session.get_package_info(package_name)
            info = data.get("info", {})
            releases = data.get("releases", {})

            details = []
            for key, value in info.items():
                if key not in ("description", "summary"):
                    details.append(f"🔹 {key} : {value}")

            details.append(f"📂 تعداد نسخه‌ها: {len(releases)}")
            if releases:
                latest_version = info.get("version", "")
                if latest_version in releases:
                    details.append(f"📅 آخرین انتشار: {releases[latest_version][0].get('upload_time', 'نامشخص')}")

            chunk_size = 5
            pages = [details[i:i+chunk_size] for i in range(0, len(details), chunk_size)]
            pages = ["\n".join(p) for p in pages]

            user_pages[msg.chat_id] = pages

            reply_text = pages[0]
            keypad = (
                ChatKeypadBuilder()
                .row(ChatKeypadBuilder().button("next_page", "⏭️ ادامه"))
                .row(ChatKeypadBuilder().button("start", "پایان"))
                .build()
            ) if len(pages) > 1 else None

            sent = await msg.reply(reply_text, inline_keypad=keypad if web_hook else None,
                            chat_keypad=None if web_hook else keypad)

            user_last_sent[msg.chat_id] = sent

        except Exception as e:
            await msg.reply(f"❌ خطا در گرفتن اطلاعات پکیج:\n{e}")

        user_states.pop(msg.chat_id, None)


@bot.on_callback("next_page")
async def next_page(bot: Robot, msg: Message):
    user_id = msg.chat_id
    if user_id in user_pages and len(user_pages[user_id]) > 1:
        user_pages[user_id].pop(0)
        reply_text = user_pages[user_id][0]

        keypad = (
            ChatKeypadBuilder()
            .row(ChatKeypadBuilder().button("next_page", "⏭️ ادامه"))
            .row(ChatKeypadBuilder().button("start", "پایان"))
            .build()
        ) if len(user_pages[user_id]) > 1 else None

        last_msg = user_last_sent.get(user_id)
        print(last_msg)
        if last_msg:
            print(await bot.edit_message_text(msg.chat_id, last_msg.data.message_id, reply_text))
    else:
        await msg.reply("📌 توضیحات بیشتری وجود ندارد.")


async def main():
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
