# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import Message

from assistant import bot, cus_filters


@bot.on_message(
    filters.command("logs") & cus_filters.auth_chats & cus_filters.auth_users)
async def _logs(_, msg: Message):
    k = await msg.reply("Checking logs...")
    with open("logs/assistant.log", 'r') as d_f:
            text = d_f.read()
    async with aiohttp.ClientSession() as ses:
        async with ses.post(
            "https://nekobin.com/" + "api/documents", json={"content": text}) as resp:
            if resp.status == 201:
                response = await resp.json()
                url = "https://nekobin.com/" + response['result']['key'] + ".txt"
                await k.edit(f"[My logs]({url})", disable_web_page_preview=True)
            else:
                await msg.reply_document("logs/assistant.log")
                await k.delete()
