import asyncio
from rubka.asynco import Robot, filters
from rubka.context import Message

bot = Robot(token="token")

@bot.on_message(filters.is_group & filters.is_command)
async def handle_group_message(bot: Robot, message: Message):
    print(message.__dict__)
    sent = await message.reply("⏳ لطفاً صبر کنید...")
    await asyncio.sleep(2)
    await bot.delete_message(
        chat_id=message.chat_id,
        message_id=message.message_id,
    )
    await bot.delete_message(
        chat_id=message.chat_id,
        message_id=sent["data"]["message_id"],
    )
    
async def main():
    await bot.run()
if __name__ == "__main__":asyncio.run(main())
