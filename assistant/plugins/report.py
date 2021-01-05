# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__commands__ = ["report"]

from assistant import bot, Config, Message
from assistant.utils import is_self, is_admin, is_dev


@bot.on_cmd("report", about={
    'description': "Report to admins",
    'usage': "/report [reply to message] [reason]"})
async def _report(msg: Message):
    replied = msg.reply_to_message
    if not replied:
        return
    f_u_id = replied.from_user.id
    if await is_self(f_u_id) or is_dev(f_u_id) or is_admin(msg.chat.id, f_u_id):
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
    sent = await msg.reply("`Reporting ...`")
    for admin_id in Config.ADMINS.get(msg.chat.id):
        try:
            await bot.send_message(admin_id, reason, disable_web_page_preview=True)
        except Exception:  # pylint: disable=broad-except
            pass
    await sent.edit("`Reported to all Admins !`")
