# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__commands__ = ["neko", "paste", "getpaste"]

import os

import aiohttp
from aiohttp import ClientResponseError, ServerTimeoutError, TooManyRedirects

from assistant import bot, Config, Message

DOGBIN_URL = "https://del.dog/"
NEKOBIN_URL = "https://nekobin.com/"


@bot.on_cmd("paste", about={
    'description': "Paste to Dogbin",
    'usage': "/paste [reply to message]"})
async def dogbin_paste(message: Message):
    """ pastes the text directly to dogbin  """
    cmd = len(message.text)
    msg = await message.reply("`Processing...`")
    text = None
    if message.text and cmd > 6:
        _, args = message.text.split(maxsplit=1)
        text = args
    replied = message.reply_to_message
    file_ext = '.txt'
    if not cmd > 6 and replied and replied.document and replied.document.file_size < 2 ** 20 * 10:
        file_ext = os.path.splitext(replied.document.file_name)[1]
        path = await replied.download("downloads/")
        with open(path, 'r') as d_f:
            text = d_f.read()
        os.remove(path)
    elif not cmd > 6 and replied and replied.text:
        text = replied.text
    if not text:
        await msg.edit("`input not found!`")
        return
    await msg.edit("`Pasting text...`")
    async with aiohttp.ClientSession() as ses:
        async with ses.post(DOGBIN_URL + "documents", data=text.encode('utf-8')) as resp:
            if resp.status == 200:
                response = await resp.json()
                key = response['key']
                final_url = DOGBIN_URL + key
                if response['isUrl']:
                    reply_text = (f"**Shortened** [URL]({final_url})\n"
                                  f"**Dogbin** [URL]({DOGBIN_URL}v/{key})")
                else:
                    reply_text = f"**Dogbin** [URL]({final_url}{file_ext})"
                await msg.edit(reply_text, disable_web_page_preview=True)
            else:
                await msg.edit("`Failed to reach Dogbin`")


@bot.on_cmd("neko", about={
    'description': "Paste to Nekobin",
    'usage': "/neko [reply to message]"})
async def nekobin_paste(message: Message):
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


@bot.on_cmd("getpaste", about={
    'description': "Get text from pasted urls.",
    'usage': "/getpaste [reply to message]"})
async def get_paste_(message: Message):
    """ fetches the content of a dogbin or nekobin URL """
    if message.text and len(message.text) == 9:
        await message.reply("`input not found!`")
        return
    _, args = message.text.split(maxsplit=1)
    link = args
    msg = await message.reply("`Getting paste content...`")
    format_view = f'{DOGBIN_URL}v/'
    if link.startswith(format_view):
        link = link[len(format_view):]
        raw_link = f'{DOGBIN_URL}raw/{link}'
    elif link.startswith(DOGBIN_URL):
        link = link[len(DOGBIN_URL):]
        raw_link = f'{DOGBIN_URL}raw/{link}'
    elif link.startswith("del.dog/"):
        link = link[len("del.dog/"):]
        raw_link = f'{DOGBIN_URL}raw/{link}'
    elif link.startswith(NEKOBIN_URL):
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
