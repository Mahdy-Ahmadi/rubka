import asyncio
from rubka.asynco import Robot, Message, filters
from rubka.button import InlineBuilder


TOKEN = "" #توکن

bot = Robot(TOKEN, web_hook="https://direct.rubka.ir/users/09100000000/11111") #وب هوک

inline_keypad = (
    InlineBuilder().row(InlineBuilder().button_simple("start", "Start Robot"))
    .build()
)


@bot.on_message(filters.is_command.start)
async def start_handler(bot: Robot, msg: Message):
    await msg.reply_inline(
        text="Robot Start handel Inline Web hook",
        inline_keypad=inline_keypad
    )


@bot.on_callback("start")
async def get_pypi_package_button(bot, msg: Message):
    await msg.reply("پیغام استارت اینلاین دریافت شد")

asyncio.run(bot.run())
