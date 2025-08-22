import asyncio
from rubka.asynco import Robot
from rubka.update import Message

bot = Robot("")
#ربات باید در کانال ادمین فول باشد و پس از ادمین کردن ربات داخل چنل دستور /start را داخل چنل ارسال کنید
channel_id = None
task = None
sleep = 10
async def send_backgrounds():
    while True:
        if channel_id:
            try:
                print(await bot.send_image(channel_id, "http://v3.api-free.ir/background/",text="✨ لحظه‌ای برای خودت، لحظه‌ای برای آرامش ✨\n\nID : @rubka_library"))
            except Exception as e:
                print("Error fetching background:", e)
        await asyncio.sleep(sleep)

@bot.on(commands=['start'])
async def handle_start(bot: Robot, message: Message):
    global channel_id, task
    channel_id = message.chat_id
    await bot.send_message(channel_id, "✅ ربات در چنل فعال شد و شروع به ارسال بک‌گراند می‌کند")
    if task is None:
        task = asyncio.create_task(send_backgrounds())

asyncio.run(bot.run())
