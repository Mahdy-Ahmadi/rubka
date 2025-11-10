# 📘 Rubka Bot Message Formatting Guide

This documentation provides a **complete guide** on how to format and send messages using the **Rubka Bot API** with support for both **Markdown** and **HTML** styles.  
Rubka bots can display styled text, code snippets, quotes, links, and more — similar to Telegram or Discord bots.

---

## 🚀 Getting Started

Import the `Robot` and `Message` classes from the Rubka Asynco library and create your bot instance using your token:

```python
from rubka.asynco import Robot, Message

TOKEN = "YOUR_TOKEN_HERE"
bot = Robot(TOKEN)
```

Then, define an event listener for new messages:

```python
@bot.on_message()
async def handle_message(bot: Robot, message: Message):
    ...
```

Finally, run your bot:

```python
bot.run()
```

---

## ✨ Markdown Mode

Markdown allows you to **style text** easily using special characters.  
Rubka supports a custom Markdown parser with additional features, including **quotes (`$`)** and **spoilers (`||`)**.

### 🧩 Example

```python
@bot.on_message()
async def handle_message(bot: Robot, message: Message):
    markdown_text = f"""Hi {await message.name}
$Welcome to our amazing Rubka bot demo!
Here is a [Quote example](https://rubka.ir) that spans multiple lines,
and inside it you can see:
- **Bold text**
- __Italic text__
- --Underlined text--
- `Mono text`
- ~~Strikethrough~~
- ||Spoiler content||
$
Outside the quote, you can also highlight:

- **Important parts**  
- __Emphasized words__  
- Links like [Rubka](https://rubka.ir)  

You can even show `inline code` or code blocks:

```from rubka.asynco import Robot,Message
bot = Robot("token")
@bot.on_message()
async def handle_start(bot: Robot, message: Message):
    await message.reply(f"Hello Word")
bot.run()```

Enjoy exploring all the Markdown features!
"""
    await bot.send_message(message.chat_id, markdown_text)
```

### 🧠 Markdown Features

| Feature | Syntax | Example | Output |
|----------|--------|----------|---------|
| **Bold** | `**text**` | `**Hello**` | **Hello** |
| *Italic* | `__text__` | `__Hello__` | *Hello* |
| ~~Strikethrough~~ | `~~text~~` | `~~Deleted~~` | ~~Deleted~~ |
| `Mono` | `` `code` `` | `` `var x = 1` `` | `var x = 1` |
| **Underlined** | `--text--` | `--Important--` | <u>Important</u> |
| ||Spoiler|| | `||text||` | `||Hidden||` | Spoiler block |
| [Link](url) | `[text](https://...)` | `[Rubka](https://rubka.ir)` | [Rubka](https://rubka.ir) |
| Quote | `$` before and after | `$Quote block$` | Quote block |
| Code block | ```code``` | ```print("Hello")``` | multi-line code block |

> 💡 Tip: Quotes (`$`) can span multiple lines and contain any Markdown inside them.

---

## 💎 HTML Mode

HTML formatting gives you more control and allows you to use standard HTML tags for text styling.

### 🧩 Example

```python
@bot.on_message()
async def handle_message(bot: Robot, message: Message):
    html_text = f"""<b>Hi {await message.name}</b><br><br>
Welcome to our amazing Rubka bot demo!<br>
Here you can see all HTML formatting features:<br><br>
<b>Bold text</b><br>
<i>Italic text</i><br>
<u>Underlined text</u><br>
<s>Strikethrough text</s><br>
<code>Mono text</code><br>
<pre>from rubka.asynco import Robot, Message
bot = Robot("token")
@bot.on_message()
async def handle_start(bot: Robot, message: Message):
    await message.reply(f"Hello World")
bot.run()
</pre><br>
<a href="https://rubka.ir">Link to Rubka</a><br>
<b>Important parts:</b><br>
<u>Emphasized words</u><br>
Enjoy exploring all the HTML features!
"""
    await message.reply(html_text, parse_mode="HTML")
```

### 🧠 Supported HTML Tags

| Tag | Description | Example |
|------|--------------|----------|
| `<b>` | Bold text | `<b>Hello</b>` → **Hello** |
| `<i>` | Italic text | `<i>Hello</i>` → *Hello* |
| `<u>` | Underlined | `<u>Hello</u>` → <u>Hello</u> |
| `<s>` | Strikethrough | `<s>Deleted</s>` → ~~Deleted~~ |
| `<code>` | Inline code | `<code>x = 1</code>` → `x = 1` |
| `<pre>` | Code block | `<pre>print("Hi")</pre>` |
| `<a href="">` | Hyperlink | `<a href="https://rubka.ir">Rubka</a>` |
| `<br>` | Line break | `<br>` |

> ⚠️ Always use `parse_mode="HTML"` when sending HTML-formatted messages.

---

## 🧾 Quotes in Markdown

You can create **multi-line quotes** in Markdown using the `$` symbol:

```text
$This is a
multi-line quote
that supports formatting like **bold** or [links](https://rubka.ir)$
```

Output:

> This is a  
> multi-line quote  
> that supports formatting like **bold** or [links](https://rubka.ir)

---

## 🧰 Code Blocks

For larger code examples, use triple backticks around the block:

```python
from rubka.asynco import Robot
bot = Robot("TOKEN")
@bot.on_message()
async def hello(bot, message):
    await message.reply("Hi there!")
bot.run()
```

---

## 🎨 Visual Comparison

| Format | Example Input | Example Output |
|---------|----------------|----------------|
| Markdown | `**Bold** and __Italic__` | **Bold** and *Italic* |
| HTML | `<b>Bold</b> and <i>Italic</i>` | **Bold** and *Italic* |

---

## ⚙️ Tips & Best Practices

- Use **Markdown** when you want fast and readable formatting.
- Use **HTML** for more control and complex layouts.
- Always escape or close your tags properly.
- Use `$` wisely for quotes; avoid nesting them.
- Always test your output before publishing to users.

---

## 🧑‍💻 Example Repository Structure

```
rubka-bot/
├── main.py
├── README.md
└── requirements.txt
```

---

## 🪪 License

This project is released under the **MIT License**.  
Feel free to use, modify, and distribute — just keep proper credits.

---

## 💬 Credits

Developed by **[Mehdi Ahmadi (Codern Team)](https://api-free.ir)**  
Rubka Bot Framework powered by `rubka.asynco`

```
Made with ❤️ for developers who love clean design.
```
