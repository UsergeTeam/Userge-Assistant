# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__all__ = ["auth_chats", "auth_users", "whitelist_chats"]

import asyncio

from pyrogram import filters, Client
from pyrogram.types import Message

from . import Config, logging

_LOG = logging.getLogger(__name__)
_FETCHING = False


async def _is_admin_or_dev(_, bot: Client, msg: Message) -> bool:
    global _FETCHING  # pylint: disable=global-statement
    if msg.chat.id not in Config.AUTH_CHATS:
        return False
    if not msg.from_user:
        return False
    if msg.from_user.id in Config.DEV_USERS:
        return True
    while _FETCHING:
        _LOG.info("waiting for fetching task ... sleeping (5s) !")
        await asyncio.sleep(5)
    if msg.chat.id not in Config.ADMINS:
        _FETCHING = True
        admins = []
        _LOG.info("fetching data from [%s] ...", msg.chat.id)
        # pylint: disable=protected-access
        async for c_m in bot.iter_chat_members(msg.chat.id):
            if c_m.status in ("creator", "administrator"):
                admins.append(c_m.user.id)
        Config.ADMINS[msg.chat.id] = tuple(admins)
        _LOG.info("data fetched from [%s] !", msg.chat.id)
        del admins
        _FETCHING = False
    return msg.from_user.id in Config.ADMINS[msg.chat.id]


async def _is_chat_whitelist(_, __, msg: Message) -> bool:
    if msg.chat.id in Config.WHITELIST_CHATS:
        return True
    return False


auth_chats = filters.chat(list(Config.AUTH_CHATS))
auth_users = filters.create(_is_admin_or_dev)
whitelist_chats = filters.create(_is_chat_whitelist)
