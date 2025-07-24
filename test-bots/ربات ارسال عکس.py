from rubka import Robot
from rubka.keypad import ChatKeypadBuilder
from rubka.button import InlineBuilder
from rubka.context import Message
chat_keypad = ChatKeypadBuilder().row(
    ChatKeypadBuilder().button(id="btn_female", text="زن"),
    ChatKeypadBuilder().button(id="btn_male", text="مرد")
).build()
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
bot = Robot("token")
@bot.on_message()
def handler(bot: Robot, message: Message):
    message.reply_image(
        path="https://s6.uupload.ir/files/chatgpt_image_jul_20,_2025,_10_22_47_pm_oiql.png",
        text="📷 عکس ریپلای شده دکمه شیشه ای",
        inline_keypad=inline_keypad
    )
    print(message.reply_image(
        path="https://s6.uupload.ir/files/chatgpt_image_jul_20,_2025,_10_22_47_pm_oiql.png",
        text="📷 عکس ریپلای شده دکمه کیبوردی",
        chat_keypad=chat_keypad,
        chat_keypad_type="New"
    ))
@bot.on_callback()
def callback_handler(bot: Robot, message: Message):
    data = message.aux_data.button_id
    if data == "btn_male":message.reply("سلام مرد")
    elif data == "btn_female":message.reply("سلام زن")
    else:message.reply_text(f"دکمه ناشناخته: {data}")
bot.run()
