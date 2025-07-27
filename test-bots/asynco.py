import asyncio
from rubka.asynco import Robot
from rubka.context import Message

bot = Robot("token")

@bot.on_message(commands=['start'])
async def handle_start(bot: Robot, message: Message):
    name = await bot.get_name(message.chat_id)
    await message.reply(f"سلام {name} حالت چطوره ؟")

@bot.on_message(commands=['help'])
async def handle_(bot: Robot, message: Message):
    name = await bot.get_name(message.chat_id)
    await message.reply(f"سلام {name} راهنما")

asyncio.run(bot.run())
