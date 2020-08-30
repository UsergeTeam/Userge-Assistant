# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import Message

from assistant import bot, cus_filters, Config


@bot.on_message(filters.command("report") & cus_filters.auth_chats)
async def _report(_, msg: Message):
    replied = msg.reply_to_message
    if not replied:
        return
    if len(msg.text) < 9:
        return
    _, args = msg.text.split(maxsplit=1)
    if not args:
        return
    reason = f"**Reported User:** {replied.from_user.mention}\n"
    reason += f"**Reported Msg link:** {replied.link}\n"
    reason += f"**Reason:** `{args}`\n\n"
    reason += f"**Report From:** {msg.from_user.mention}"
    for admin_id in Config.ADMINS.get(msg.chat.id):
        try:
            await bot.send_message(admin_id, reason, disable_web_page_preview=True)
        except Exception:  # pylint: disable=broad-except
            pass
    await msg.reply("`Report request Accepted ...`")
