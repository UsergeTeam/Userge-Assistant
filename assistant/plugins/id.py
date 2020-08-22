# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import Message, Filters

from assistant import bot, filters


@bot.on_message(Filters.command("id") & filters.auth_chats)
async def _id(_, message: Message):
    replied = message.reply_to_message
    if replied and replied.from_user:
        await message.reply(f"**USER_ID** : `{replied.from_user.id}`")
    else:
        await message.reply(f"**CHAT_ID** : `{message.chat.id}`")
