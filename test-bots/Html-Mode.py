from rubka.asynco import Robot, Message

TOKEN = ""
bot = Robot(TOKEN)

@bot.on_message()
async def handle_message(bot: Robot, message: Message):
    html_text = f"""<b>Hi {await message.name} 👋</b><br><br>
Welcome to our amazing Rubka bot demo! 🎉<br>
Here you can see all HTML formatting features:<br><br>
<b>Bold text</b><br>
<i>Italic text</i><br>
<u>Underlined text</u><br>
<s>Strikethrough text</s><br>
<code>Mono text</code><br>
<code>Inline code example</code><br>
<pre>from rubka.asynco import Robot, Message
bot = Robot("token")
@bot.on_message()
async def handle_start(bot: Robot, message: Message):
    await message.reply(f"Hello World")
bot.run()
</pre><br>
<a href="https://rubka.ir">Link to Rubka</a><br>
Emojis 😎✨🔥<br><br>
<b>Important parts:</b><br>
<u>Emphasized words</u><br>
Enjoy exploring all the HTML features! 🎉
"""
    await message.reply(html_text, parse_mode="HTML")

bot.run()
