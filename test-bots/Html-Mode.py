from rubka.asynco import Robot, Message

TOKEN = ""
bot = Robot(TOKEN)

@bot.on_message()
async def handle_intro(bot: Robot, message: Message):
    html_text = """
<b>Hello everyone!</b> 👋<br>
<u>This is a complete guide message</u> that includes all formatting:<br>
<b>Bold text</b><br>
<i>Spoil text</i><br>
<u>Underlined text</u><br>
<s>Strikethrough text</s><br>
<code>Inline code</code><br>
<a href="https://rubka.ir">Hyperlink to Rubka</a><br>
Emojis 😎✨🔥<br><br>
For more information, visit <a href="https://rubka.ir">Rubka website</a>.
"""
    await message.reply(html_text, parse_mode="HTML")

bot.run()
