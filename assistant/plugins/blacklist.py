# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__commands__ = ["addblacklist", "delblacklist", "listblacklist", "setblacklist"]

import re
import time
import json
import asyncio

from typing import Dict, List
from pyrogram.types import Message, ChatPermissions

from assistant import bot, filters, cus_filters as Filters
from assistant.plugins.warn import warn as warn_user
from assistant.utils import check_bot_rights, _is_spammer

user_dict = {}


@bot.on_cmd("addblacklist", about={
    'description': "Add Blacklist trigger. You can add multiple "
                   "triggers by seperate them with new line.",
    'usage': ["/addblacklist {trigger}", "/addblacklist {trigger}\n{trigger}"]
}, admin_only=True)
async def _add_blacklist(msg: Message):
    if msg.text and len(msg.text) == 13:
        await msg.reply("`Input not found...`")
        return
    _, args = msg.text.split(maxsplit=1)
    chat_id = str(msg.chat.id)

    BLACK_LIST = await bot.load_data(bot.BLACKLIST_DATA_ID)
    triggers = list({trigger.strip()
                    for trigger in args.lower().split("\n") if trigger.strip()})
    for word in triggers:
        if BLACK_LIST.get(chat_id):
            BLACK_LIST[chat_id].append(word)
        else:
            BLACK_LIST[chat_id] = [word]
    await bot.save_data(bot.BLACKLIST_DATA_ID, json.dumps(BLACK_LIST))
    if len(triggers) == 1:
        out = f"added `{triggers[0]}` to blacklist."
    else:
        out = f"added `{len(triggers)} words` to blacklist."
    await msg.reply(out)


@bot.on_cmd("delblacklist", about={
    'description': "Delete Blacklist trigger. You can delete multiple "
                   "triggers by seperate them with new line.",
    'usage': ["/delblacklist {trigger}", "/delblacklist {trigger}\n{trigger}"]
}, admin_only=True)
async def _del_blacklist(msg: Message):
    global BLACK_LIST  # pylint: disable=global-statement
    if msg.text and len(msg.text) == 13:
        await msg.reply("`Input not found...`")
        return
    _, args = msg.text.split(maxsplit=1)
    chat_id = str(msg.chat.id)

    triggers = list({trigger.strip()
                    for trigger in args.split("\n") if trigger.strip()})
    success = 0
    failure = 0
    BLACK_LIST = await bot.load_data(bot.BLACKLIST_DATA_ID)
    for word in triggers:
        if word in BLACK_LIST.get(chat_id):
            BLACK_LIST[chat_id].remove(word)
            success += 1
        else:
            failure += 1
    await bot.save_data(bot.BLACKLIST_DATA_ID, json.dumps(BLACK_LIST))
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


@bot.on_cmd("listblacklist", about={
    'description': "List all blacklisted triggers.",
    'usage': "/listbalcklist"})
async def _blacklist(msg: Message):
    chat_id = str(msg.chat.id)
    BLACK_LIST = await bot.load_data(bot.BLACKLIST_DATA_ID)
    if BLACK_LIST.get(chat_id) is None:
        bl_words = f"`Blacklist empty for {msg.chat.title}`"
    else:
        bl_words = f"Blacklist Words in `{msg.chat.title}`:-\n"
        for trigger in BLACK_LIST.get(chat_id):
            bl_words += f"- `{trigger}`\n"
    await msg.reply(bl_words)


@bot.on_cmd("setblacklist", about={
    'description': "Set blacklist Mode.",
    'usage': "/setblacklist {mode}"
}, admin_only=True)
async def _set_blacklist_mode(msg: Message):
    if msg.text and len(msg.text) == 13:
        await msg.reply("`Input not found...`")
        return
    _, args = msg.text.split(maxsplit=1)
    chat_id = str(msg.chat.id)
    BLACKLIST_MODE = await bot.load_data(bot.BLACKLIST_MODE_ID)
    _MODE = {chat_id: "warn"}
    if 'warn' in args.lower():
        _MODE = {chat_id: "warn"}
        await msg.reply("`Blacklist Mode Updated to Warn`")
    elif 'ban' in args.lower():
        _MODE = {chat_id: "ban"}
        await msg.reply("`Blacklist Mode Updated to Ban`")
    elif 'kick' in args.lower():
        _MODE = {chat_id: "kick"}
        await msg.reply("`Blacklist Mode Updated to Kick`")
    elif 'mute' in args.lower():
        _MODE = {chat_id: "mute"}
        await msg.reply("`Blacklist Mode Updated to Mute`")
    elif 'off' in args.lower():
        _MODE = {chat_id: "off"}
        await msg.reply("`Blacklist Turned Off...`")
    elif 'del' in args.lower():
        _MODE = {chat_id: "del"}
        await msg.reply("`Now Blacklisted word will only delete.`")
    else:
        await msg.reply("`Invalid arguments, Exiting...`")
    BLACKLIST_MODE.update(_MODE)
    await bot.save_data(bot.BLACKLIST_MODE_ID, json.dumps(BLACKLIST_MODE))


@bot.on_filters(
    filters.incoming & ~filters.edited & Filters.auth_chats & ~Filters.auth_users, group=1
)
async def _filter_blacklist(msg: Message):
    chat_id = str(msg.chat.id)
    BLACK_LIST = await bot.load_data(bot.BLACKLIST_DATA_ID)
    BLACKLIST_MODE = await bot.load_data(bot.BLACKLIST_MODE_ID)
    if BLACKLIST_MODE.get(chat_id) is None:
        BLACKLIST_MODE.update({chat_id: "warn"})
        await bot.save_data(bot.BLACKLIST_MODE_ID, json.dumps(BLACKLIST_MODE))
    if BLACK_LIST.get(chat_id) is None:
        return
    if not user_dict.get(msg.from_user.id):
        bio = (await bot.get_chat(msg.from_user.id)).bio
        if not bio:
            bio = "No Bio"
        user_dict[msg.from_user.id] = bio
    if await _is_spammer(int(chat_id), msg.from_user.id, user_dict[msg.from_user.id]):
        return
    text = None
    if msg.text:
        text = msg.text.lower()
    elif msg.caption:
        text = msg.caption.lower()
    if text and BLACK_LIST.get(chat_id) is not None:
        for trigger in BLACK_LIST.get(chat_id):
            pattern = r"( |^|[^\w])" + re.escape(trigger) + r"( |$|[^\w])"
            if re.search(pattern, text, re.IGNORECASE):
                reason = f"Due to match on {trigger} Blacklisted word."
                try:
                    if await check_bot_rights(msg.chat.id, "can_delete_messages"):
                        await msg.delete()
                    if BLACKLIST_MODE.get(chat_id) == "del":
                        if await check_bot_rights(msg.chat.id, "can_delete_messages"):
                            await msg.reply(f"#DELETED\n\n{reason}")
                    elif BLACKLIST_MODE.get(chat_id) == "warn":
                        await warn_user(msg, msg.chat.id, msg.from_user.id, reason)
                    elif BLACKLIST_MODE.get(chat_id) == "ban":
                        await asyncio.gather(
                            bot.kick_chat_member(msg.chat.id, msg.from_user.id),
                            msg.reply(f"#BANNED\n\n{reason}")
                        )
                    elif BLACKLIST_MODE.get(chat_id) == "kick":
                        await asyncio.gather(
                            bot.kick_chat_member(
                                msg.chat.id, msg.from_user.id, time.time() + 45),
                            msg.reply(f"#KICKED\n\n{reason}")
                        )
                    elif BLACKLIST_MODE.get(chat_id) == "mute":
                        await asyncio.gather(
                            bot.restrict_chat_member(
                                msg.chat.id, msg.from_user.id, ChatPermissions()),
                            msg.reply(f"#MUTED\n\n{reason}")
                        )
                except Exception:
                    pass
                break
