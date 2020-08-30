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
    cmd = len(msg.text)
    if not replied:
        return
    if msg.text and cmd == 7:
        return
    _, args = msg.text.split(maxsplit=1)
    if replied and args:
        reason = f"**Reported User:** {replied.from_user.mention}\n"
        reason += f"**Reported Msg link:** {replied.link}\n"
        reason += f"**Reason:** `{args}`\n\n"
        reason += f"**Report From:** {msg.from_user.mention}"
    admins = Config.ADMINS.get(msg.chat.id)
    for i in range(len(admins)):
        try:
            await bot.send_message(
                admins[i], reason, disable_web_page_preview=True)
        except Exception:  # pylint: disable=broad-except
            pass
    await msg.reply("`Report request Accepted...`")
