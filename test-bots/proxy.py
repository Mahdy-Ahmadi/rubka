import asyncio, random, aiohttp
from rubka.asynco import Robot, Message, filters
from rubka.button import ChatKeypadBuilder

TOKEN = ""
API_V2RAY = "https://v3.api-free.ir/v2ray/"
API_TELEGRAM = "https://api-free.ir/api/proxy.php"
API_EDIT_V2RAY = "https://v3.api-free.ir/v2ray/edit.php"

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

async def edit_v2ray_proxy(proxy: str, name: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_EDIT_V2RAY}?proxy={proxy}&name={name}") as resp:
            return await resp.json()

inline_keypad = (ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button("get_telegram_proxy", "📱 پروکسی تلگرام"),
        ChatKeypadBuilder().button("get_v2ray_proxy", "💻 پروکسی V2Ray"))
    .row(
        ChatKeypadBuilder().button("edit_v2ray_name", "✏️ ادیت نام پروکسی V2Ray"))
    .build())


@bot.on_message(filters.is_command.start)
async def handler(bot: Robot, msg: Message):
    await msg.reply(
        f"👋 سلام {await bot.get_name(msg.chat_id)} !\n\nبا دکمه‌های زیر می‌تونی پروکسی مورد نظرت رو دریافت یا ویرایش کنی:",
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
@bot.on_callback("edit_v2ray_name")
async def edit_v2ray_name_button(bot, msg: Message):
    msg.session['edit_stage'] = 'await_proxy'
    await msg.reply("💻 لطفاً ابتدا پروکسی V2Ray را وارد کنید:")

@bot.on_message(filters.is_text)
async def handle_edit_steps(bot: Robot, msg: Message):
    stage = msg.session.get('edit_stage')
    if not stage:
        return
    
    if stage == 'await_proxy':
        msg.session['v2ray_proxy'] = msg.text.strip()
        msg.session['edit_stage'] = 'await_name'
        await msg.reply("✏️ حالا نام جدید را وارد کنید:")
    
    elif stage == 'await_name':
        msg.session['v2ray_name'] = msg.text.strip()
        proxy_text = msg.session.get('v2ray_proxy')
        name_text = msg.session.get('v2ray_name')
        
        result = await edit_v2ray_proxy(proxy_text, name_text)
        if result.get("ok"):
            edited = result.get("result", "")
            await msg.reply(f"✅ پروکسی با موفقیت ویرایش شد:\n\nEdited : {edited}")
        else:
            await msg.reply("❌ خطا در ویرایش پروکسی.")
        
        
        msg.session.pop('edit_stage', None)
        msg.session.pop('v2ray_proxy', None)
        msg.session.pop('v2ray_name', None)



async def main():
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
