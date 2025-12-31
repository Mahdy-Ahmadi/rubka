from rubka import Robot, Message,filters

bot = Robot("token")

bot.start_save_message()
@bot.on_message()
async def save_message(bot,message):return

@bot.on_message(filters.text_equals("بن"))
async def info(bot: Robot, message: Message):
    data = await bot.get_message(message.chat_id, message.reply_to_message_id)
    if await bot.ban_member_chat(chat_id=message.chat_id,user_id=data['sender_id']):
        await message.reply(f"> [کاربر]({data['sender_id']}) مورد نظر از گروه اخراج شد")

@bot.on_message(filters.text_equals("آن بن"))
async def info2(bot: Robot, message: Message):
    data = await bot.get_message(message.chat_id, message.reply_to_message_id)
    if await bot.unban_chat_member(chat_id=message.chat_id,user_id=data['sender_id']):
        await message.reply(f"[کاربر]({data['sender_id']}) مورد نظر از لیست سکوت خارج شد")

bot.run()
