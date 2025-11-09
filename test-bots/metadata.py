from rubka.asynco import Robot, Message

bot = Robot("TOKEN")

@bot.on_message()
async def handle_metadata_message(bot: Robot, message: Message):
    info = []
    if message.has_metadata:
        info.append("📦 This message contains metadata ✅")
        info.append(f"🧱 meta_types: {', '.join(message.meta_types) if message.meta_types else 'None'}")
        if message.is_bold: info.append("📝 Contains bold text")
        if message.is_italic: info.append("🖋️ Contains italic text")
        if message.is_strike: info.append("❌ Contains strikethrough text")
        if message.is_underline: info.append("🔠 Contains underline")
        if message.is_quote: info.append("💬 Contains quote")
        if message.is_spoiler: info.append("🙈 Contains spoiler")
        if message.is_pre: info.append("💻 Contains code block (Pre)")
        if message.is_mono: info.append("⌨️ Contains monospace font (Mono)")
        if message.is_link_meta: info.append("🔗 Contains a link in metadata")
        if message.meta_links:info.append(f"🌐 Links: {', '.join(message.meta_links)}")
        if message.has_link:info.append("🧩 The message or metadata contains a link")
        if message.is_formatted:info.append("🎨 The message is formatted")
    else:info.append("ℹ️ This message has no metadata.")

    await message.reply("\n".join(info))

bot.run(sleep_time=0)
