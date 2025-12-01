from rubka.asynco import Robot, Message, filters

ADMIN_ID = "" #سندر ایدی ادمین گپ

bot = Robot("token",api_endpoint="messenger")

bot.start_save_message(1000)

@bot.on_message()
async def handle_admin_message(bot: Robot, message: Message):
    if message.sender_id != ADMIN_ID:
        rules = [message.has_link,message.meta_links,message.is_link_meta,message.is_mention,message.is_forwarded]
        if any(rules):
            await message.reply(f"> ⛔ [کاربر]({message.sender_id}) ارسال لینک خلاف قوانین گروه است؛ لطفاً رعایت کنید.", 30)
            await message.delete()

@bot.on_message(filters.sender_id_is(ADMIN_ID))
async def handle_admin_message(bot: Robot, message: Message):
    await message.delete()
    reply_id = message.reply_to_message_id
    await message.copy_message(to_chat_id=message.chat_id, message_id=reply_id)
    if message.text in ["get","اطلاعات","info"] and reply_id:
        info = await bot.get_message(message.chat_id, reply_id)
        text = f"**Info Message:**\n\n>{info}"
        await bot.send_message(
            chat_id=message.chat_id,
            text=text,
            reply_to_message_id=reply_id
        )

bot.run(sleep_time=0)
