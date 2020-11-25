# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram.types import (
    InlineQuery, InlineQueryResultArticle, InputTextMessageContent,
    InlineQueryResultPhoto, InlineKeyboardButton, InlineKeyboardMarkup)

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
    if query in ["decorator", "decorators"]:
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
                        docs.intro + i[2], disable_web_page_preview=True
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
                        docs.intro + i[2], disable_web_page_preview=True
                    ),
                    thumb_url=docs.DEPLOYMENT_THUMB
                )
            )
    elif query in ["var", "vars"]:
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

        for i in docs.VARS:
            results.append(
                InlineQueryResultArticle(
                    title=i[0],
                    description=i[1],
                    input_message_content=InputTextMessageContent(
                        docs.intro + i[2], disable_web_page_preview=True
                    ),
                    thumb_url=docs.VARS_THUMB
                )
            )
    elif query in ["mode", "modes"]:
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
                        docs.intro + i[2], disable_web_page_preview=True
                    ),
                    thumb_url=i[3]
                )
            )
    elif query in ["example", "examples"]:
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
                        url=docs.examples
                    )
                ]]),
                thumb_url=docs.USERGE_THUMB,
            )
        )

        for i in docs.EXAMPLES:
            results.append(
                InlineQueryResultArticle(
                    title=i[0],
                    description=i[1],
                    input_message_content=InputTextMessageContent(
                        docs.intro + i[2], disable_web_page_preview=True
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
                        f"{docs.intro}**FAQ {i+1}:-**\n"
                        f"[{docs.FAQS[i][0]}]({docs.FAQS[i][1]})",
                        disable_web_page_preview=True
                    ),
                    thumb_url=docs.FAQS_THUMB
                )
            )
    elif query in ["error", "errors"]:
        results.append(
            InlineQueryResultArticle(
                title="Errors and their Fixes",
                input_message_content=InputTextMessageContent(
                    f"{docs.intro}"
                    f"`Online Documentation Page for UserGe-Errors.`"
                ),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "📚 Online docs",
                        url=docs.errors
                    )
                ]]),
                thumb_url=docs.ERRORS_THUMB,
            )
        )

        for i in range(len(docs.ERRORS)):
            results.append(
                InlineQueryResultPhoto(
                    photo_url=f"{docs.ERRORS[i][2]}",
                    title=f"{docs.ERRORS[i][0]}",
                    caption=(
                        f"[{docs.ERRORS[i][0]}]({docs.errors}{docs.ERRORS[i][1]})"
                    )
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
