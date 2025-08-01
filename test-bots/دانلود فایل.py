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
        file_path = "name.mp3"
        downloaded = await bot.download(message.file.file_id, file_path)
        
        if downloaded:
            sent = await bot.send_file(
                chat_id=message.chat_id,
                path=file_path,
                caption="عه 🎵",
                file_name="music.mp3",
                reply_to_message_id=message.message_id
            )
        else:
            await message.reply("❌ دانلود فایل با مشکل مواجه شد.")
    except Exception as e:
        await message.reply(f"خطا هنگام پردازش فایل:\n{str(e)}")
asyncio.run(bot.run())
