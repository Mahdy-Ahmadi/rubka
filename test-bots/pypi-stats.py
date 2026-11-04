import asyncio
import re
import hashlib
from datetime import datetime, timezone
from urllib.parse import quote

import requests

from rubka import Robot, Message, ChatKeypadBuilder

BOT_TOKEN = "Token"
PYPISTATS_URL = "https://pypistats.org/api/packages/{}/recent"
PYPI_JSON_URL = "https://pypi.org/pypi/{}/json"
HTTP_HEADERS = {
    "User-Agent": "Rubka-PyPI-Package-Analyzer/2.0"
}
HTTP_TIMEOUT = 20

bot = Robot(token=BOT_TOKEN, show_progress=True)
user_states = {}

BTN_STATS = "📊 بررسی کتابخانه"
BTN_HELP = "❓ راهنما"
BTN_BACK = "↩️ بازگشت"
def main_keyboard():
    k = ChatKeypadBuilder()
    k.row(k.button_simple(id=BTN_STATS, text=BTN_STATS))
    k.row(k.button_simple(id=BTN_HELP, text=BTN_HELP))
    return k.build(resize_keyboard=True)


def back_keyboard():
    k = ChatKeypadBuilder()
    k.row(k.button(id=BTN_BACK, text=BTN_BACK))
    return k.build(resize_keyboard=True, on_time_keyboard=True)


def get_package_stats(package_name):
    try:
        url = PYPISTATS_URL.format(quote(package_name, safe=""))
        response = requests.get(
            url,
            headers=HTTP_HEADERS,
            timeout=HTTP_TIMEOUT,
        )

        if response.status_code == 404:
            return None, "not_found"

        response.raise_for_status()
        payload = response.json()

        if payload.get("type") != "recent_downloads":
            return None, "invalid_response"

        data = payload.get("data")
        if not isinstance(data, dict):
            return None, "invalid_response"

        return data, None

    except requests.exceptions.Timeout:
        return None, "timeout"
    except requests.exceptions.RequestException as exc:
        print(f"PyPIStats request error: {exc}")
        return None, "connection_error"
    except (ValueError, TypeError) as exc:
        print(f"PyPIStats response error: {exc}")
        return None, "invalid_response"
    except Exception as exc:
        print(f"PyPIStats unknown error: {exc}")
        return None, "unknown_error"

def parse_upload_time(file_info):
    value = (
        file_info.get("upload_time_iso_8601")
        or file_info.get("upload_time")
    )

    if not value:
        return None

    try:
        normalized = value.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except (TypeError, ValueError):
        return None


def format_datetime(value):
    if not value:
        return "نامشخص"
    return value.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def get_gravatar_url(email):
    if not email or "@" not in str(email):
        return None

    normalized_email = str(email).strip().lower()
    email_hash = hashlib.md5(normalized_email.encode("utf-8")).hexdigest()
    avatar_url = f"https://www.gravatar.com/avatar/{email_hash}?s=400&d=404"

    try:
        response = requests.get(
            avatar_url,
            headers=HTTP_HEADERS,
            timeout=10,
            stream=True,
            allow_redirects=True,
        )
        content_type = response.headers.get("Content-Type", "").lower()
        is_image = response.status_code == 200 and content_type.startswith("image/")
        response.close()
        return avatar_url if is_image else None
    except requests.exceptions.RequestException:
        return None

def get_package_info(package_name):
    try:
        url = PYPI_JSON_URL.format(quote(package_name, safe=""))
        response = requests.get(
            url,
            headers=HTTP_HEADERS,
            timeout=HTTP_TIMEOUT,
        )

        if response.status_code == 404:return None, "not_found"
        response.raise_for_status()
        payload = response.json()
        info = payload.get("info") or {}
        releases = payload.get("releases") or {}
        if not isinstance(releases, dict):
            releases = {}
        latest_version = info.get("version") or "نامشخص"
        latest_files = releases.get(latest_version) or []
        all_upload_times = []
        total_release_files = 0
        published_versions = 0
        for version_files in releases.values():
            if not isinstance(version_files, list):
                continue
            if version_files:
                published_versions += 1
            total_release_files += len(version_files)
            for file_info in version_files:
                if not isinstance(file_info, dict):
                    continue
                uploaded_at = parse_upload_time(file_info)
                if uploaded_at:
                    all_upload_times.append(uploaded_at)
        latest_upload_times = []
        latest_file_types = set()
        for file_info in latest_files:
            if not isinstance(file_info, dict):
                continue
            uploaded_at = parse_upload_time(file_info)
            if uploaded_at:
                latest_upload_times.append(uploaded_at)
            file_type = file_info.get("packagetype")
            if file_type:
                latest_file_types.add(file_type)
        latest_version_date = min(latest_upload_times) if latest_upload_times else None
        first_release_date = min(all_upload_times) if all_upload_times else None
        last_release_date = max(all_upload_times) if all_upload_times else None
        project_urls = info.get("project_urls") or {}
        if not isinstance(project_urls, dict):project_urls = {}
        def first_url(*names):
            for name in names:
                value = project_urls.get(name)
                if value:
                    return str(value)
            return ""
        home_page = (
            first_url("Homepage", "Home", "Homepage URL")
            or info.get("home_page")
            or ""
        )
        source_url = first_url(
            "Source", "Source Code", "Repository", "Code", "GitHub"
        )
        documentation_url = first_url(
            "Documentation", "Docs", "Documentation URL"
        ) or info.get("docs_url") or ""
        bug_tracker_url = first_url(
            "Issues", "Issue Tracker", "Bug Tracker"
        ) or info.get("bugtrack_url") or ""

        classifiers = info.get("classifiers") or []
        python_versions = []
        for classifier in classifiers:
            prefix = "Programming Language :: Python :: "
            if classifier.startswith(prefix):
                version_label = classifier[len(prefix):]
                if version_label and version_label.lower() not in {
                    "implementation", "pypy", "jython", "ironpython", "cpython"
                }:
                    python_versions.append(version_label)

        python_versions = sorted(set(python_versions))
        requires_dist = info.get("requires_dist") or []
        if not isinstance(requires_dist, list):
            requires_dist = []
        license_value = info.get("license") or ""
        if not license_value:
            for classifier in classifiers:
                if classifier.startswith("License ::"):
                    license_value = classifier.split("::")[-1].strip()
                    break
        if not license_value:
            license_value = "نامشخص"
        author = info.get("author") or "نامشخص"
        maintainer = info.get("maintainer") or "نامشخص"
        avatar_url = None
        for avatar_email in (
            info.get("author_email"),
            info.get("maintainer_email"),
        ):
            avatar_url = get_gravatar_url(avatar_email)
            if avatar_url:
                break

        return {
            "name": info.get("name") or package_name,
            "author": author,
            "maintainer": maintainer,
            "author_email": info.get("author_email") or "",
            "maintainer_email": info.get("maintainer_email") or "",
            "avatar_url": avatar_url,
            "version": latest_version,
            "release_date": latest_version_date,
            "first_release_date": first_release_date,
            "last_release_date": last_release_date,
            "versions_count": published_versions,
            "release_files_count": total_release_files,
            "latest_files_count": len(latest_files),
            "latest_file_types": sorted(latest_file_types),
            "license": license_value,
            "requires_python": info.get("requires_python") or "نامشخص",
            "dependencies_count": len(requires_dist),
            "dependencies": requires_dist,
            "python_versions": python_versions,
            "homepage": home_page,
            "source": source_url,
            "documentation": documentation_url,
            "issues": bug_tracker_url,
            "package_url": info.get("package_url") or f"https://pypi.org/project/{quote(package_name, safe='')}/",
            "yanked_latest": any(
                bool(item.get("yanked"))
                for item in latest_files
                if isinstance(item, dict)
            ),
        }, None
    except requests.exceptions.Timeout:
        return None, "timeout"
    except requests.exceptions.RequestException as exc:
        print(f"PyPI JSON request error: {exc}")
        return None, "connection_error"
    except (ValueError, TypeError, AttributeError) as exc:
        print(f"PyPI JSON response error: {exc}")
        return None, "invalid_response"
    except Exception as exc:
        print(f"PyPI JSON unknown error: {exc}")
        return None, "unknown_error"

def format_number(value):
    try:return f"{int(value):,}"
    except (ValueError, TypeError):return "نامشخص"

def clean_text(value, limit=180):
    value = str(value or "نامشخص")
    value = " ".join(value.split())
    value = value.replace("`", "'")
    if len(value) > limit:value = value[: limit - 1] + "…"
    return value

def format_list(values, limit=8):
    if not values:
        return "نامشخص"
    selected = [clean_text(item, 45) for item in values[:limit]]
    result = "، ".join(selected)
    if len(values) > limit:
        result += f" و {len(values) - limit} مورد دیگر"
    return result

def format_url(value):
    value = clean_text(value, 220)
    return value if value != "نامشخص" else "ثبت نشده"

def make_report(package_name, stats, info):
    if stats:
        day = format_number(stats.get("last_day"))
        week = format_number(stats.get("last_week"))
        month = format_number(stats.get("last_month"))
    else:day = week = month = "در دسترس نیست"
    if info:
        python_versions = format_list(info["python_versions"])
        file_types = format_list(info["latest_file_types"])
        latest_yanked = "بله ⚠️" if info["yanked_latest"] else "خیر"
        lines = [
            "📦 گزارش کامل کتابخانه پایتون",
            "━━━━━━━━━━━━━━━━━━━━",
            f"🔹 نام: `{clean_text(info['name'], 100)}`",
            f"👨‍💻 سازنده: `{clean_text(info['author'])}`",
            f"🛠 نگهدارنده: `{clean_text(info['maintainer'])}`",
            "",
            "🚀 اطلاعات نسخه و انتشار",
            f"• آخرین نسخه: `{clean_text(info['version'], 80)}`",
            f"• تاریخ انتشار نسخه فعلی: `{format_datetime(info['release_date'])}`",
            f"• اولین انتشار ثبت‌شده: `{format_datetime(info['first_release_date'])}`",
            f"• آخرین انتشار ثبت‌شده: `{format_datetime(info['last_release_date'])}`",
            f"• تعداد نسخه‌های منتشرشده: `{format_number(info['versions_count'])}`",
            f"• تعداد کل فایل‌های انتشار: `{format_number(info['release_files_count'])}`",
            f"• فایل‌های نسخه فعلی: `{format_number(info['latest_files_count'])}`",
            f"• نوع فایل‌های نسخه فعلی: `{file_types}`",
            f"• نسخه فعلی حذف‌شده (Yanked): `{latest_yanked}`",
            "",
            "📥 آمار دانلود (بدون آینه‌های شناخته‌شده)",
            f"• ۲۴ ساعت اخیر: `{day}`",
            f"• ۷ روز اخیر: `{week}`",
            f"• ۳۰ روز اخیر: `{month}`",
            "",
            "⚙️ مشخصات فنی",
            f"• لایسنس: `{clean_text(info['license'])}`",
            f"• نیازمندی Python: `{clean_text(info['requires_python'])}`",
            f"• نسخه‌های Python: `{python_versions}`",
            f"• تعداد وابستگی‌های اعلام‌شده: `{format_number(info['dependencies_count'])}`",
            "",
            "🔗 لینک‌ها",
            f"• صفحه PyPI: {format_url(info['package_url'])}",
            f"• وب‌سایت: {format_url(info['homepage'])}",
            f"• مخزن کد: {format_url(info['source'])}",
            f"• مستندات: {format_url(info['documentation'])}",
            f"• گزارش مشکلات: {format_url(info['issues'])}",
            "━━━━━━━━━━━━━━━━━━━━",
            "📊 منابع: PyPIStats و PyPI JSON API",
        ]
    else:
        lines = [
            "📊 آمار دانلود کتابخانه پایتون",
            "━━━━━━━━━━━━━━━━━━━━",
            f"📦 نام: `{clean_text(package_name, 100)}`",
            f"• ۲۴ ساعت اخیر: `{day}`",
            f"• ۷ روز اخیر: `{week}`",
            f"• ۳۰ روز اخیر: `{month}`",
            "",
            "⚠️ دریافت اطلاعات تکمیلی از PyPI ناموفق بود.",
        ]

    return "\n".join(lines)

async def show_package_stats(msg, package_name):
    package_name = package_name.strip().lower()

    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,199}", package_name):
        await msg.reply(
            "❌ نام کتابخانه معتبر نیست.\n"
            "لطفاً نام صحیح پکیج PyPI را ارسال کنید."
        )
        return

    wait_msg = await msg.reply(
        f"⏳ در حال جمع‌آوری اطلاعات و آمار `{package_name}`..."
    )
    stats_result, info_result = await asyncio.gather(
        asyncio.to_thread(get_package_stats, package_name),
        asyncio.to_thread(get_package_info, package_name),
    )
    stats, stats_error = stats_result
    package_info, info_error = info_result
    if stats is None and package_info is None:
        errors = {
            "not_found": "❌ این کتابخانه در PyPI پیدا نشد.",
            "timeout": "⏱ زمان پاسخ‌گویی سرور تمام شد. کمی بعد دوباره تلاش کنید.",
            "connection_error": "❌ اتصال به سرورهای دریافت اطلاعات برقرار نشد.",
            "invalid_response": "❌ پاسخ دریافتی از API معتبر نیست.",
            "unknown_error": "❌ خطای ناشناخته‌ای رخ داد.",
        }
        error_code = info_error or stats_error
        error_text = errors.get(error_code, "❌ دریافت اطلاعات ناموفق بود.")
        await bot.edit_message_text(
            msg.chat_id,
            wait_msg.message_id,
            error_text,
        )
        return
    report = make_report(package_name, stats, package_info)
    image_sent = False
    if package_info and package_info.get("avatar_url"):
        try:
            await msg.reply_image(
                path=package_info["avatar_url"],
                text=report,
            )
            image_sent = True
        except Exception as exc:
            print(f"Avatar send error: {exc}")

    if image_sent:
        await bot.edit_message_text(
            msg.chat_id,
            wait_msg.message_id,
            "گزارش کتابخانه ارسال شد.",
        )
    else:
        await bot.edit_message_text(
            msg.chat_id,
            wait_msg.message_id,
            report,
        )

@bot.on_message()
async def message_handler(bot: Robot, msg: Message):
    chat_id = msg.chat_id
    text = msg.text.strip() if msg.text else ""

    callback_data = (
        msg.aux_data.button_id
        if msg.aux_data else None
    )

    state = user_states.get(chat_id)
    if callback_data:
        if callback_data == BTN_BACK:
            user_states.pop(chat_id, None)
            await msg.reply(
                "🏠 به منوی اصلی برگشتید.",
                chat_keypad=main_keyboard(),
            )
            return

        if callback_data == BTN_STATS:
            user_states[chat_id] = "awaiting_package"
            await msg.reply(
                "📦 لطفاً نام کتابخانه پایتون مورد نظر خود را ارسال کنید.\n\n"
                "مثال:\n"
                "`flask`\n"
                "`requests`\n"
                "`django`",
                chat_keypad=back_keyboard(),
            )
            return
        if callback_data == BTN_HELP:
            await msg.reply(
                "❓ راهنمای ربات\n\n"
                "۱. روی دکمه بررسی کتابخانه بزنید.\n"
                "۲. نام پکیج موردنظر در PyPI را ارسال کنید.\n"
                "۳. گزارش دانلودها، نسخه‌ها، انتشارها و مشخصات فنی را دریافت کنید.\n\n"
                "منابع اطلاعات: PyPI و PyPIStats",
                chat_keypad=main_keyboard(),
            )
            return
    if text == "/start":
        user_states.pop(chat_id, None)
        await msg.reply(
            "سلام! 👋\n\n"
            "به ربات تحلیل و آمار کتابخانه‌های پایتون خوش آمدید.\n\n"
            "با این ربات می‌توانید اطلاعات انتشار و آمار دانلود پکیج‌های PyPI را مشاهده کنید.\n\n"
            "برای شروع از دکمه زیر استفاده کنید.",
            chat_keypad=main_keyboard(),
        )
        return

    if text == "/cancel":
        user_states.pop(chat_id, None)
        await msg.reply(
            "عملیات لغو شد.",
            chat_keypad=main_keyboard(),
        )
        return
    if state == "awaiting_package" and text:
        user_states.pop(chat_id, None)
        await show_package_stats(msg, text)
        await msg.reply(
            "برای بررسی کتابخانه دیگری، نام آن را دوباره از منو ارسال کنید.",
            chat_keypad=main_keyboard(),
        )
        return

async def main():
    await bot.run()
if __name__ == "__main__":
    try:asyncio.run(main())
    except KeyboardInterrupt:print("Bot Stopped!")
