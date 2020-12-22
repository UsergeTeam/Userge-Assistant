# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

import re
import time
import json
import asyncio

from typing import Dict, List
from pyrogram import filters
from pyrogram.types import Message, ChatPermissions

from assistant import bot, cus_filters as Filters, DB, save_data, load_data
from assistant.plugins.warn import warn as warn_user
from assistant.utils import check_bot_rights


@bot.on_message(
    filters.command("addblacklist") & Filters.auth_chats & Filters.auth_users)
async def _add_blacklist(_, msg: Message):
    if msg.text and len(msg.text) == 13:
        await msg.reply("`Input not found...`")
        return
    _, args = msg.text.split(maxsplit=1)

    BLACK_LIST = await load_data(DB.BLACKLIST_DATA_ID)
    triggers = list({trigger.strip()
                    for trigger in args.lower().split("\n") if trigger.strip()})
    for word in triggers:
        if BLACK_LIST.get(msg.chat.id):
            BLACK_LIST[msg.chat.id].append(word)
        else:
            BLACK_LIST[msg.chat.id] = [word]
    await save_data(DB.BLACKLIST_DATA_ID, json.dumps(BLACK_LIST))
    if len(triggers) == 1:
        out = f"added `{triggers[0]}` to blacklist."
    else:
        out = f"added `{len(triggers)} words` to blacklist."
    await msg.reply(out)


@bot.on_message(
    filters.command("delblacklist") & Filters.auth_chats & Filters.auth_users)
async def _del_blacklist(_, msg: Message):
    global BLACK_LIST  # pylint: disable=global-statement
    if msg.text and len(msg.text) == 13:
        await msg.reply("`Input not found...`")
        return
    _, args = msg.text.split(maxsplit=1)
    triggers = list({trigger.strip()
                    for trigger in args.split("\n") if trigger.strip()})
    success = 0
    failure = 0
    BLACK_LIST = await load_data(DB.BLACKLIST_DATA_ID)
    for word in triggers:
        if word in BLACK_LIST.get(msg.chat.id):
            BLACK_LIST[msg.chat.id].remove(word)
            success += 1
        else:
            failure += 1
    await save_data(DB.BLACKLIST_DATA_ID, json.dumps(BLACK_LIST))
    if len(triggers) == 1:
        if success:
            out = f"`{triggers[0]}` deleted from blacklist."
        else:
            out = f"`{triggers[0]}` is not in blacklist."
    elif failure == len(triggers):
        out = "`None of these words are in my blacklist.`"
    elif success == len(triggers):
        out = f"`{len(triggers)} words` deleted from blacklist."
    else:
        out = f"`{success} words` deleted from blacklist, "
        out += f"`{failure} words` not in blacklist."
    await msg.reply(out)


@bot.on_message(
    filters.command("blacklist") & Filters.auth_chats)
async def _blacklist(_, msg: Message):
    BLACK_LIST = await load_data(DB.BLACKLIST_DATA_ID)
    if not BLACK_LIST.get(msg.chat.id):
        bl_words = f"`Blacklist empty for {msg.chat.title}`"
    bl_words = f"Blacklist Words in `{msg.chat.title}`:-\n"
    for trigger in BLACK_LIST.get(msg.chat.id):
        bl_words += f"- `{trigger}`\n"
    await msg.reply(bl_words)


@bot.on_message(
    filters.command("setblacklist") & Filters.auth_chats & Filters.auth_users)
async def _set_blacklist_mode(_, msg: Message):
    if msg.text and len(msg.text) == 13:
        await msg.reply("`Input not found...`")
        return
    _, args = msg.text.split(maxsplit=1)
    BLACKLIST_MODE = await load_data(DB.BLACKLIST_MODE_ID)
    _MODE = {msg.chat.id: "warn"}
    if 'warn' in args.lower():
        _MODE = {msg.chat.id: "warn"}
        await msg.reply("`Blacklist Mode Updated to Warn`")
    elif 'ban' in args.lower():
        _MODE = {msg.chat.id: "ban"}
        await msg.reply("`Blacklist Mode Updated to Ban`")
    elif 'kick' in args.lower():
        _MODE = {msg.chat.id: "kick"}
        await msg.reply("`Blacklist Mode Updated to Kick`")
    elif 'mute' in args.lower():
        _MODE = {msg.chat.id: "mute"}
        await msg.reply("`Blacklist Mode Updated to Mute`")
    elif 'off' in args.lower():
        _MODE = {msg.chat.id: "off"}
        await msg.reply("`Blacklist Turned Off...`")
    elif 'del' in args.lower():
        _MODE = {msg.chat.id: "del"}
        await msg.reply("`Now Blacklisted word will only delete.`")
    else:
        await msg.reply("`Invalid arguments, Exiting...`")
    data = BLACKLIST_MODE.update(_MODE)
    await save_data(DB.BLACKLIST_MODE_ID, json.dumps(data))


@bot.on_message(
    filters.incoming & ~filters.edited & Filters.auth_chats & ~Filters.auth_users, group=1
)
async def _filter_blacklist(_, msg: Message):
    BLACK_LIST = await load_data(DB.BLACKLIST_DATA_ID)
    BLACKLIST_MODE = await load_data(DB.BLACKLIST_MODE_ID)

    if not BLACK_LIST.get(msg.chat.id):
        return
    text = None
    if msg.text:
        text = msg.text.lower()
    elif msg.caption:
        text = msg.caption.lower()
    if text:
        for trigger in BLACK_LIST.get(msg.chat.id):
            pattern = r"( |^|[^\w])" + re.escape(trigger) + r"( |$|[^\w])"
            if re.search(pattern, text, re.IGNORECASE):
                reason = f"Due to match on {trigger} Blacklisted word."
                try:
                    if await check_bot_rights(msg.chat.id, "can_delete_messages"):
                        await msg.delete()
                    if BLACKLIST_MODE == "del":
                        if await check_bot_rights(msg.chat.id, "can_delete_messages"):
                            await msg.reply(f"#DELETED\n\n{reason}")
                    elif BLACKLIST_MODE == "warn":
                        await warn_user(msg, msg.chat.id, msg.from_user.id, reason)
                    elif BLACKLIST_MODE == "ban":
                        await asyncio.gather(
                            bot.kick_chat_member(msg.chat.id, msg.from_user.id),
                            msg.reply(f"#BANNED\n\n{reason}")
                        )
                    elif BLACKLIST_MODE == "kick":
                        await asyncio.gather(
                            bot.kick_chat_member(
                                msg.chat.id, msg.from_user.id, time.time() + 45),
                            msg.reply(f"#KICKED\n\n{reason}")
                        )
                    elif BLACKLIST_MODE == "mute":
                        await asyncio.gather(
                            bot.restrict_chat_member(
                                msg.chat.id, msg.from_user.id, ChatPermissions()),
                            msg.reply(f"#MUTED\n\n{reason}")
                        )
                except Exception:
                    pass
                break
