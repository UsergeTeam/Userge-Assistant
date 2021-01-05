# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import Message

from assistant import bot, cus_filters


@bot.on_message(filters.command("reply") & cus_filters.auth_chats & cus_filters.auth_users)
async def _reply(_, message: Message):
    replid = message.reply_to_message
    if not replid:
        return
    _, text = message.text.html.split(maxsplit=1)
    if not text:
        return
    await message.delete()
    await replid.reply(f"{text.strip()}\n**cc** : {message.from_user.mention}")
