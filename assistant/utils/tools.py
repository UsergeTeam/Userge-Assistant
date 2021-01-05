# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

import re
import time
from typing import Union, List, Dict

from pyrogram.types import Message

from assistant import bot, Config

_BOT_ID = 0


def time_formatter(seconds: float) -> str:
    """ humanize time """
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2]


async def extract_time(msg, time_val):
    if any(time_val.endswith(unit) for unit in ('m', 'h', 'd')):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            await msg.reply("`Invalid time amount specified.`")
            return

        if unit == 'm':
            bantime = int(time.time() + int(time_num) * 60)
        elif unit == 'h':
            bantime = int(time.time() + int(time_num) * 60 * 60)
        elif unit == 'd':
            bantime = int(time.time() + int(time_num) * 24 * 60 * 60)
        else:
            await msg.reply("`Any other unit of time you know..?`")
            return
        return bantime
    else:
        await msg.reply("`Need time in format of m, h or d`")
        return


def is_admin(chat_id: int, user_id: int, check_devs: bool = False) -> bool:
    """ check user is admin or not in this chat """
    if check_devs and is_dev(user_id):
        return True
    if chat_id not in Config.ADMINS:
        return False
    return user_id in Config.ADMINS[chat_id]


def is_dev(user_id: int) -> bool:
    """ returns user is dev or not """
    return user_id in Config.DEV_USERS


def parse_about(about) -> str:
    if isinstance(about, str):
        return about
    tmp_chelp = ''
    if about.get('example') and isinstance(about['description'], str):
        tmp_chelp += ("\n\n📝 <u><b>Description</b></u> :\n\n    "
                      f"<i>{about['description']}</i>")
        del about['description']
    if about.get('flags'):
        tmp_chelp += "\n\n⛓ <u><b>Available Flags</b></u> :\n"
        if isinstance(about['flags'], dict):
            for f_n, f_d in about['flags'].items():
                tmp_chelp += f"\n    ▫ <code>{f_n}</code> : <i>{f_d.lower()}</i>"
        else:
            tmp_chelp += f"\n    {about['flags']}"
        del about['flags']
    if about.get('usage'):
        tmp_chelp += f"\n\n✒ <u><b>Usage</b></u> :"
        if isinstance(about['usage'], list):
            for us_ in about['usage']:
                tmp_chelp += f"\n\n    <code>{us_}</code>"
        else:
            tmp_chelp += "\n\n<code>{about['usage']}</code>"
        del about['usage']
    if about.get('examples'):
        tmp_chelp += "\n\n✏ <u><b>Examples</b></u> :"
        if isinstance(about['examples'], list):
            for ex_ in about['examples']:
                tmp_chelp += f"\n\n    <code>{ex_}</code>"
        else:
            tmp_chelp += f"\n\n    <code>{about['examples']}</code>"
        del about['examples']
    if about:
        for t_n, t_d in about.items():
            tmp_chelp += f"\n\n⚙ <u><b>{t_n.title()}</b></u> :\n"
            if isinstance(t_d, dict):
                for o_n, o_d in t_d.items():
                    tmp_chelp += f"\n    ▫ <code>{o_n}</code> : <i>{o_d.lower()}</i>"
            elif isinstance(t_d, list):
                tmp_chelp += '\n'
                for _opt in t_d:
                    tmp_chelp += f"    <code>{_opt}</code> ,"
            else:
                tmp_chelp += '\n'
                tmp_chelp += t_d
    return tmp_chelp


async def is_self(user_id: int) -> bool:
    """ returns user is assistant or not """
    global _BOT_ID  # pylint: disable=global-statement
    if not _BOT_ID:
        _BOT_ID = (await bot.get_me()).id
    return user_id == _BOT_ID


async def check_rights(chat_id: int, user_id: int, rights: str) -> bool:
    """ check admin rights """
    user = await bot.get_chat_member(chat_id, user_id)
    if user.status == "member":
        return False
    if user.status == "administrator":
        if getattr(user, rights, None):
            return True
        return False
    return False


async def check_bot_rights(chat_id: int, rights: str) -> bool:
    """ check bot rights """
    global _BOT_ID  # pylint: disable=global-statement
    if not _BOT_ID:
        _BOT_ID = (await bot.get_me()).id
    bot_ = await bot.get_chat_member(chat_id, _BOT_ID)
    if bot_.status == "administrator":
        if getattr(bot_, rights, None):
            return True
        return False
    return False


async def _is_spammer(chat_id: int, user_id: int, bio: str = None) -> bool:
    """ Manage new members Spambots """
    if not bio:
        bio = (await bot.get_chat(user_id)).bio
        if not bio:
            return False
    pattern = r"( |^|[^\w])@date4ubot( |$|[^\w])"
    if re.search(pattern, bio, re.IGNORECASE):
        await bot.kick_chat_member(chat_id, user_id)
        await bot.send_message(
            chat_id,
            r"\\ SpamBot Detected //"
            f"\n\n**USER ID:** {user_id}"
        )
        return True
    return False


async def sed_sticker(msg: Message):
    """ send default sticker """
    sticker = (await bot.get_messages('UserGeOt', 498697)).sticker.file_id
    await msg.reply_sticker(sticker)
