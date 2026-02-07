from rubka import Robot,InlineBuilder,Message

inline_keypad = (
    InlineBuilder()
    .row(
        InlineBuilder().button_simple("one", "🎯 دکمه اول"),
        InlineBuilder().button_simple("two", "🧩 دکمه دوم")
    )
    .row(
        InlineBuilder().button_simple("3", "💬 دکمه سوم")
    )
    .build()
)

bot = Robot(
    "token",
    web_hook="https://webhook..."
)

@bot.on_message(commands=['start'])
async def start_handler(bot: Robot, message: Message):
    await message.reply(
        text="👋 خوش اومدی!\nزیرش دکمه‌های شیشه‌ای رو می‌بینی:",
        inline_keypad=inline_keypad
    )

@bot.on_callback("one")
async def callback_handler1(bot: Robot, message: Message):
    await message.answer(f"دکمه اول")
@bot.on_callback("two")
async def callback_handler1(bot: Robot, message: Message):
    await message.answer(f"دکمه 2")
@bot.on_callback("3")
async def callback_handler1(bot: Robot, message: Message):
    await message.answer(f"دکمه 3")

bot.run()
