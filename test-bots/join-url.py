from rubka.asynco import Robot
from rubka.context import Message
from rubka.button import InlineBuilder
import asyncio

bot = Robot("token")

@bot.on_update(commands=['start'])
async def start(bot: Robot, message: Message):
    user_name = await bot.get_name(message.chat_id)
    buttons = (InlineBuilder()
        .row(
            InlineBuilder().button_join_channel(
                text="📢 Join Our Channel",
                id="join",
                username="api_dev")
            ,
            InlineBuilder().button_url_link(
                text="🌐 Visit Website",
                id="website",
                url="https://api-free.ir")
        ).build()
    )
    welcome_text = (
        f"👋 Hello {user_name} !\n\n"
        "📚 Welcome to the < Rubka Library Bot >.\n"
        "Before using the bot, please join our official channel "
        "and feel free to explore our website for more resources."
    )
    await message.reply_inline(text=welcome_text,inline_keypad=buttons)

asyncio.run(bot.run())
