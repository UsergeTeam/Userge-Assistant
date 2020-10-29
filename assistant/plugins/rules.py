# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from assistant import bot, cus_filters


@bot.on_message(filters.command("rules") & cus_filters.auth_chats)
async def _rules(_, message: Message):
    replied = message.reply_to_message
    if replied:
        msg_id = replied.message_id
    else:
        msg_id = message.message_id
    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Read Rules",
                               callback_data="rules")]]
    )
    await bot.send_message(chat_id=message.chat.id,
                           text="**⚠️ Here Our RULES ⚠️**",
                           reply_to_message_id=msg_id,
                           reply_markup=markup)


@bot.on_callback_query(filters.regex(pattern=r"^rules$"))
async def _rules_cq(_, c_q: CallbackQuery):
    await c_q.answer(url="https://t.me/usergeot/537063")
