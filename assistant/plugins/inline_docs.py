# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import emoji
from pyrogram.types import (
    InlineQuery, InlineQueryResultArticle, InlineQueryResultPhoto,
    InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup)

from assistant import bot
from assistant.utils import docs
from assistant.utils.docs import (
    USERGE, DECORATORS, DEPLOYMENT,
    VARS, MODES, EXAMPLES, FAQS)


@bot.on_inline_query()
async def inline_docs(_, i_q: InlineQuery):
    query = i_q.query.lower()

    if query == "":
        await i_q.answer(
            results=USERGE,
            cache_time=5,
            switch_pm_text=f"{emoji.MAGNIFYING_GLASS_TILTED_RIGHT} Type to search UserGe Docs",
            switch_pm_parameter="start",
        )

        return
