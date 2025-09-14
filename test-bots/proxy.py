import asyncio, random, aiohttp
from rubka.asynco import Robot, Message, filters
from rubka.button import ChatKeypadBuilder

TOKEN = ""
API_V2RAY = "https://v3.api-free.ir/v2ray/"
API_TELEGRAM = "https://api-free.ir/api/proxy.php"

bot = Robot(TOKEN)

async def get_random_v2ray():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_V2RAY) as resp:
            data = await resp.json()
            proxies = data.get("proxies", [])
            if not proxies:
                return None
            return random.choice(proxies)

async def get_random_telegram_proxy():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_TELEGRAM) as resp:
            data = await resp.json()
            proxies = data.get("result", [])
            if not proxies:
                return None
            return random.choice(proxies)

inline_keypad = (ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button("get_telegram_proxy", "📱 پروکسی تلگرام"),
        ChatKeypadBuilder().button("get_v2ray_proxy", "💻 پروکسی V2Ray"))
    .build())

@bot.on_message(filters.is_command.start)
async def handler(bot: Robot, msg: Message):
    await msg.reply(
        f"👋 سلام {await bot.get_name(msg.chat_id)} !\n\nبا دکمه‌های زیر می‌تونی پروکسی مورد نظرت رو دریافت کنی:",
        chat_keypad=inline_keypad
    )

@bot.on_callback("get_telegram_proxy")
async def telegram_proxy_button(bot, msg: Message):
    proxy = await get_random_telegram_proxy()
    if not proxy:
        await msg.reply("❌ پروکسی تلگرام پیدا نشد.")
        return
    await msg.reply(f"📱 Telegram Proxy:\n{proxy}")

@bot.on_callback("get_v2ray_proxy")
async def v2ray_proxy_button(bot, msg: Message):
    proxy = await get_random_v2ray()
    if not proxy:
        await msg.reply("❌ پروکسی V2Ray پیدا نشد.")
        return
    await msg.reply(f"💻 V2Ray Proxy :\n\nType : {proxy['type']}\n\nProxy : {proxy['proxy']}")

async def main():
    await bot.run()
if __name__ == "__main__":
    asyncio.run(main())
