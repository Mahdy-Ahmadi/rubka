from rubka.asynco import Robot,Message,filters
from rubka import rubino as ClientRubino

username_page = "mahdy_ahmadi" #یوزرنیم پیج فالو اجباری
rubino = ClientRubino("auth") #یه اوت روبینو ریجستر شده از m.rubika.ir
bot = Robot("token") #توکن ربات


target_profile_id=rubino.search_Page(username_page)['profiles'][0]['id']
def check_Follow(username):
    followers = rubino.get_Page_Follower(target_profile_id=target_profile_id,limit=200).get('profiles', [])
    return any(profile.get('username') == username for profile in followers)

@bot.on_message(filters.is_private)
async def handle_start(_: Robot, message: Message):
    username = await message.username
    if username == "None":await message.reply(f"شما دارای پیج روبینو نمیباشید")
    send = await message.reply(f"منتظر بمانید...")
    has_followed = check_Follow(username)
    if has_followed:
        reply_text = "✅ فالو تأیید شد.\nاز حضور شما خوشحالیم! 🌟"
    else:
        reply_text = (
            f"⚠️ کاربر گرامی، لطفاً ابتدا صفحه‌ی شما: https://rubika.ir/{username}\n\n"
            f"و صفحه‌ی روبینو ما: https://rubika.ir/page/{username_page} را فالو نمایید.\n"
            "پس از انجام این کار، دوباره تلاش کنید. 🙏"
        )
    await send.edit(reply_text)
bot.run()
