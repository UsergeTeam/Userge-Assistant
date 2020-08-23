# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

import time

from pyrogram import Message, Filters, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions import FileIdInvalid, FileReferenceEmpty
from pyrogram.errors.exceptions.bad_request_400 import BadRequest

from assistant import bot, filters, versions
from assistant.bot import START_TIME
from assistant.utils import time_formatter

LOGO_ID, LOGO_REF = None, None


@bot.on_message(Filters.command("alive") & filters.auth_chats)
async def _alive(_, message: Message):
    
    output = f"""
**🤖 Bot Uptime** : `{time_formatter(time.time() - START_TIME)}`
**🤖 Bot Version** : `{versions.__assistant_version__}`
    **__python__** : `{versions.__python_version__}`
    **__pyrogram__** : `{versions.__pyro_version__}` """
    try:
        if LOGO_ID:
            await sendit(message, LOGO_ID, LOGO_REF, output)
        else:
            await refresh_id()
            await sendit(message, LOGO_ID, LOGO_REF, output)
    except (FileIdInvalid, FileReferenceEmpty, BadRequest):
        await refresh_id()
        await sendit(message, LOGO_ID, LOGO_REF, output)


async def refresh_id():
    global LOGO_ID, LOGO_REF
    gif = (await bot.get_messages('UserGeOt', 492405)).animation
    LOGO_ID = gif.file_id
    LOGO_REF = gif.file_ref


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
