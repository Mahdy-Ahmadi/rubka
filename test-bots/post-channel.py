import asyncio
from rubka.asynco import Robot
from rubka.update import Message

bot = Robot("")


channel_id: str | None = None

task: asyncio.Task | None = None

SLEEP_INTERVAL = 10
BACKGROUND_URL = "http://v3.api-free.ir/background/"
CAPTION = "✨ لحظه‌ای برای خودت، لحظه‌ای برای آرامش ✨\n\nID : @rubka_library"

async def send_backgrounds():
    global channel_id
    while channel_id:
        try:
            
            result = await bot.send_image(channel_id, BACKGROUND_URL, text=CAPTION)
            print("Background sent:", result)
        except Exception as e:
            print(e)
        await asyncio.sleep(SLEEP_INTERVAL)

@bot.on_message_channel(commands=['start'])
async def handle_start(bot: Robot, message: Message):
    global channel_id, task

    channel_id = message.chat_id
    await bot.send_message(channel_id, "✅ ربات در کانال فعال شد و شروع به ارسال بک‌گراند می‌کند")
    
    if not task or task.done():
        task = asyncio.create_task(send_backgrounds())

if __name__ == "__main__":
    asyncio.run(bot.run())
