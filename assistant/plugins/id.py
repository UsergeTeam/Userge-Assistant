# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__commands__ = ["id"]

from assistant import bot, Message


@bot.on_cmd("id", about={
    'description': "Check Ids",
    'usage': "/id\n/id [reply to message]"})
async def _id(message: Message):
    msg = message.reply_to_message or message
    out_str = f"👥 **Chat ID** : `{(msg.forward_from_chat or msg.chat).id}`\n"
    out_str += f"💬 **Message ID** : `{msg.forward_from_message_id or msg.message_id}`\n"
    if msg.from_user:
        out_str += f"🙋‍♂️ **From User ID** : `{msg.from_user.id}`\n"
    file_id, file_unique_id = None, None
    if msg.audio:
        type_ = "audio"
        file_id = msg.audio.file_id
        file_unique_id = msg.audio.file_unique_id
    elif msg.animation:
        type_ = "animation"
        file_id = msg.animation.file_id
        file_unique_id = msg.animation.file_unique_id
    elif msg.document:
        type_ = "document"
        file_id = msg.document.file_id
        file_unique_id = msg.document.file_unique_id
    elif msg.photo:
        type_ = "photo"
        file_id = msg.photo.file_id
        file_unique_id = msg.photo.file_unique_id
    elif msg.sticker:
        type_ = "sticker"
        file_id = msg.sticker.file_id
        file_unique_id = msg.sticker.file_unique_id
    elif msg.voice:
        type_ = "voice"
        file_id = msg.voice.file_id
        file_unique_id = msg.voice.file_unique_id
    elif msg.video_note:
        type_ = "video_note"
        file_id = msg.video_note.file_id
        file_unique_id = msg.video_note.file_unique_id
    elif msg.video:
        type_ = "video"
        file_id = msg.video.file_id
        file_unique_id = msg.video.file_unique_id
    if (file_id and file_unique_id) is not None:
        out_str += f"● **Type:** `{type_}`\n"
        out_str += f"📄 **File ID:** `{file_id}`\n"
        out_str += f"📄 **File UNIQUE ID:** `{file_unique_id}`"
    await message.reply(out_str)
