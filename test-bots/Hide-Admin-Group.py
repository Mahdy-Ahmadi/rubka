from rubka.asynco import Robot, Message, filters

ADMIN_ID = "u0HJtFl043f3d7e43bdc1f305ed42a11" #سندر ایدی ادمین گپ
TOKEN = "" # توکن ربات

bot = Robot(TOKEN)

@bot.on_message(filters.is_group)
async def handle_admin_message(bot: Robot, message: Message):
    if message.sender_id != ADMIN_ID:
        return
    try:
        send_methods = {
            "is_photo": bot.send_image,
            "is_video": bot.send_video,
            "is_document": bot.send_document,
            "is_text": bot.send_message
        }
        for attr, send_func in send_methods.items():
            if getattr(message, attr, False):
                await message.delete()
                kwargs = {
                    "chat_id": message.chat_id,
                    "text": message.text,
                    "reply_to_message_id": message.reply_to_message_id or None
                }
                if hasattr(message, "file") and message.file:
                    kwargs["path"] = await bot.get_url_file(message.file.file_id)
                await send_func(**kwargs)
                break
    except Exception as e:
        print(e)
bot.run(sleep_time=0)
