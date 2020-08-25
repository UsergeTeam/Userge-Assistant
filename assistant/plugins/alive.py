# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

import time
import random

from pyrogram import Message, Filters, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions import FileIdInvalid, FileReferenceEmpty
from pyrogram.errors.exceptions.bad_request_400 import BadRequest

from assistant import bot, filters, versions
from assistant.bot import START_TIME
from assistant.utils import time_formatter


@bot.on_message(Filters.command("alive") & filters.auth_chats)
async def _alive(_, message: Message):

    output = f"""
**🤖 Bot Uptime** : `{time_formatter(time.time() - START_TIME)}`
**🤖 Bot Version** : `{versions.__assistant_version__}`
**️️⭐ Python** : `{versions.__python_version__}`
**💥 Pyrogram** : `{versions.__pyro_version__}` """
    msg_id = random.choice(
        499509, 499428, 496502, 496360, 496498)  # Too many GiF 😂
    gif = (await bot.get_messages('UserGeOt', msg_id)).animation
    file_id = gif.file_id
    file_ref = gif.file_ref
    await sendit(message, file_id, file_ref, output)



async def sendit(message, fileid, fileref, caption):
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
    await bot.send_animation(
        chat_id=message.chat.id,
        animation=fileid, file_ref=fileref,
        caption=caption, reply_markup=button)
