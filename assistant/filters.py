# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__all__ = ["auth_chats", "is_admin"]

import asyncio

from pyrogram import Filters, Message

from . import Config, logging

_LOG = logging.getLogger(__name__)
_FETCHING = False


async def _is_admin(_, msg: Message) -> bool:
    global _FETCHING
    if msg.chat.type not in ("supergroup", "channel"):
        return False
    if msg.chat.id not in Config.AUTH_CHATS:
        return False
    if not msg.from_user:
        return False
    while _FETCHING:
        _LOG.info("waiting for fetching task ... sleeping (5s) !")
        await asyncio.sleep(5)
    if msg.chat.id not in Config.ADMINS:
        _FETCHING = True
        admins = []
        _LOG.info(f"fetching data from [{msg.chat.id}] ...")
        async for c_m in msg._client.iter_chat_members(msg.chat.id):
            if c_m.status in ("creator", "administrator"):
                admins.append(c_m.user.id)
        Config.ADMINS[msg.chat.id] = tuple(admins)
        _LOG.info(f"data fetched from [{msg.chat.id}] !")
        del admins
        _FETCHING = False
    return msg.from_user.id in (Config.ADMINS[msg.chat.id] or Config.DEV_USERS)


auth_chats = Filters.chat(list(Config.AUTH_CHATS)) 
is_admin = Filters.create(_is_admin)
