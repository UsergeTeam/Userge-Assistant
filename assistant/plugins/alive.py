# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

import time

from pyrogram import Message, Filters
from pyrogram.errors.exceptions import FileIdInvalid, FileReferenceEmpty
from pyrogram.errors.exceptions.bad_request_400 import BadRequest

from assistant import bot, filters, versions
from assistant.bot import START_TIME
from assistant.utils import time_formatter

LOGO_STICKER_ID, LOGO_STICKER_REF = None, None


@bot.on_message(Filters.command("alive") & filters.auth_chats)
async def _alive(_, message: Message):
    try:
        if LOGO_STICKER_ID:
            await sendit(LOGO_STICKER_ID, LOGO_STICKER_REF, message)
        else:
            await refresh_id()
            await sendit(LOGO_STICKER_ID, LOGO_STICKER_REF, message)
    except (FileIdInvalid, FileReferenceEmpty, BadRequest):
        await refresh_id()
        await sendit(LOGO_STICKER_ID, LOGO_STICKER_REF, message)
    output = f"""**Userge-Assistant is Up**

• **uptime** : `{time_formatter(time.time() - START_TIME)}`
• **python version** : `{versions.__python_version__}`
• **pyrogram version** : `{versions.__pyro_version__}`
• **bot version** : `{versions.__assistant_version__}`
• **license** : {versions.__license__}
• **copyright** : {versions.__copyright__}
• **repo** : [Userge-Assistant](https://github.com/UsergeTeam/Userge-Assistant)
"""
    await bot.send_message(message.chat.id, output, disable_web_page_preview=True)


async def refresh_id():
    global LOGO_STICKER_ID, LOGO_STICKER_REF
    sticker = (await bot.get_messages('UsergeOt', 488248)).sticker
    LOGO_STICKER_ID = sticker.file_id
    LOGO_STICKER_REF = sticker.file_ref


async def sendit(fileid, fileref, message: Message):
    await bot.send_sticker(message.chat.id, fileid, file_ref=fileref)
