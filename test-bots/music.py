import asyncio
from rubka.asynco import Robot
from rubka.context import Message

bot = Robot("token",show_progress=True)

@bot.on_message()
async def handle_message(bot: Robot, message: Message):
    if not message.file:
        await message.reply("لطفاً یک فایل ارسال کنید.")
        return
    try:
        file_path = "name.ogg"
        downloaded = await bot.download(message.file.file_id, file_path)
        
        if downloaded:
            sent = await bot.send_music(
                chat_id=message.chat_id,
                path=file_path,
                text="عه 🎵",
                file_name="music.ogg",
                reply_to_message_id=message.message_id
            )
        else:
            await message.reply("❌ دانلود فایل با مشکل مواجه شد.")
    except Exception as e:
        await message.reply(f"خطا هنگام پردازش فایل:\n{str(e)}")
asyncio.run(bot.run())
