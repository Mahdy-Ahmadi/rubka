from rubka.asynco import Robot, Message, filters

ADMIN_ID = "" #سندر ایدی ادمین گپ

bot = Robot("token",api_endpoint="messenger")

@bot.on_message(filters.sender_id_is(ADMIN_ID))
async def handle_admin_message(bot: Robot, message: Message):
    await message.delete()
    await message.copy_message(message.chat_id,message.reply_to_message_id or None)
    
bot.run(sleep_time=0)
