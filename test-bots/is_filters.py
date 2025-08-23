import asyncio
from rubka.asynco import Robot
from rubka.context import Message

bot = Robot("")

@bot.on_message()
async def handle_channel(bot: Robot, message: Message):
    if message.is_channel:
        await message.reply("I received this message in the channel.")
    if message.is_group:
        await message.reply("I received this message in the group.")
    if message.is_user:
        await message.reply("I received this message in the user.")

asyncio.run(bot.run())
