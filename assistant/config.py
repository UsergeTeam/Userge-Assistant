# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__all__ = ["Config"]

import os

from dotenv import load_dotenv

if os.path.isfile("config.env"):
    load_dotenv("config.env")


class Config:
    """ assistant configs """
    APP_ID = int(os.environ.get("1383845", 0))
    API_HASH = os.environ.get("0e3d2c299cc3c5cc26c283cecd2eb97c")
    BOT_TOKEN = os.environ.get("1138227910:AAHRh2gfBE5eHdDJCpEhyvD0-jLjfNdiN7s")
    AUTH_CHATS = set([-1001266398622])  # @UserGeOt
    if os.environ.get("AUTH_CHATS"):
        AUTH_CHATS.update(map(int, os.environ.get("AUTH_CHATS").split()))
    WHITELIST_CHATS = set([-1001470978862])  # @UserGeSpam
    if os.environ.get("WHITELIST_CHATS"):
        WHITELIST_CHATS.update(map(int, os.environ.get("WHITELIST_CHATS").split()))
    DEV_USERS = (
        1131653685
    )
    ADMINS = {}
    MAX_MSG_LENGTH = 4096
