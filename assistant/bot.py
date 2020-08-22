# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import Client

from assistant import Config, logging

LOG = logging.getLogger(__name__)

bot = Client(
    "userge-assistant",
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins={'root': "assistant/plugins"}
)

LOG.info("assistant-bot initialized!")
