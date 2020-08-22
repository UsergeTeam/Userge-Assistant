# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

import os

from pyrogram import Filters
from dotenv import load_dotenv

if os.path.isfile("config.env"):
    load_dotenv("config.env")


class Config:
    APP_ID = int(os.environ.get("APP_ID", 0))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    AUTH_CHATS = Filters.chat(list(set(map(int, os.environ.get("AUTH_CHATS", "123").split()))))
