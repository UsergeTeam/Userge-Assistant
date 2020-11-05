# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery)

from assistant import bot, cus_filters


@bot.on_message(filters.command("repo") & cus_filters.auth_chats)
async def _rules(_, message: Message):
    replied = message.reply_to_message
    if replied:
        msg_id = replied.message_id
    else:
        msg_id = message.message_id
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Official Channel",
                    callback_data="official_channel"),
                InlineKeyboardButton(
                    text="Unofficial Help",
                    callback_data="unofficial_help")
            ],
            [
                InlineKeyboardButton(
                    text="Main Repo",
                    callback_data="main_repo"),
                InlineKeyboardButton(
                    text="Plugins Repo",
                    callback_data="plugins")
            ],
            [
                InlineKeyboardButton(
                    text="Tutorial",
                    callback_data="tutorial")
            ]
        ]
    )
    await bot.send_message(message.chat.id,
                           text=("**Welcome**\n"
                                 "__Check out our channels and Repo's 🤘__"),
                           reply_to_message_id=msg_id,
                           reply_markup=markup)


@bot.on_callback_query(filters.regex(pattern=r"^official_channel$"))
async def _channel_cq(_, c_q: CallbackQuery):
    await c_q.answer(url="https://t.me/TheUserGe")


@bot.on_callback_query(filters.regex(pattern=r"^unofficial_help$"))
async def _unofficial_cq(_, c_q: CallbackQuery):
    await c_q.answer(url="https://t.me/UnofficialPluginsHelp")


@bot.on_callback_query(filters.regex(pattern=r"^main_repo$"))
async def _main_repo_cq(_, c_q: CallbackQuery):
    await c_q.answer(url="https://github.com/UsergeTeam/UserGe")


@bot.on_callback_query(filters.regex(pattern=r"^plugins$"))
async def _plugins_cq(_, c_q: CallbackQuery):
    await c_q.answer(url="https://github.com/UsergeTeam/Userge-Plugins")


@bot.on_callback_query(filters.regex(pattern=r"^tutorial$"))
async def _tutorial_cq(_, c_q: CallbackQuery):
    await c_q.answer(url="https://t.me/usergeot/612003")
