from rubka import rubino

bot = rubino("your_auth")  # از rubika.ir بگیر
post = "path_or_url.jpg"
text = "کپشن پست"

try:
    data = bot.add_post(
        post_file=post,
        caption=text,
        time=1,
        size=[668, 798]
    )
    print("✅ ارسال شد!")
    print(data)
except:
    print("❌ خطا")
