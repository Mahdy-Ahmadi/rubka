import asyncio
import requests
from rubka.asynco import Robot, Message, filters,InlineBuilder

bot = Robot("token")

@bot.on_message(filters.text_equals("چالش"))
async def handle_start(bot: Robot, message: Message):
    response = requests.get("https://api.rubka.ir/poll")
    poll_data = response.json()
    inline = (InlineBuilder().row(InlineBuilder().button_simple("0", "ربات چالش آنلاین")).build()) if message.is_private else None
    await bot.send_poll(
        message.chat_id,
        reply_to_message_id=message.message_id,
        question=poll_data['question'],
        options=poll_data['options'],
        type=poll_data['type'],
        allows_multiple_answers=poll_data['allows_multiple_answers'],
        is_anonymous=poll_data['is_anonymous'],
        correct_option_index= poll_data['correct_option_index'],
        hint=poll_data.get('hint'),
        show_results=poll_data['show_results'],
        inline_keypad=inline
    )
asyncio.run(bot.run())
