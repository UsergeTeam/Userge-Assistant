# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from assistant import bot, Message, filters
from assistant.utils.docs import HELP


@bot.on_filters(filters.private)
async def _start_(msg: Message):
    await msg.reply(
        HELP,
        disable_web_page_preview=True,
        parse_mode="markdown",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "🗂 Source Code",
                url="https://github.com/UserGeTeam/UserGe-Assistant"
            ),
            InlineKeyboardButton(
                "😎 Use Inline!",
                switch_inline_query=""
            )
        ]])
    )
