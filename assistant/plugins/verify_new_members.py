# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

import asyncio

from pyrogram import filters
from pyrogram.types import (
    Message, ChatPermissions, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton)

from assistant import bot, cus_filters
from assistant.utils import check_bot_rights


@bot.on_message(
    filters.group & filters.new_chat_members & cus_filters.auth_chats)
async def _verify_msg_(_, msg: Message):
    """ Verify Msg for New chat Members """
    chat_id = msg.chat.id
    for member in msg.new_chat_members:
        if member.is_bot or not await check_bot_rights(chat_id, "can_restrict_members"):
            file_id, file_ref, text, buttons = await wc_msg(member)
            reply = await msg.reply_animation(
                animation=file_id, file_ref=file_ref,
                caption=text, reply_markup=buttons
            )
            await asyncio.sleep(120)
            await reply.delete()
        else:
            await bot.restrict_chat_member(chat_id, member.id, ChatPermissions())
            await verify_keyboard(msg, member)
    msg.continue_propagation()


async def verify_keyboard(msg: Message, user):
    """ keyboard for verifying """
    _msg = f""" Hi {user.mention}, Welcome to {msg.chat.title}.
To Chat here, Please click on the button below. """
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Verify now 🤖",
                    callback_data=f"verify_cq({user.id} {msg.message_id})")
            ]
        ]
    )
    await msg.reply_text(_msg, reply_markup=button)


async def wc_msg(user):
    """ arguments and reply_markup for sending after verify """
    gif = await bot.get_messages("UserGeOt", 510608)
    file_id = gif.animation.file_id
    file_ref = gif.animation.file_ref
    text = f""" **Welcome** {user.mention},
__Check out the Button below. and feel free to ask here.__ 🤘 """
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="More info.",
                    url="https://t.me/usergeot/527524"
                )
            ]
        ]
    )
    return file_id, file_ref, text, buttons


@bot.on_callback_query(filters.regex(pattern=r"verify_cq\((.+?)\)"))
async def _verify_user_(_, c_q: CallbackQuery):
    _a, _b = c_q.matches[0].group(1).split(' ', maxsplit=1)
    user_id = int(_a)
    msg_id = int(_b)
    if c_q.from_user.id == user_id:
        await c_q.message.delete()
        await bot.restrict_chat_member(
            c_q.message.chat.id, user_id,
            ChatPermissions(
                can_send_messages=c_q.message.chat.permissions.can_send_messages,
                can_send_media_messages=c_q.message.chat.permissions.can_send_media_messages,
                can_send_stickers=c_q.message.chat.permissions.can_send_stickers,
                can_send_animations=c_q.message.chat.permissions.can_send_animations,
                can_send_games=c_q.message.chat.permissions.can_send_games,
                can_use_inline_bots=c_q.message.chat.permissions.can_use_inline_bots,
                can_add_web_page_previews=c_q.message.chat.permissions.can_add_web_page_previews,
                can_send_polls=c_q.message.chat.permissions.can_send_polls,
                can_change_info=c_q.message.chat.permissions.can_change_info,
                can_invite_users=c_q.message.chat.permissions.can_invite_users,
                can_pin_messages=c_q.message.chat.permissions.can_pin_messages))
        file_id, file_ref, text, buttons = await wc_msg(await bot.get_users(user_id))
        msg = await bot.send_animation(
            c_q.message.chat.id,
            animation=file_id,
            file_ref=file_ref,
            caption=text, reply_markup=buttons,
            reply_to_message_id=msg_id
        )
        await asyncio.sleep(120)
        await msg.delete()
    else:
        await c_q.answer("This message is not for you. 😐", show_alert=True)
