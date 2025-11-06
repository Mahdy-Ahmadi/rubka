import aiohttp
from rubka.asynco import Robot, Message, filters

bot = Robot(
    "token",
    safeSendMode=True
)

async def fetch_poll():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.rubka.ir/poll", timeout=10) as response:
            return await response.json()

@bot.on_message(filters.text_contains_any(["چالش","کوییز","Quiz"]))
async def handle_challenge(bot: Robot, message: Message):
    sent = await message.reply("درحال دریافت اطلاعات چالش لطفا منتظر باشید...")
    try:
        poll_data = await fetch_poll()

        await bot.send_poll(
            chat_id=message.chat_id,
            question=poll_data["question"],
            options=poll_data["options"],
            type="Quiz",
            hint=poll_data.get("hint", ""),
            correct_option_index=0,
            reply_to_message_id=message.message_id
        )

        await sent.delete()
    except Exception as e:
        await sent.delete()
        await message.reply(f"Error {e}")

bot.run()
