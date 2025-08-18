import asyncio
from rubka.asynco import Robot
from rubka.context import Message

bot = Robot("token")
@bot.on_message()
async def handle_message(bot: Robot, message: Message):
    await bot.send_button_join(
        chat_id=message.chat_id,
        text="سلام خوش آمدید جهت ادامه عضو شوید",
        title_button="عضویت",
        username="rubka_library",
        reply_to_message_id=message.message_id
    )

asyncio.run(
    bot.run(
        debug=True,
        sleep_time=0
    )
)
