import asyncio
from rubka.asynco import Robot,Message
from rubka.button import InlineBuilder

bot = Robot(token="")

@bot.on_message()
async def send_textbox(bot: Robot, message: Message):
    inline = (
        InlineBuilder()
        .row(
            InlineBuilder().button_textbox(
                id="enter_name",
                title="📝 وارد کردن نام",
                type_line="SingleLine",
                type_keypad="String",
                place_holder="نام خود را وارد کنید...",
                default_value=""
            )
        )
        .build()
    )
    await message.reply_inline("👤 لطفاً نام خود را وارد کنید:", inline_keypad=inline)

@bot.on_callback("enter_name")
async def receive_textbox(bot: Robot, message: Message):
    user_input = message.aux_data.start_id
    await message.reply(f"✅ نام وارد شده: {user_input}")

asyncio.run(bot.run())
