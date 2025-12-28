from rubka import Robot,Message,ChatKeypadBuilder

bot = Robot("token")

items = [
    {"text": "سیب","image_url": "https://upload.wikimedia.org/wikipedia/commons/1/15/Red_Apple.jpg","type": "TextImgBig"},
    {"text": "موز","image_url": "https://upload.wikimedia.org/wikipedia/commons/8/8a/Banana-Single.jpg","type": "TextImgBig"}
]

kb = ChatKeypadBuilder()
keypad = (
    kb
    .row(
        kb.button_selection_items(
            id="2",
            button_text="انتخاب میوه",
            selection_id="fruit_select_1",
            title="انتخاب میوه",
            items=items
        )
    )
    .build()
)

@bot.on_message()
async def start(bot:Robot,message:Message):
    await message.reply_inline("سلام میوه",keypad)

bot.run()
