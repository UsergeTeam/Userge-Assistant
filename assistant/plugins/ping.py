# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__commands__ = ["ping"]

from datetime import datetime

from assistant import bot, Message


@bot.on_cmd("ping", about="Check how long it takes to ping.")
async def _ping(message: Message):
    start = datetime.now()
    replied = await message.reply('`Pong!`')
    end = datetime.now()
    m_s = (end - start).microseconds / 1000
    await replied.edit(f"**Pong!**\n`{m_s} ms`")
