# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__commands__ = ["alive"]

import time
import random

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FileIdInvalid, FileReferenceEmpty, BadRequest

from assistant import bot, Message, versions, START_TIME
from assistant.utils import time_formatter

LOGO_DATA = []
MSG_IDS = [499509, 499428, 496502, 496360, 496498]


@bot.on_cmd("alive", about={
    'description': "Check bot alive or not, Uptime and Versions.",
    'usage': "/alive"})
async def _alive(message: Message):
    try:
        await _sendit(message.chat.id)
    except (FileIdInvalid, FileReferenceEmpty, BadRequest):
        await _refresh_data()
        await _sendit(message.chat.id)


async def _refresh_data():
    LOGO_DATA.clear()
    for msg in await bot.get_messages('UserGeOt', MSG_IDS):
        if not msg.animation:
            continue
        gif = msg.animation
        LOGO_DATA.append(gif.file_id)


async def _sendit(chat_id):
    if not LOGO_DATA:
        await _refresh_data()
    caption = f"""
**🤖 Bot Uptime** : `{time_formatter(time.time() - START_TIME)}`
**🤖 Bot Version** : `{versions.__assistant_version__}`
**️️⭐ Python** : `{versions.__python_version__}`
**💥 Pyrogram** : `{versions.__pyro_version__}` """
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="License",
                    url=("https://github.com/"
                         "UsergeTeam/Userge-Assistant/blob/master/LICENSE")),
                InlineKeyboardButton(
                    text="Repo",
                    url="https://github.com/UsergeTeam/Userge-Assistant")
            ]
        ]
    )
    file_id = random.choice(LOGO_DATA)
    await bot.send_animation(chat_id=chat_id,
                             animation=file_id,
                             caption=caption,
                             reply_markup=button)
