from rubka.asynco import Robot, Message,filters

ADMIN_ID = "" #سندر ایدی ادمین ربات
TOKEN = "" # توکن شما

bot = Robot(TOKEN)

@bot.on_message(filters.is_group)
async def handle_admin_message(bot: Robot, message: Message):
    if message.sender_id != ADMIN_ID:return
    await message.delete()
    if message.is_photo:
        file_url = await bot.get_url_file(message.file.file_id)
        await bot.send_image(
            message.chat_id,
            file_url,
            text=message.text,
            reply_to_message_id=message.reply_to_message_id or None
        )
        return
    if message.text:
        await bot.send_message(
            message.chat_id,
            message.text,
            reply_to_message_id=message.reply_to_message_id or None
        )

bot.run()
