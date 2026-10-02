from rubka import Robot
from rubka.enums import EventTypeEnum, EventJoinTypeEnum, EnumChatAccess
from rubka.event import Event

bot = Robot(
    token="BGBHCC0....."
)


@bot.on_event(event_type=EventTypeEnum.BotJoined)
async def on_bot_joined(bot: Robot, event: Event):
    print(f"Bot joined chat: {event.chat_id}")
    print(f"Join type: {event.join_type}")

    if not event.has_access(EnumChatAccess.SendMessages):
        print(f"No send permission in {event.chat_id}")
        return

    if event.join_type == EventJoinTypeEnum.Admin:
        await bot.send_message(
            chat_id=event.chat_id,
            text="Bot added as admin.",
        )
    else:
        await bot.send_message(
            chat_id=event.chat_id,
            text="Bot added as member.",
        )


@bot.on_event(event_type=EventTypeEnum.BotRemoved)
async def on_bot_removed(bot: Robot, event: Event):
    print(f"Bot removed from chat: {event.chat_id}")
    with open("removed_chats.log", "a", encoding="utf-8") as f:
        f.write(f"{event.chat_id}\n")


@bot.on_event(event_type=EventTypeEnum.BotPermissionsChanged)
async def on_permissions_changed(bot: Robot, event: Event):
    print(f"Permissions changed in: {event.chat_id}")

    access_names = {
        EnumChatAccess.SendMessages: "SendMessages",
        EnumChatAccess.EditMyMessages: "EditMyMessages",
        EnumChatAccess.EditAllMessages: "EditAllMessages",
        EnumChatAccess.DeleteGlobalAllMessages: "DeleteGlobalAllMessages",
        EnumChatAccess.ViewMembers: "ViewMembers",
        EnumChatAccess.BanMember: "BanMember",
    }

    report_lines = ["New permissions:"]

    if event.access_list:
        for access in event.access_list:
            name = access_names.get(access, str(access))
            report_lines.append(f"- {name}")
    else:
        report_lines.append("- None")

    report = "\n".join(report_lines)
    print(report)

    if not event.has_access(EnumChatAccess.SendMessages):
        print(f"No send permission in {event.chat_id}")
        return

    await bot.send_message(
        chat_id=event.chat_id,
        text=report,
    )


@bot.on_event(
    event_type=[
        EventTypeEnum.BotJoined,
        EventTypeEnum.BotRemoved,
    ]
)
async def log_membership_changes(bot: Robot, event: Event):
    with open("membership_events.log", "a", encoding="utf-8") as f:
        f.write(
            f"[{event.chat_id}] type={event.type} join_type={event.join_type}\n"
        )
    print(f"Membership event logged: {event.type}")


def only_admin_join(event: Event) -> bool:
    return event.join_type == EventJoinTypeEnum.Admin


@bot.on_event(
    event_type=EventTypeEnum.BotJoined,
    filters=only_admin_join,
)
async def on_admin_join(bot: Robot, event: Event):
    print(f"Bot joined as admin in: {event.chat_id}")

    if not event.has_access(EnumChatAccess.SendMessages):
        print(f"No send permission in {event.chat_id}")
        return

    await bot.send_message(
        chat_id=event.chat_id,
        text="Bot added as admin.",
    )


IMPORTANT_GROUPS = [
    "b0d7f8a9-1c2d-3e4f-5a6b-7c8d9e0f1a2b",
    "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
]


@bot.on_event(
    event_type=EventTypeEnum.BotJoined,
    chat_id=IMPORTANT_GROUPS,
)
async def on_join_important_groups(bot: Robot, event: Event):
    print(f"Bot joined important group: {event.chat_id}")

    ADMIN_CHAT_ID = "YOUR_ADMIN_CHAT_ID_HERE"
    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"Bot joined important group: {event.chat_id}",
    )


@bot.on_event()
async def debug_all_events(bot: Robot, event: Event):
    print("=" * 60)
    print("Event received:")
    print(f"  type       : {event.type}")
    print(f"  join_type  : {event.join_type}")
    print(f"  chat_id    : {event.chat_id}")
    print(f"  access_list: {event.access_list}")
    print(f"  raw_data   : {event.raw_data}")
    print("=" * 60)


bot.run()
