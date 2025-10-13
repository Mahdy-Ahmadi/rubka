import asyncio
from rubka.asynco import Robot,Message

bot = Robot("",show_progress=True)

@bot.on_message(commands=['info', 'start'])
async def handle_info(bot: Robot, message: Message):
    info = await message.author_info
    reply_text = (
        f"👋 سلام \n\n"
        f"ℹ️ you Info : \n{info}\n\nاین پیام بعد از 10 ثانیه حذف خواهد شد"
    )
    await message.reply(reply_text, delete_after=30)

@bot.on_message(commands=['image'])
async def handle_image(bot: Robot, message: Message):
    send = await message.reply("⏳ در حال بارگذاری...",delete_after=6)

    url = (
        await bot.get_avatar_me()
        or "https://s6.uupload.ir/files/ef61798e-8986-46a2-9769-fa2be838cddd_oj4b.jpeg"
    )

    sent = await message.reply_image(
        path=url,
        text="📷 این عکس به صورت موقت ارسال شده و پس از 5 ثانیه حذف خواهد شد"
    )
    await bot.delete_after(message.chat_id, sent.message_id, delay=5)

if __name__ == "__main__":
    asyncio.run(bot.run())
