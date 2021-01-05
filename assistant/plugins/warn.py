# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__commands__ = ["warn", "setwarn", "resetwarn", "warns"]

import time
import json

from pyrogram.types import (
    CallbackQuery, ChatPermissions,
    InlineKeyboardMarkup, InlineKeyboardButton)

from assistant import bot, filters, Message
from assistant.utils import is_admin, is_dev, is_self, sed_sticker


async def warn(msg: Message, chat_id: int, user_id: int, reason: str = "None"):
    replied = msg.reply_to_message or msg
    mention = f"[{replied.from_user.first_name}](tg://user?id={user_id})"

    w_lt = await bot.load_data(bot.WARN_LIMIT_ID)
    w_me = await bot.load_data(bot.WARN_MODE_ID)
    DATA = await bot.load_data(bot.WARN_DATA_ID)

    if not DATA.get(str(chat_id)):
        DATA[str(chat_id)] = {}
    if not (
        w_lt.get(str(chat_id)) or w_me.get(str(chat_id))
    ):
        w_lt[str(chat_id)] = 3
        w_me[str(chat_id)] = "ban"
    w_l = w_lt.get(str(chat_id))
    w_m = w_me.get(str(chat_id))
    if not DATA[str(chat_id)].get(str(user_id)):
        w_d = {
            'limit': 1,
            'reason': [reason]
        }
        DATA[str(chat_id)][str(user_id)] = w_d  # warning data
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Remove Warn",
                        callback_data=f"rm_warn({user_id})")
                ]
            ]
        )
        reply_text = f"**#Warned**\n{mention} `has 1/{w_l} warnings.`\n"
        reply_text += f"**Reason:** `{reason}`"
        await replied.reply_text(reply_text, reply_markup=keyboard)
    else:
        p_l = DATA[str(chat_id)][str(user_id)]['limit']  # previous limit
        nw_l = p_l + 1  # new limit
        if nw_l >= w_l:
            if w_m == "ban":
                await bot.kick_chat_member(chat_id, user_id)
                exec_str = 'BANNED'
            elif w_m == "kick":
                await bot.kick_chat_member(
                    chat_id, user_id, time.time() + 300)
                exec_str = 'KICKED'
            else:
                await bot.restrict_chat_member(
                    chat_id, user_id, ChatPermissions())
                exec_str = 'MUTED'
            reasons = ('\n'.join(DATA[str(chat_id)][str(user_id)]['reason']) + '\n' + str(reason))
            await msg.reply(
                f"**#WARNED_{exec_str}**\n"
                f"**{exec_str} User:** {mention}\n"
                f"**Warn Counts:** `{nw_l}/{w_l} Warnings`\n"
                f"**Reason:** `{reasons}`")
            DATA[str(chat_id)].pop(str(user_id))

        else:
            DATA[str(chat_id)][str(user_id)]['limit'] = nw_l
            DATA[str(chat_id)][str(user_id)]['reason'].append(reason)
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Remove Warn",
                            callback_data=f"rm_warn({user_id})")
                    ]
                ]
            )
            r_t = f"**#Warned**\n{mention} `has {nw_l}/{w_l} warnings.`\n"
            r_t += f"**Reason:** `{reason}`"   # r_t = reply text
            await replied.reply_text(r_t, reply_markup=keyboard)
    await bot.save_data(bot.WARN_DATA_ID, json.dumps(DATA))
    await bot.save_data(bot.WARN_MODE_ID, json.dumps(w_me))
    await bot.save_data(bot.WARN_LIMIT_ID, json.dumps(w_lt))


@bot.on_cmd("warn", about={
    'description': "Warn user in Supergroup.",
    'usage': "/warn [reply to user] [reason: optional]"
}, admin_only=True)
async def _warn_user(msg: Message):
    replied = msg.reply_to_message
    if not replied:
        return
    chat_id = msg.chat.id
    user_id = replied.from_user.id
    if is_dev(user_id):
        await msg.reply("`He is My Master, Can't Warn him.`")
        return
    if await is_self(user_id):
        await sed_sticker(msg)
        return
    if is_admin(chat_id, user_id):
        await msg.reply("`User is Admin, Can't Warn him.`")
        return
    cmd = len(msg.text)
    reason = None
    if msg.text and cmd > 5:
        _, reason = msg.text.split(maxsplit=1)
    await warn(msg, chat_id, user_id, reason)


@bot.on_callback_query(filters.regex(pattern=r"rm_warn\((.+?)\)"))
async def remove_warn(_, c_q: CallbackQuery):
    user_id = str(c_q.matches[0].group(1))
    DATA = await bot.load_data(bot.WARN_DATA_ID)
    if is_admin(c_q.message.chat.id, c_q.from_user.id, check_devs=True):
        if DATA.get(str(c_q.message.chat.id)) is None:
            await c_q.edit_message_text(
                "This User already not have any Warn.")
            return
        if DATA[str(c_q.message.chat.id)].get(user_id):
            up_l = DATA[str(c_q.message.chat.id)][user_id]['limit'] - 1  # up_l = updated limit
            if up_l > 0:
                DATA[str(c_q.message.chat.id)][user_id]['limit'] = up_l
                del DATA[str(c_q.message.chat.id)][user_id]['reason'][-1]
            else:
                DATA[str(c_q.message.chat.id)].pop(user_id)
            await bot.save_data(bot.WARN_DATA_ID, json.dumps(DATA))
            text = f"[{c_q.from_user.first_name}](tg://user?id={c_q.from_user.id})"
            text += " `removed this Warn.`"
            await c_q.edit_message_text(text)
        else:
            await c_q.edit_message_text(
                "This User already not have any Warn.")
    else:
        await c_q.answer(
            "Only Admins can remove this Warn", show_alert=True)


@bot.on_cmd("setwarn", about={
    'description': "Set Warn mode or Warn limit.",
    'usage': ["/setwarn [warn limit]", "/setwarn [warn mode]"],
    'examples': ["/setwarn 5", "/setwarn ban"]
}, admin_only=True)
async def _set_warn_mode_and_limit(msg: Message):
    chat_id = str(msg.chat.id)
    cmd = len(msg.text)
    if msg.text and cmd == 8:
        await msg.reply("`Input not found!`")
        return
    _, args = msg.text.split(maxsplit=1)
    WARN_MODE = await bot.load_data(bot.WARN_MODE_ID)
    WARN_LIMIT = await bot.load_data(bot.WARN_LIMIT_ID)
    _MODE = {chat_id: 'ban'}
    _LIMIT = {chat_id: 3}
    if 'ban' in args.lower():
        _MODE = {chat_id: 'ban'}
        await msg.reply("`Warning Mode Updated to Ban`")
    elif 'kick' in args.lower():
        _MODE = {chat_id: 'kick'}
        await msg.reply("`Warning Mode Updated to Kick`")
    elif 'mute' in args.lower():
        _MODE = {chat_id: 'mute'}
        await msg.reply("`Warning Mode Updated to Mute`")
    elif args[0].isnumeric():
        input_ = int(args[0])
        if input_ < 3:
            await msg.reply("`Can't set Warn Limit less then 3`")
            return
        _LIMIT = {chat_id: input_}
        await msg.reply(f"`Warn limit Updated to {input_} Warns.`")
    else:
        await msg.reply("`invalid arguments, exiting...`")
    WARN_MODE.update(_MODE)
    WARN_LIMIT.update(_LIMIT)
    await bot.save_data(bot.WARN_MODE_ID, json.dumps(WARN_MODE))
    await bot.save_data(bot.WARN_LIMIT_ID, json.dumps(WARN_LIMIT))


@bot.on_cmd("resetwarn", about={
    'description': "Reset all Warns of User.",
    'usage': "/resetwarn [reply to user]"
}, admin_only=True)
async def _reset_all_warns(msg: Message):
    replied = msg.reply_to_message
    if not replied:
        return
    user_id = replied.from_user.id
    if is_dev(user_id):
        await msg.reply("`He is My Master, I never Warned him.`")
        return
    if await is_self(user_id):
        return
    if is_admin(msg.chat.id, user_id):
        await msg.reply("`He is admin, I never Warned him.`")
        return
    DATA = await bot.load_data(bot.WARN_DATA_ID)
    if DATA.get(str(msg.chat.id)) is None:
        await msg.reply("`User already not have any warn.`")
        return
    if DATA[str(msg.chat.id)].get(str(user_id)):
        DATA[str(msg.chat.id)].pop(str(user_id))
        await bot.save_data(bot.WARN_DATA_ID, json.dumps(DATA))
        await msg.reply("`All Warns are removed for this User.`")
    else:
        await msg.reply("`User already not have any warn.`")


@bot.on_cmd("warns", about={
    'description': "See Warnings.",
    'usage': ["/warns", "/warns [reply to user]"]})
async def _check_warns_of_user(msg: Message):
    replied = msg.reply_to_message
    if replied:
        user_id = str(replied.from_user.id)
        mention = f"[{replied.from_user.first_name}](tg://user?id={user_id})"
    else:
        user_id = str(msg.from_user.id)
        mention = f"[{msg.from_user.first_name}](tg://user?id={user_id})"
    if is_dev(int(user_id)):
        await msg.reply("`He is My Master, I never Warned him.`")
        return
    if await is_self(int(user_id)):
        return
    if is_admin(msg.chat.id, int(user_id)):
        await msg.reply("`He is admin, I never Warned him.`")
        return
    if replied and not is_admin(msg.chat.id, msg.from_user.id, check_devs=True):
        await msg.reply("`You can only see your Warnings.`")
        return
    DATA = await bot.load_data(bot.WARN_DATA_ID)
    w_l = (await bot.load_data(bot.WARN_LIMIT_ID)).get(str(msg.chat.id))
    if DATA.get(str(msg.chat.id)) is None:
        await msg.reply("`Warnings not Found.`")
        return

    if DATA[str(msg.chat.id)].get(user_id):
        w_c = DATA[str(msg.chat.id)][user_id]['limit']  # warn counts
        reason = '\n'.join(DATA[str(msg.chat.id)][user_id]['reason'])
        reply_msg = (
            "**#WARNINGS**\n"
            f"**User:** {mention}\n"
            f"**Warn Counts:** `{w_c}/{w_l} Warnings.`\n"
            f"**Reason:** `{reason}`")
        await msg.reply(reply_msg)
    else:
        await msg.reply("`Warnings not Found.`")
