import asyncio
from rubka.asynco import Robot,filters,Message

bot = Robot("")

@bot.on_message_group(filters=filters.text_regex(r"(https?://|www\.|\.ir|\.com|\.net|t\.me|@\w+)"))
async def handle_start(bot: Robot, message: Message):
    await message.delete()

asyncio.run(bot.run())
