# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

import os

import aiohttp
from aiohttp import ClientResponseError, ServerTimeoutError, TooManyRedirects
from assistant import Config, bot, cus_filters
from pyrogram import filters
from pyrogram.types import Message

NEKOBIN_URL = "https://nekobin.com/"

@bot.on_message(filters.command("paste") & cus_filters.auth_chats)
async def nekobin_paste(_, message: Message):
    """ pastes the text directly to nekobin  """
    cmd = len(message.text)
    msg = await message.reply("`Processing...`")
    text = None
    if message.text and cmd > 5:
        _, args = message.text.split(maxsplit=1)
        text = args
    replied = message.reply_to_message
    file_ext = '.txt'
    if not cmd > 5 and replied and replied.document and replied.document.file_size < 2 ** 20 * 10:
        file_ext = os.path.splitext(replied.document.file_name)[1]
        path = await replied.download("downloads/")
        with open(path, 'r') as d_f:
            text = d_f.read()
        os.remove(path)
    elif not cmd > 5 and replied and replied.text:
        text = replied.text
    if not text:
        await msg.edit("`input not found!`")
        return
    await msg.edit("`Pasting text...`")
    async with aiohttp.ClientSession() as ses:
        async with ses.post(NEKOBIN_URL + "api/documents", json={"content": text}) as resp:
            if resp.status == 201:
                response = await resp.json()
                key = response['result']['key']
                final_url = NEKOBIN_URL + key + file_ext
                reply_text = f"**Nekobin** [URL]({final_url})"
                await msg.edit(reply_text, disable_web_page_preview=True)
            else:
                await msg.edit("`Failed to reach Nekobin`")


@bot.on_message(filters.command("getpaste") & cus_filters.auth_chats)
async def get_paste_(_, message: Message):
    """ fetches the content of a Nekobin URL """
    if message.text and len(message.text) == 9:
        await message.reply("`input not found!`")
        return
    _, args = message.text.split(maxsplit=1)
    link = args
    msg = await message.reply("`Getting paste content...`")
    if link.startswith(NEKOBIN_URL):
        link = link[len(NEKOBIN_URL):]
        raw_link = f'{NEKOBIN_URL}raw/{link}'
    elif link.startswith("nekobin.com/"):
        link = link[len("nekobin.com/"):]
        raw_link = f'{NEKOBIN_URL}raw/{link}'
    else:
        await msg.edit("`Is that even a paste url?`")
        return
    async with aiohttp.ClientSession(raise_for_status=True) as ses:
        try:
            async with ses.get(raw_link) as resp:
                text = await resp.text()
        except ServerTimeoutError as e_r:
            await msg.edit(f"`Request timed out -> {e_r}`")
        except TooManyRedirects as e_r:
            await msg.edit("`Request exceeded the configured `"
                           f"`number of maximum redirections -> {e_r}`")
        except ClientResponseError as e_r:
            await msg.edit(f"`Request returned an unsuccessful status code -> {e_r}`")
        else:
            if len(text) > Config.MAX_MSG_LENGTH:
                await msg.edit("`Content Too Large...`")
            else:
                await msg.edit("--Fetched Content Successfully!--"
                               f"\n\n**Content** :\n`{text}`")
