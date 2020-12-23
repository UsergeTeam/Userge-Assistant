# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

import time
import json

from pyrogram import filters
from pyrogram.types import (
    Message, CallbackQuery, ChatPermissions,
    InlineKeyboardMarkup, InlineKeyboardButton)

from assistant import bot, cus_filters, DB, save_data, load_data
from assistant.utils import is_admin, is_dev, is_self, sed_sticker


async def warn(msg: Message, chat_id: int, user_id: int, reason: str = "None"):
    replied = msg.reply_to_message or msg
    mention = f"[{replied.from_user.first_name}](tg://user?id={user_id})"

    w_l = (await load_data(DB.WARN_LIMIT_ID)).get(str(chat_id))
    w_m = (await load_data(DB.WARN_MODE_ID)).get(str(chat_id))
    DATA = (await load_data(DB.WARN_DATA_ID)).get(str(chat_id))

    if not DATA:
        DATA = {}
    if not (w_l or w_m):
        w_l = 3
        w_m = "ban"
    if not DATA.get(str(user_id)):
        w_d = {
            'limit': 1,
            'reason': [reason]
        }
        DATA[str(user_id)] = w_d  # warning data
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
        p_l = DATA[str(user_id)]['limit']  # previous limit
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
            reason = ('\n'.join(DATA[str(user_id)]['reason']) + '\n' + str(args))
            await msg.reply(
                f"**#WARNED_{exec_str}**\n"
                f"**{exec_str} User:** {mention}\n"
                f"**Warn Counts:** `{nw_l}/{w_l} Warnings`\n"
                f"**Reason:** `{reason}`")
            DATA.pop(str(user_id))

        else:
            DATA[str(user_id)]['limit'] = nw_l
            DATA[str(user_id)]['reason'].append(reason)
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
    ALL_WARN_DATA = (await load_data(DB.WARN_DATA_ID)).update({str(chat_id): DATA})
    WARN_MODE_DATA = (await load_data(DB.WARN_MODE_ID)).update({str(chat_id): w_m})
    WARN_LIMIT_DATA = (await load_data(DB.WARN_LIMIT_ID)).update({str(chat_id): w_l})
    await save_data(DB.WARN_DATA_ID, json.dumps(ALL_WARN_DATA))
    await save_data(DB.WARN_MODE_ID, json.dumps(WARN_MODE_DATA))
    await save_data(DB.WARN_LIMIT_ID, json.dumps(WARN_LIMIT_DATA))


@bot.on_message(
    filters.command("warn") & cus_filters.auth_chats & cus_filters.auth_users)
async def _warn_user(_, msg: Message):
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
    DATA = (await load_data(DB.WARN_DATA_ID)).get(str(c_q.message.chat.id))
    if is_admin(c_q.message.chat.id, c_q.from_user.id, check_devs=True):
        if DATA is None:
            await c_q.edit_message_text(
                "This User already not have any Warn.")
            return
        if DATA.get(user_id):
            up_l = DATA[user_id]['limit'] - 1  # up_l = updated limit
            if up_l > 0:
                DATA[user_id]['limit'] = up_l
                del DATA[user_id]['reason'][-1]
            else:
                DATA.pop(user_id)
            ALL_DATA = (await load_data(DB.WARN_DATA_ID)).update({str(c_q.message.chat.id): DATA})
            await save_data(DB.WARN_DATA_ID, json.dumps(ALL_DATA))
            text = f"[{c_q.from_user.first_name}](tg://user?id={c_q.from_user.id})"
            text += " `removed this Warn.`"
            await c_q.edit_message_text(text)
        else:
            await c_q.edit_message_text(
                "This User already not have any Warn.")
    else:
        await c_q.answer(
            "Only Admins can remove this Warn", show_alert=True)


@bot.on_message(
    filters.command("setwarn") & cus_filters.auth_chats & cus_filters.auth_users)
async def _set_warn_mode_and_limit(_, msg: Message):
    chat_id = str(msg.chat.id)
    cmd = len(msg.text)
    if msg.text and cmd == 8:
        await msg.reply("`Input not found!`")
        return
    _, args = msg.text.split(maxsplit=1)
    WARN_MODE = await load_data(DB.WARN_MODE_ID)
    WARN_LIMIT = await load_data(DB.WARN_LIMIT_ID)
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
            await msg.reply("`Can't Warn Limit less then 3`")
            return
        _LIMIT = {chat_id: input_}
        await msg.reply(f"`Warn limit Updated to {input_} Warns.`")
    else:
        await msg.reply("`invalid arguments, exiting...`")
    WARN_MODE.update(_MODE)
    WARN_LIMIT.update(_LIMIT)
    await save_data(DB.WARN_MODE_ID, json.dumps(WARN_MODE))
    await save_data(DB.WARN_LIMIT_ID, json.dumps(WARN_LIMIT))


@bot.on_message(
    filters.command("resetwarn") & cus_filters.auth_chats & cus_filters.auth_users)
async def _reset_all_warns(_, msg: Message):
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
    DATA = (await load_data(DB.WARN_DATA_ID)).get(str(msg.chat.id))
    if DATA is None:
        await msg.reply("`User already not have any warn.`")
        return
    if DATA.get(str(user_id)):
        DATA.pop(str(user_id))
        ALL_DATA = (await load_data(DB.WARN_DATA_ID)).update({str(msg.chat.id): DATA})
        await save_data(DB.WARN_DATA_ID, json.dumps(ALL_DATA))
        await msg.reply("`All Warns are removed for this User.`")
    else:
        await msg.reply("`User already not have any warn.`")


@bot.on_message(filters.command("warns") & cus_filters.auth_chats)
async def _check_warns_of_user(_, msg: Message):
    replied = msg.reply_to_message
    chat_id = str(msg.chat.id)
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
    DATA = (await load_data(DB.WARN_DATA_ID)).get(chat_id)
    w_l = (await load_data(DB.WARN_LIMIT_ID)).get(chat_id)

    if DATA is None:
        await msg.reply("`Warnings not Found.`")
        return

    if DATA.get(user_id):
        w_c = DATA[user_id]['limit']  # warn counts
        reason = '\n'.join(DATA[user_id]['reason'])
        reply_msg = (
            "**#WARNINGS**\n"
            f"**User:** {mention}\n"
            f"**Warn Counts:** `{w_c}/{w_l} Warnings.`\n"
            f"**Reason:** `{reason}`")
        await msg.reply(reply_msg)
    else:
        await msg.reply("`Warnings not Found.`")
