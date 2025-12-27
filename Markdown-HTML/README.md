# 📘 rubka – Markdown & HTML Usage Guide

این داکیومنت برای استفاده از سیستم پارس مارک‌داون و HTML شما نوشته شده و برای **کپی مستقیم** یا **دانلود** آماده است.

---

## ⚙️ راه‌اندازی پایه ربات

### حالت Markdown (پیش‌فرض)

```python
from rubka.asynco import Robot, Message

bot = Robot("token")

@bot.on_message()
async def start(bot: Robot, message: Message):
    await message.reply("**hi bold**")

bot.run()
```

---

### حالت HTML

```python
from rubka.asynco import Robot, Message

bot = Robot("token", parse_mode="HTML")

@bot.on_message()
async def start(bot: Robot, message: Message):
    await message.reply("<b>Bold text</b>")

bot.run()
```
---

### حالت ورودی در متود

```python
from rubka.asynco import Robot, Message

bot = Robot("token")

@bot.on_message()
async def start(bot: Robot, message: Message):
    await message.reply("<b>Bold text</b>",parse_mode='HTML')

bot.run()
```

---

## ✨ مثال‌های پشتیبانی‌شده (ساده و قابل کپی)

---

### 🔹 Bold

Markdown:
```python
await message.reply("**Bold Text**")
```

HTML:
```python
await message.reply("<b>Bold Text</b>")
```

---

### 🔹 Italic

Markdown:
```python
await message.reply("__Italic Text__")
```

HTML:
```python
await message.reply("<i>Italic Text</i>")
```

---

### 🔹 Underline

Markdown:
```python
await message.reply("--Underline Text--")
```

HTML:
```python
await message.reply("<u>Underline Text</u>")
```

---

### 🔹 Strike

Markdown:
```python
await message.reply("~~Strike Text~~")
```

HTML:
```python
await message.reply("<s>Strike Text</s>")
```

---

### 🔹 Mono / Code

Markdown:
```python
await message.reply("`print('hello')`")
```

HTML:
```python
await message.reply("<code>print('hello')</code>")
```

---

### 🔹 Code Block

Markdown:
````python
await message.reply("""
```
print("Hello World")
```
""")
````

HTML:
```python
await message.reply("<pre>print('Hello World')</pre>")
```

---

### 🔹 Spoiler

Markdown:
```python
await message.reply("||Spoiler Text||")
```

HTML:
```python
await message.reply('<span class="spoiler">Spoiler Text</span>')
```

---

### 🔹 Quote (تک خط)

Markdown:
```python
await message.reply("> This is quote")
```

---

### 🔹 Quote (چند خط)

Markdown:
```python
await message.reply("""
> Line one
> Line two
""")
```

---

### 🔹 Link

Markdown:
```python
await message.reply("[Google](https://google.com)")
```

HTML:
```python
await message.reply('<a href="https://google.com">Google</a>')
```

---

### 🔹 Mention (user_id)

Markdown:
```python
await message.reply("[Me](u0123456789)")
```
