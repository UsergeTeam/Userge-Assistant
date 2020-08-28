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


@bot.on_message(filters.command("id") & cus_filters.auth_chats)
async def _id(_, message: Message):
    msg = message.reply_to_message or message
    out_str = f"👥 **Chat ID** : `{(msg.forward_from_chat or msg.chat).id}`\n"
    out_str += f"💬 **Message ID** : `{msg.forward_from_message_id or msg.message_id}`\n"
    if msg.from_user:
        out_str += f"🙋‍♂️ **From User ID** : `{msg.from_user.id}`\n"
    file_id, file_ref = None, None
    if msg.audio:
        type_ = "audio"
        file_id = msg.audio.file_id
        file_ref = msg.audio.file_ref
    elif msg.animation:
        type_ = "animation"
        file_id = msg.animation.file_id
        file_ref = msg.animation.file_ref
    elif msg.document:
        type_ = "document"
        file_id = msg.document.file_id
        file_ref = msg.document.file_ref
    elif msg.photo:
        type_ = "photo"
        file_id = msg.photo.file_id
        file_ref = msg.photo.file_ref
    elif msg.sticker:
        type_ = "sticker"
        file_id = msg.sticker.file_id
        file_ref = msg.sticker.file_ref
    elif msg.voice:
        type_ = "voice"
        file_id = msg.voice.file_id
        file_ref = msg.voice.file_ref
    elif msg.video_note:
        type_ = "video_note"
        file_id = msg.video_note.file_id
        file_ref = msg.video_note.file_ref
    elif msg.video:
        type_ = "video"
        file_id = msg.video.file_id
        file_ref = msg.video.file_ref
    if (file_id and file_ref) is not None:
        out_str += f"● **Type:** `{type_}`\n"
        out_str += f"📄 **File ID:** `{file_id}`\n"
        out_str += f"📄 **File REF:** `{file_ref}`"
    await message.reply(out_str)
