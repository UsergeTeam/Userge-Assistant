# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import Message, Filters
from assistant import bot, filters

DATA = {}

@bot.on_message(Filters.incoming & ~Filters.edited & filters.auth_chats & ~filters.is_admin)
async def flood(_, message: Message):
    limit = 5
    chat_flood = DATA.get(message.chat.id)
    if chat_flood is None:
        data = {
            'user_id': message.from_user.id,
            'count': 1
        }
        DATA[message.chat.id] = data
        return
    cur_user = message.from_user.id
    if cur_user != chat_flood['user_id']:
        data = {
            'user_id': cur_user,
            'count': 1
        }
        DATA[message.chat.id] = data
        return
    perv_count = chat_flood['count']
    count = perv_count + 1
    if count >= limit:
        await message.chat.kick_member(cur_user)
        await message.reply("**MAX FLOOD LIMIT REACHED**\n User Has been Banned")
        return
    DATA[message.chat.id] = {'user_id': cur_user, 'count': count}
