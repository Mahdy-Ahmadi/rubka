from rubka.asynco import Robot,Message

bot = Robot("")

@bot.on_message()
async def handle_start(bot: Robot, message: Message):
    name = await message.name
    await message.reply(
        f"your Name : {name}",
        delete_after=10
    )

bot.run()
