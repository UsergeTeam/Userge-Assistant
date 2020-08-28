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


@bot.on_message(filters.command("json") & cus_filters.auth_chats & cus_filters.auth_users)
async def _json(_, message: Message):
    msg = str(message.reply_to_message) if message.reply_to_message else str(message)
    if len(msg) > Config.MAX_MSG_LENGTH:
        await message.reply("`too large !`")
    else:
        await message.reply(msg)
