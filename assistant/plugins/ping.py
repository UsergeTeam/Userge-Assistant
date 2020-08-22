# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
from datetime import datetime

from pyrogram import Message, Filters

from assistant import bot, Config


@bot.on_message(Config.AUTH_CHATS & Filters.command("ping"))
async def _ping(_, message: Message):
    start = datetime.now()
    replied = await message.reply('`Pong!`')
    end = datetime.now()
    m_s = (end - start).microseconds / 1000
    await replied.edit(f"**Pong!**\n`{m_s} ms`")
    await asyncio.sleep(5)
    await replied.delete()
