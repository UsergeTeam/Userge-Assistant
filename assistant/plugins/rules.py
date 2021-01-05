# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__commands__ = ["rules"]

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from assistant import bot, Message


@bot.on_cmd("rules", about="Rules for @UsereOt")
async def _rules(message: Message):
    replied = message.reply_to_message
    if replied:
        msg_id = replied.message_id
    else:
        msg_id = message.message_id
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Read Rules",
                    url="https://t.me/usergeot/537063"
                )
            ]
        ]
    )
    await bot.send_message(chat_id=message.chat.id,
                           text="**⚠️ Here Our RULES ⚠️**",
                           reply_to_message_id=msg_id,
                           reply_markup=markup)
