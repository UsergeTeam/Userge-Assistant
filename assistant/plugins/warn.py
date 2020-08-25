# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

import time

from pyrogram import (
    Message, Filters, CallbackQuery, ChatPermissions,
    InlineKeyboardMarkup, InlineKeyboardButton)

from assistant import bot, filters, Config
from assistant.utils import is_admin

WARN_LIMIT = 5
WARN_MODE = "kick"

DATA = {}


@bot.on_message(
    Filters.command("warn") & filters.auth_chats & filters.is_admin)
async def warn_user(_, msg: Message):
    global WARN_MODE, WARN_LIMIT  # pylint: disable=global-statement

    replied = msg.reply_to_message
    if not replied:
        return
    chat_id = msg.chat.id
    user_id = replied.from_user.id
    mention = f"[{replied.from_user.first_name}](tg://user?id={user_id})"

    if user_id in Config.DEV_USERS:
        await msg.reply("`He is My Master, Can't Warn him.`")
        return
    if user_id == (await bot.get_me()).id:
        await sed(msg)
        return
    if is_admin(chat_id, user_id):
        await msg.reply("`User is Admin, Can't Warn him.`")
        return

    cmd = len(msg.text)
    if msg.text and cmd == 5:
        await msg.reply("`Give a reason to warn him.`")
        return
    _, args = msg.text.split(maxsplit=1)

    w_l = WARN_LIMIT
    w_m = WARN_MODE
    if not DATA.get(user_id):
        w_d = {
            'limit': 1,
            'reason': [args]
        }
        DATA[user_id] = w_d  # warning data
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Remove this Warn",
                        callback_data=f"rm_warn({user_id})")
                ]
            ]
        )
        reply_text = f"#Warned\n{mention} has 1/{w_l} warnings.\n"
        reply_text += f"**Reason:** {args}"
        await replied.reply_text(reply_text, reply_markup=keyboard)
    else:
        p_l = DATA[user_id]['limit']  # previous limit
        nw_l = p_l + 1  # new limit
        if nw_l >= w_l:
            if w_m == "ban":
                await bot.kick_chat_member(chat_id, user_id)
                exec_str = 'BANNED'
            elif w_m == "kick":
                await bot.kick_chat_member(
                    chat_id, user_id, time.time() + 60)
                exec_str = 'KICKED'
            else:
                await bot.restrict_chat_member(
                    chat_id, user_id, ChatPermissions())
                exec_str = 'MUTED'
            reason = ('\n'.join(DATA[user_id]['reason']) + '\n' + str(args))
            await msg.reply(
                f"#WARNED_{exec_str}\n"
                f"**{exec_str} User:** {mention}\n"
                f"**Warn Counts:** {w_l}/{w_l} Warnings\n"
                f"**Reason:** {reason}")
            DATA.pop(user_id)

        else:
            DATA[user_id]['limit'] = nw_l
            DATA[user_id]['reason'].append(args)
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Remove this Warn",
                            callback_data=f"rm_warn({user_id})")
                    ]
                ]
            )
            r_t = f"#Warned\n{mention} has {nw_l}/{w_l} warnings.\n"
            r_t += f"**Reason:** {args}"   # r_t = reply text
            await replied.reply_text(r_t, reply_markup=keyboard)


@bot.on_callback_query(Filters.regex(pattern=r"rm_warn\((.+?)\)"))
async def remove_warn(_, c_q: CallbackQuery):
    user_id = int(c_q.matches[0].group(1))
    if is_admin(c_q.message.chat.id, c_q.from_user.id):
        if DATA.get(user_id):
            up_l = DATA[user_id]['limit'] - 1  # up_l = updated limit
            if up_l > 0:
                DATA[user_id]['limit'] = up_l
                del DATA[user_id]['reason'][-1]
            else:
                DATA.pop(user_id)
            text = "This Warn is Removed By "
            text += f"[{c_q.from_user.first_name}](tg://user?id={c_q.from_user.id})"
            await c_q.edit_message_text(text)
        else:
            await c_q.edit_message_text(
                "This User already not have any Warn.")
    else:
        await c_q.answer(
            "Only Admins Can Remove this Warn", show_alert=True)


@bot.on_message(
    Filters.command("setwarn") & filters.auth_chats & filters.is_admin)
async def set_warn_mode_and_limit(_, msg: Message):
    global WARN_MODE, WARN_LIMIT  # pylint: disable=global-statement
    cmd = len(msg.text)
    if msg.text and cmd == 8:
        await msg.reply("`Input not found!`")
        return
    _, args = msg.text.split(maxsplit=1)
    if 'ban' in args.lower():
        WARN_MODE = "ban"
        await msg.reply("`Warning Mode Updated to Ban`")
    elif 'kick' in args.lower():
        WARN_MODE = "kick"
        await msg.reply("`Warning Mode Updated to Kick`")
    elif 'mute' in args.lower():
        WARN_MODE = "mute"
        await msg.reply("`Warning Mode Updated to Mute`")
    elif args[0].isnumeric():
        input_ = int(args[0])
        if not input_ >= 3:
            await msg.reply("`Can't Warn Limit less then 3`")
            return
        WARN_LIMIT = input_
        await msg.reply(f"`Warn limit Updated to {input_} Warns.`")
    else:
        await msg.reply("`Invalid arguments, Exiting...`")



@bot.on_message(
    Filters.command("resetwarn") & filters.auth_chats & filters.is_admin)
async def reset_all_warns(_, msg: Message):
    replied = msg.reply_to_message
    if not replied:
        return
    user_id = replied.from_user.id
    if user_id in Config.DEV_USERS:
        await msg.reply("`He is My Master, I never Warned him.`")
        return
    if user_id == (await bot.get_me()).id:
        await sed(msg)
        return
    if is_admin(msg.chat.id, user_id):
        await msg.reply("`He is admin, I never Warned him.`")
        return
    if DATA.get(user_id):
        DATA.pop(user_id)
        await msg.reply("`All Warns are removed for this User.`")
    else:
        await msg.reply("`User already not have any warn.`")


@bot.on_message(Filters.command("warns") & filters.auth_chats)
async def check_warns_of_user(_, msg: Message):
    global WARN_LIMIT  # pylint: disable=global-statement
    replied = msg.reply_to_message
    if replied:
        user_id = replied.from_user.id
        mention = f"[{replied.from_user.first_name}](tg://user?id={user_id})"
    else:
        user_id = msg.from_user.id
        mention = f"[{msg.from_user.first_name}](tg://user?id={user_id})"
    if user_id in Config.DEV_USERS:
        await msg.reply("`He is My Master, I never Warned him.`")
        return
    if user_id == (await bot.get_me()).id:
        await sed(msg)
        return
    if is_admin(msg.chat.id, user_id):
        await msg.reply("`He is admin, I never Warned him.`")
        return
    if replied and not is_admin(msg.chat.id, msg.from_user.id):
        await msg.reply("`You can Only see your Warnings.`")
        return
    if DATA.get(user_id):
        w_c = DATA[user_id]['limit']  # warn counts
        reason = '\n'.join(DATA[user_id]['reason'])
        reply_msg = (
            "#WARNINGS\n"
            f"**User:** {mention}\n"
            f"**Warn Counts:** {w_c}/{WARN_LIMIT} Warnings\n"
            f"**Reason:** {reason}")
        await msg.reply(reply_msg)
    else:
        await msg.reply("`Warnings not Found.`")


async def sed(msg: Message):
    sticker = (await bot.get_messages('UserGeOt', 498697)).sticker
    file_id = sticker.file_id
    fileref = sticker.file_ref
    await bot.send_sticker(
        msg.chat.id, file_id, file_ref=fileref)
