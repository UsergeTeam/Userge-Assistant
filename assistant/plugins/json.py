# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__commands__ = ["json"]

from assistant import bot, Config, Message


@bot.on_cmd("json", about={
    'description': "Check json of message",
    'usage': "/json\n/json [reply to message]"
}, admin_only=True)
async def _json(message: Message):
    msg = str(message.reply_to_message) if message.reply_to_message else str(message)
    if len(msg) > Config.MAX_MSG_LENGTH:
        await message.reply("`too large !`")
    else:
        await message.reply(msg)
