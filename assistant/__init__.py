# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters  # noqa
from pyrogram.types import Message  # noqa
from .logger import logging  # noqa
from .config import Config  # noqa
from assistant.core import Bot, START_TIME  # noqa
from . import cus_filters  # noqa

bot = Bot()  # bot is the client name