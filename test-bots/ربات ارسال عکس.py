import asyncio
from rubka.asynco import Robot
from rubka.button import InlineBuilder,ChatKeypadBuilder
from rubka.context import Message

chat_keypad = (
    ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button(id="btn_female", text="زن"),
        ChatKeypadBuilder().button(id="btn_male", text="مرد")
    )
    .build()
)

inline_keypad = (
    InlineBuilder()
    .row(
        InlineBuilder().button_simple("btn_bets", "button1"),
        InlineBuilder().button_simple("btn_rps", "button2")
    )
    .row(
        InlineBuilder().button_simple("btn_chatid", "butthon3")
    )
    .build()
)

bot = Robot(
    "token",
    web_hook=None
)


@bot.on_message(commands=['start'])
async def handler(bot: Robot, message: Message):
    await message.reply_image(
        path="https://s6.uupload.ir/files/ef61798e-8986-46a2-9769-fa2be838cddd_oj4b.jpeg",
        text="📷 عکس ریپلای شده دکمه شیشه ای",
        inline_keypad=inline_keypad
    )

    resp = await message.reply_image(
        path="https://s6.uupload.ir/files/ef61798e-8986-46a2-9769-fa2be838cddd_oj4b.jpeg",
        text="📷 عکس ریپلای شده دکمه کیبوردی",
        chat_keypad=chat_keypad,
        chat_keypad_type="New"
    )
    print(resp)

@bot.on_callback('btn_male')
async def btn_male(bot: Robot, message: Message):
    await message.answer("سلام مرد")
    return

@bot.on_callback('btn_female')
async def btn_female(bot: Robot, message: Message):
    await message.answer("سلام زن")
    return

@bot.on_callback()
async def callback_handler(bot: Robot, message: Message):
    await message.answer(f"button : {message.aux_data.button_id}")
    return


if __name__ == "__main__":
    asyncio.run(bot.run())
