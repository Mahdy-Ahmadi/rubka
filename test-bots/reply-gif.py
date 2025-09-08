import asyncio
from rubka.asynco import Robot
from rubka.context import Message

bot = Robot("token")

@bot.on_message(commands=['start'])
async def handle_start(bot: Robot, message: Message):
    print(
        await message.reply_gif("https://gifgif.ir/ariaApp/gifgif/files/du/video_gallery/k96DTsGSxrBOJpViu2LHy.mp4",text="تست ریپلای گیف")
    )
    print(
        await message.reply_music("https://v.delgarm.com/mp3/804/2023/11/13/6551f92d8fca5.mp3",text="تست ریپلای موزیک")
    )

asyncio.run(bot.run())
