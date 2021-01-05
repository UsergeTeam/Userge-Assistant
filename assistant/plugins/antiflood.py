# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__commands__ = ["setflood"]

import time
import json
import asyncio

from pyrogram import filters
from pyrogram.types import ChatPermissions
from assistant import bot, cus_filters, Message
from assistant.plugins.warn import warn as warn_user

DATA = {}

LIMIT = await bot.load_data(bot.FLOOD_LIMIT_ID)
MODE = await bot.load_data(bot.FLOOD_MODE_ID)
DELAY = 3


@bot.on_cmd("setflood", about={
    'description': "Set flood mode or flood limit.",
    'usage': ["/setflood [flood limit]", "/setflood [flood mode]"],
    'examples': ["/setflood 5", "/setflood warn"]
}, admin_only=True)
async def _set_warn_mode_and_limit(msg: Message):
    chat_id = str(msg.chat.id)
    cmd = len(msg.text)
    if msg.text and cmd == 8:
        await msg.reply("`Input not found!`")
        return
    _, args = msg.text.split(maxsplit=1)
    FLOOD_MODE = await bot.load_data(bot.FLOOD_MODE_ID)
    FLOOD_LIMIT = await bot.load_data(bot.FLOOD_LIMIT_ID)
    _MODE = {chat_id: 'ban'}
    _LIMIT = {chat_id: 3}
    if 'ban' in args.lower():
        _MODE = {chat_id: 'ban'}
        await msg.reply("`AntiFlood Mode Updated to Ban`")
    elif 'kick' in args.lower():
        _MODE = {chat_id: 'kick'}
        await msg.reply("`AntiFlood Mode Updated to Kick`")
    elif 'warn' in args.lower():
        _MODE = {chat_id: 'warn'}
        await msg.reply("`AntiFlood Mode Updated to Warn`")
    elif 'mute' in args.lower():
        _MODE = {chat_id: 'mute'}
        await msg.reply("`AntiFlood Mode Updated to Mute`")
    elif args[0].isnumeric():
        input_ = int(args[0])
        if input_ < 5:
            await msg.reply("`Can't set AntiFlood Limit less then 5`")
            return
        _LIMIT = {chat_id: input_}
        await msg.reply(f"`AntiFlood limit Updated to {input_}`")
    else:
        await msg.reply("`invalid arguments!`")
    FLOOD_MODE.update(_MODE)
    FLOOD_LIMIT.update(_LIMIT)
    await bot.save_data(bot.FLOOD_MODE_ID, json.dumps(FLOOD_MODE))
    await bot.save_data(bot.FLOOD_LIMIT_ID, json.dumps(FLOOD_LIMIT))


@bot.on_filter(filters.incoming & ~filters.edited & cus_filters.auth_chats &
                ~cus_filters.auth_users & ~cus_filters.whitelist_chats, group=1)
async def _flood(message: Message):
    if not LIMIT.get(str(message.chat.id)):
        LIMIT = {str(message.chat.id): 5}
        await bot.save_data(bot.FLOOD_LIMIT_ID, json.dumps(LIMIT))
    elif not MODE.get(str(message.chat.id)):
        MODE = {str(message.chat.id): "warn"}
        await bot.save_data(bot.FLOOD_MODE_ID, json.dumps(MODE))
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
    if (time.time() - prev_time) < DELAY:
        count = prev_count + 1
        if count >= LIMIT:
            reason = "User Flood Limit reached"
            if MODE.get(str(message.chat.id)) == "warn":
                await warn_user(
                    message, message.chat.id, message.from_user.id, reason)
            elif MODE.get(str(message.chat.id)) == "ban":
                await asyncio.gather(
                    bot.kick_chat_member(message.chat.id, message.from_user.id),
                    message.reply(f"#BANNED\n\n{reason}")
                )
            elif MODE.get(str(message.chat.id)) == "kick":
                await asyncio.gather(
                    bot.kick_chat_member(
                        message.chat.id, message.from_user.id, time.time() + 45),
                    message.reply(f"#KICKED\n\n{reason}")
                )
            elif MODE.get(str(message.chat.id)) == "mute":
                await asyncio.gather(
                    bot.restrict_chat_member(
                        message.chat.id, message.from_user.id, ChatPermissions()),
                    message.reply(f"#MUTED\n\n{reason}")
                )
    DATA[message.chat.id] = {'user_id': cur_user, 'count': count}
    message.continue_propagation()
