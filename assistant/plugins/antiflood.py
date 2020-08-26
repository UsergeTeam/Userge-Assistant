# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

import time

from pyrogram import Message, Filters
from assistant import bot, filters

DATA = {}

MSG_LIMIT = 8
WARN_LIMIT = 5
MIN_DELAY = 3


@bot.on_message(
    Filters.incoming & ~Filters.edited & filters.auth_chats & ~filters.auth_users, group=1)
async def _flood(_, message: Message):
    chat_flood = DATA.get(message.chat.id)
    if chat_flood is None:
        data = {
            'user_id': message.from_user.id,
            'time': time.time(),
            'count': 1
        }
        DATA[message.chat.id] = data
        return
    cur_user = message.from_user.id
    if cur_user != chat_flood['user_id']:
        data = {
            'user_id': cur_user,
            'time': time.time(),
            'count': 1
        }
        DATA[message.chat.id] = data
        return
    prev_count = chat_flood['count']
    prev_time = chat_flood['time']
    if (time.time() - prev_time) < MIN_DELAY:
        count = prev_count + 1
        if count >= MSG_LIMIT:
            await message.chat.kick_member(cur_user, until_date=int(time.time() + 45))
            await message.reply("**MAX FLOOD LIMIT REACHED**\n User Has been Kicked.")
        elif count == WARN_LIMIT:
            await message.reply("**WARN**\n `Flood Detected !`")
    else:
        count = 1
    DATA[message.chat.id] = {'user_id': cur_user, 'time': time.time(), 'count': count}
    message.continue_propagation()
