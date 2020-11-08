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


@bot.on_inline_query()
async def inline_docs(_, i_q: InlineQuery):
    query = i_q.query.lower()

    if query == "":
        await i_q.answer(
            results=docs.USERGE,
            cache_time=5,
            switch_pm_text="🔍 Type to search UserGe Docs",
            switch_pm_parameter="start",
        )

        return
    results = []
    if query == "decorators":
        results.append(
            InlineQueryResultArticle(
                title="Decorators",
                description="UserGe Decorators online documentation page",
                input_message_content=InputTextMessageContent(
                    f"{docs.intro}"
                    f"`Online Documentation Page for UserGe Decorators.`"
                ),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "📚 Online docs",
                        url=docs.decorators
                    )
                ]]),
                thumb_url=docs.USERGE_THUMB,
            )
        )

        for i in docs.DECORATORS:
            results.append(
                InlineQueryResultArticle(
                    title=i[0],
                    description=i[1],
                    input_message_content=InputTextMessageContent(
                        docs.intro + i[2]
                    ),
                    thumb_url=docs.DECORATORS_THUMB
                )
            )
    elif query == "deployment":
        results.append(
            InlineQueryResultArticle(
                title="Deployment",
                description="UserGe Deployment online documentation page",
                input_message_content=InputTextMessageContent(
                    f"{docs.intro}"
                    f"`Online Documentation Page for UserGe Deployment.`"
                ),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "📚 Online docs",
                        url=docs.deployment
                    )
                ]]),
                thumb_url=docs.USERGE_THUMB,
            )
        )

        for i in docs.DEPLOYMENT:
            results.append(
                InlineQueryResultArticle(
                    title=i[0],
                    description=i[1],
                    input_message_content=InputTextMessageContent(
                        docs.intro + i[2]
                    ),
                    thumb_url=docs.DEPLOYMENT_THUMB
                )
            )
    elif query == "vars":
        results.append(
            InlineQueryResultArticle(
                title="VARS",
                description="UserGe Vars online documentation page",
                input_message_content=InputTextMessageContent(
                    f"{docs.intro}"
                    f"`Online Documentation Page for UserGe Vars.`"
                ),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "📚 Online docs",
                        url=docs.vars
                    )
                ]]),
                thumb_url=docs.USERGE_THUMB,
            )
        )

        for i in docs.vars:
            results.append(
                InlineQueryResultArticle(
                    title=i[0],
                    description=i[1],
                    input_message_content=InputTextMessageContent(
                        docs.intro + i[2]
                    ),
                    thumb_url=docs.VARS_THUMB
                )
            )
    elif query == "modes":
        results.append(
            InlineQueryResultArticle(
                title="UserGe Modes",
                description="UserGe Modes online documentation page",
                input_message_content=InputTextMessageContent(
                    f"{docs.intro}"
                    f"`Online Documentation Page for UserGe Modes.`"
                ),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "📚 Online docs",
                        url=docs.modes
                    )
                ]]),
                thumb_url=docs.USERGE_THUMB,
            )
        )

        for i in docs.MODES:
            results.append(
                InlineQueryResultArticle(
                    title=i[0],
                    description=i[1],
                    input_message_content=InputTextMessageContent(
                        docs.intro + i[2]
                    ),
                    thumb_url=i[3]
                )
            )
    elif query == "example":
        results.append(
            InlineQueryResultArticle(
                title="UserGe Example",
                description="UserGe Example-Plugins online documentation page",
                input_message_content=InputTextMessageContent(
                    f"{docs.intro}"
                    f"`Online Documentation Page for UserGe Example-Plugins.`"
                ),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "📚 Online docs",
                        url=docs.example
                    )
                ]]),
                thumb_url=docs.USERGE_THUMB,
            )
        )

        for i in docs.EXAMPLE:
            results.append(
                InlineQueryResultArticle(
                    title=i[0],
                    description=i[1],
                    input_message_content=InputTextMessageContent(
                        docs.intro + i[2]
                    ),
                    thumb_url=docs.EXAMPLE_THUMB
                )
            )
    elif query in ["faq", "faqs"]:
        results.append(
            InlineQueryResultArticle(
                title="UserGe-FAQs",
                description="UserGe-FAQs online documentation page",
                input_message_content=InputTextMessageContent(
                    f"{docs.intro}"
                    f"`Online Documentation Page for UserGe-FAQs.`"
                ),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "📚 Online docs",
                        url=docs.faqs
                    )
                ]]),
                thumb_url=docs.USERGE_THUMB,
            )
        )

        for i in range(len(docs.FAQS)):
            results.append(
                InlineQueryResultArticle(
                    title=f"FAQ {i+1}",
                    description=docs.FAQS[i][0],
                    input_message_content=InputTextMessageContent(
                        f"{docs.intro}FAQ {i+1}:-\n"
                        f"[{docs.FAQS[i][0]}]({docs.FAQS[i][1]})"
                    ),
                    thumb_url=docs.FAQS_THUMB
                )
            )
    if results:
        switch_pm_text = f"📖 {len(results)} Results for \"{query}\""
        await i_q.answer(
            results=results,
            cache_time=5,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start"
        )
    else:
        await i_q.answer(
                results=[],
                cache_time=5,
                switch_pm_text=f'❌ No results for "{query}"',
                switch_pm_parameter="okay"
            )
