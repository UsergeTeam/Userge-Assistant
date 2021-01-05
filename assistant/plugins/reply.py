# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__commands__ = ["reply"]

from assistant import bot, Message


@bot.on_cmd("reply", about={
    'description': "Reply for myself (fun command)",
    'usage': "/reply [reply to message] [text]"
}, admin_only=True)
async def _reply(message: Message):
    replid = message.reply_to_message
    if not replid:
        return
    _, text = message.text.html.split(maxsplit=1)
    if not text:
        return
    await message.delete()
    await replid.reply(f"{text.strip()}\n**cc** : {message.from_user.mention}")
