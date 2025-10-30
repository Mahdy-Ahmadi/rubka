import asyncio
from rubka.asynco import Robot,Message

bot = Robot("token")

@bot.on_message()
async def handle_start(bot: Robot, message: Message):
    name = await message.author_name
    await message.reply(f"سلام {name} حالت چطوره ؟")

asyncio.run(bot.run())
