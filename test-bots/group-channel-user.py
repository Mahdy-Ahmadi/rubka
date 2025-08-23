import asyncio
from rubka.asynco import Robot
from rubka.context import Message

bot = Robot("")

@bot.on_message_channel(commands=['start'])
async def handle_channel(bot: Robot, message: Message):
    
    await message.reply_image(
        path="https://s6.uupload.ir/files/ef61798e-8986-46a2-9769-fa2be838cddd_oj4b.jpeg",
        text="I received this message in the channel.")

@bot.on_message_group(commands=['start'])
async def handle_group(bot: Robot, message: Message):
    message.session()
    await message.reply_image(
        path="https://s6.uupload.ir/files/ef61798e-8986-46a2-9769-fa2be838cddd_oj4b.jpeg",
        text="I received this message in the group.")

@bot.on_message_private(commands=['start'])
async def handle_private(bot: Robot, message: Message):
    print(await message.reply_image(
        path="https://s6.uupload.ir/files/ef61798e-8986-46a2-9769-fa2be838cddd_oj4b.jpeg",
        text="I received this message in private chat."))

asyncio.run(bot.run())
