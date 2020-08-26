# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

import time
import asyncio

from pyrogram import Message, Filters, ChatPermissions
from pyrogram.errors import (
    FloodWait, UserAdminInvalid, UsernameInvalid, PeerIdInvalid, UserIdInvalid)

from assistant import bot, filters
from assistant.utils import is_dev, is_admin, sed, check_rights


@bot.on_message(  # tban in queue
    Filters.command("ban") & filters.auth_chats & filters.auth_users)
async def ban_user(_, msg: Message):
    chat_id = msg.chat.id
    if not check_rights(chat_id, msg.from_user.id, "can_restrict_members"):
        return
    cmd = len(msg.text)
    replied = msg.reply_to_message
    if replied:
        id = replied.from_user.id
        if not (msg.text and cmd > 4):
            await msg.reply("`Give a reason to Ban him.`")
            return
        _, reason = msg.text.split(maxsplit=1)
    else:
        if msg.text and cmd > 4:
            _, args = msg.text.split(maxsplit=1)
            try:
                id, reason = args.split(' ', maxsplit=1)
            except Exception:
                await msg.reply("**Syntax:** /ban user_id reason")
                return
        else:
            await msg.reply("`No valid User_id or message specified.`")
            return
    try:
        user = await bot.get_users(id)
        user_id = user.id
        mention = user.mention
    except (UsernameInvalid, PeerIdInvalid, UserIdInvalid):
        await msg.reply("`Invalid user_id or username, try again with valid info ⚠`")
        return
    if is_dev(user_id):
        await msg.reply("`He is My Master, I will not Ban him.`")
        return
    if user_id == (await bot.get_me()).id:
        await sed(msg)
        return
    if is_admin(chat_id, user_id):
        await msg.reply("`User is Admin, Can't Ban him.`")
        return
    if not check_rights(chat_id, (await bot.get_me()).id, "can_restrict_members"):
        await msg.reply("`Give me rights to Ban Users.`")
        return
    text = await msg.reply("`Trying to Ban User.. Hang on!! ⏳`")
    try:
        await bot.kick_chat_member(chat_id, user_id)
        await text.edit(
            f"#BAN\n"
            f"USER: {mention}\n"
            f"REASON: `{reason}`")
    except Exception as e_f:
        await text.edit(f"`Something went wrong! 🤔`\n\n**ERROR:** `{e_f}`")


@bot.on_message(
    Filters.command("unban") & filters.auth_chats & filters.auth_users)
async def unban_user(_, msg: Message):
    chat_id = msg.chat.id
    if not check_rights(chat_id, msg.from_user.id, "can_restrict_members"):
        return
    replied = msg.reply_to_message
    if replied:
        id = replied.from_user.id
    else:
        if msg.text and len(msg.text) > 6:
            _, id = msg.text.split(maxsplit=1)
        else:
            await msg.reply("`No valid User_id or message specified.`")
            return
    try:
        user_id = (await bot.get_users(id)).id
    except (UsernameInvalid, PeerIdInvalid, UserIdInvalid):
        await msg.reply("`Invalid user_id or username, try again with valid info ⚠`")
        return
    if user_id == (await bot.get_me()).id:
        return
    if is_admin(chat_id, user_id):
        await msg.reply("`User is Admin.`")
        return
    if not check_rights(chat_id, (await bot.get_me()).id, "can_restrict_members"):
        await msg.reply("`Give me rights to UnBan Users.`")
        return
    text = await msg.reply("`Trying to UnBan User.. Hang on!! ⏳`")
    try:
        await bot.unban_chat_member(chat_id, user_id)
        await text.edit("`🛡Unbanned Successfully...`")
    except Exception as e_f:
        await text.edit(f"`Something went wrong! 🤔`\n\n**ERROR:** `{e_f}`")


@bot.on_message(
    Filters.command("kick") & filters.auth_chats & filters.auth_users)
async def kick_user(_, msg: Message):
    chat_id = msg.chat.id
    if not check_rights(chat_id, msg.from_user.id, "can_restrict_members"):
        return
    cmd = len(msg.text)
    replied = msg.reply_to_message
    if replied:
        id = replied.from_user.id
        if not (msg.text and cmd > 5):
            await msg.reply("`Give a reason to Ban him.`")
            return
        _, reason = msg.text.split(maxsplit=1)
    else:
        if msg.text and cmd > 5:
            _, args = msg.text.split(maxsplit=1)
            try:
                id, reason = args.split(' ', maxsplit=1)
            except Exception:
                await msg.reply("**Syntax:** /kick user_id reason")
                return
        else:
            await msg.reply("`No valid User_id or message specified.`")
            return
    try:
        user = await bot.get_users(id)
        user_id = user.id
        mention = user.mention
    except (UsernameInvalid, PeerIdInvalid, UserIdInvalid):
        await msg.reply("`Invalid user_id or username, try again with valid info ⚠`")
        return
    if is_dev(user_id):
        await msg.reply("`He is My Master, I will not Kick him.`")
        return
    if user_id == (await bot.get_me()).id:
        await sed(msg)
        return
    if is_admin(chat_id, user_id):
        await msg.reply("`User is Admin, Can't Kick him.`")
        return
    if not check_rights(chat_id, (await bot.get_me()).id, "can_restrict_members"):
        await msg.reply("`Give me rights to Kick Users.`")
        return
    text = await msg.reply("`Trying to Kick User.. Hang on!! ⏳`")
    try:
        await bot.kick_chat_member(chat_id, user_id)
        await text.edit(
            f"#KICK\n"
            f"USER: {mention}\n"
            f"REASON: `{reason}`")
    except Exception as e_f:
        await text.edit(f"`Something went wrong! 🤔`\n\n**ERROR:** `{e_f}`")


@bot.on_message(
    Filters.command("promote") & filters.auth_chats & filters.auth_users)
async def promote_user(_, msg: Message):
    chat_id = msg.chat.id
    if not check_rights(chat_id, msg.from_user.id, "can_promote_members"):
        return
    replied = msg.reply_to_message
    if replied:
        id = replied.from_user.id
    else:
        if msg.text and len(msg.text) > 8:
            _, id = msg.text.split(maxsplit=1)
        else:
            await msg.reply("`No valid User_id or message specified.`")
            return
    try:
        user_id = (await bot.get_users(id)).id
    except (UsernameInvalid, PeerIdInvalid, UserIdInvalid):
        await msg.reply("`Invalid user_id or username, try again with valid info ⚠`")
        return
    if user_id == (await bot.get_me()).id:
        return
    if is_admin(chat_id, user_id):
        await msg.reply("`User is Already Promoted`")
        return
    if not check_rights(chat_id, (await bot.get_me()).id, "can_promote_members"):
        await msg.reply("`Give me rights to Promote User.`")
        return
    text = await msg.reply("`Trying to Promote User.. Hang on!! ⏳`")
    try:
        await bot.promote_chat_member(chat_id, user_id,
                                      can_change_info=True,
                                      can_delete_messages=True,
                                      can_restrict_members=True,
                                      can_invite_users=True,
                                      can_pin_messages=True)
        await text.edit("`👑 Promoted Successfully..`")
    except Exception as e_f:
        await text.edit(f"`Something went wrong! 🤔`\n\n**ERROR:** `{e_f}`")


@bot.on_message(
    Filters.command("demote") & filters.auth_chats & filters.auth_users)
async def demote_user(_, msg: Message):
    chat_id = msg.chat.id
    if not check_rights(chat_id, msg.from_user.id, "can_promote_members"):
        return
    replied = msg.reply_to_message
    if replied:
        id = replied.from_user.id
    else:
        if msg.text and len(msg.text) > 7:
            _, id = msg.text.split(maxsplit=1)
        else:
            await msg.reply("`No valid User_id or message specified.`")
            return
    try:
        user_id = (await bot.get_users(id)).id
    except (UsernameInvalid, PeerIdInvalid, UserIdInvalid):
        await msg.reply("`Invalid user_id or username, try again with valid info ⚠`")
        return
    if user_id == (await bot.get_me()).id:
        await sed(msg)
        return
    if is_dev(user_id):
        return
    if not is_admin(chat_id, user_id):
        await msg.reply("`Cant demote a Demoted User`")
        return
    if not check_rights(chat_id, (await bot.get_me()).id, "can_promote_members"):
        await msg.reply("`Give me rights to Demote User.`")
        return
    text = await msg.reply("`Trying to Demote User.. Hang on!! ⏳`")
    try:
        await bot.promote_chat_member(chat_id, user_id,
                                      can_change_info=False,
                                      can_delete_messages=False,
                                      can_restrict_members=False,
                                      can_invite_users=False,
                                      can_pin_messages=False)
        await text.edit("`🛡 Demoted Successfully..`")
    except Exception as e_f:
        await text.edit(f"`Something went wrong! 🤔`\n\n**ERROR:** `{e_f}`")


@bot.on_message(  # tmute in queue
    Filters.command("mute") & filters.auth_chats & filters.auth_users)
async def mute_user(_, msg: Message):
    chat_id = msg.chat.id
    if not check_rights(chat_id, msg.from_user.id, "can_restrict_members"):
        return
    cmd = len(msg.text)
    replied = msg.reply_to_message
    if replied:
        id = replied.from_user.id
        if not (msg.text and cmd > 5):
            await msg.reply("`Give a reason to Mute him.`")
            return
        _, reason = msg.text.split(maxsplit=1)
    else:
        if msg.text and cmd > 5:
            _, args = msg.text.split(maxsplit=1)
            try:
                id, reason = args.split(' ', maxsplit=1)
            except Exception:
                await msg.reply("**Syntax:** /mute user_id reason")
                return
        else:
            await msg.reply("`No valid User_id or message specified.`")
            return
    try:
        user = await bot.get_users(id)
        user_id = user.id
        mention = user.mention
    except (UsernameInvalid, PeerIdInvalid, UserIdInvalid):
        await msg.reply("`Invalid user_id or username, try again with valid info ⚠`")
        return
    if is_dev(user_id):
        await msg.reply("`He is My Master, I will not Mute him.`")
        return
    if user_id == (await bot.get_me()).id:
        await sed(msg)
        return
    if is_admin(chat_id, user_id):
        await msg.reply("`User is Admin, Can't Mute him.`")
        return
    if not check_rights(chat_id, (await bot.get_me()).id, "can_restrict_members"):
        await msg.reply("`Give me rights to Mute Users.`")
        return
    text = await msg.reply("`Trying to Mute User.. Hang on!! ⏳`")
    try:
        await bot.restrict_chat_member(chat_id, user_id, ChatPermissions())
        await asyncio.sleep(1)
        await text.edit(
            f"#MUTE\n"
            f"USER: {mention}\n"
            f"TIME: `Forever`\n"
            f"REASON: `{reason}`")
    except Exception as e_f:
        await text.edit(f"`Something went wrong 🤔`\n\n**ERROR**: `{e_f}`")


@bot.on_message(
    Filters.command("unmute") & filters.auth_chats & filters.auth_users)
async def unmute_user(_, msg: Message):
    chat_id = msg.chat.id
    if not check_rights(chat_id, msg.from_user.id, "can_restrict_members"):
        return
    replied = msg.reply_to_message
    if replied:
        id = replied.from_user.id
    else:
        if msg.text and len(msg.text) > 7:
            _, id = msg.text.split(maxsplit=1)
        else:
            await msg.reply("`No valid User_id or message specified.`")
            return
    try:
        user_id = (await bot.get_users(id)).id
    except (UsernameInvalid, PeerIdInvalid, UserIdInvalid):
        await msg.reply("`Invalid user_id or username, try again with valid info ⚠`")
        return
    if user_id == (await bot.get_me()).id:
        return
    if is_admin(chat_id, user_id):
        await msg.reply("`User is Admin.`")
        return
    if not check_rights(chat_id, (await bot.get_me()).id, "can_restrict_members"):
        await msg.reply("`Give me rights to UnMute Users.`")
        return
    text = await msg.reply("`Trying to UnMute User.. Hang on!! ⏳`")
    try:
        await bot.restrict_chat_member(chat_id, user_id,
            ChatPermissions(
                can_send_messages=msg.chat.permissions.can_send_messages,
                can_send_media_messages=msg.chat.permissions.can_send_media_messages,
                can_send_stickers=msg.chat.permissions.can_send_stickers,
                can_send_animations=msg.chat.permissions.can_send_animations,
                can_send_games=msg.chat.permissions.can_send_games,
                can_use_inline_bots=msg.chat.permissions.can_use_inline_bots,
                can_add_web_page_previews=msg.chat.permissions.can_add_web_page_previews,
                can_send_polls=msg.chat.permissions.can_send_polls,
                can_change_info=msg.chat.permissions.can_change_info,
                can_invite_users=msg.chat.permissions.can_invite_users,
                can_pin_messages=msg.chat.permissions.can_pin_messages))
        await text.edit("`🛡 Successfully Unmuted..`")
    except Exception as e_f:
        await text.edit(f"`Something went wrong!` 🤔\n\n**ERROR:** `{e_f}`")


@bot.on_message(
    Filters.command("zombies") & filters.auth_chats & filters.auth_users)
async def zombie_clean(msg: Message):
    chat_id = msg.chat.id
    if "clean" in msg.text.lower():
        del_users = 0
        del_admins = 0
        del_total = 0
        del_stats = r"`Zero zombie accounts found in this chat... WOOHOO group is clean.. \^o^/`"
        if check_rights(chat_id, (await bot.get_me()).id, "can_restrict_members"):
            text = await msg.reply("`Hang on!! cleaning zombie accounts from this chat..`")
            async for member in bot.iter_chat_members(chat_id):
                if member.user.is_deleted:
                    try:
                        await bot.kick_chat_member(
                            chat_id, member.user.id, int(time.time() + 45))
                    except UserAdminInvalid:
                        del_users -= 1
                        del_admins += 1
                    except FloodWait as e_f:
                        time.sleep(e_f.x)
                    del_users += 1
                    del_total += 1
            if del_admins > 0:
                del_stats = f"`👻 Found` **{del_total}** `total zombies..`\
                \n`🗑 Cleaned` **{del_users}** `zombie (deleted) accounts from this chat..`\
                \n🛡 **{del_admins}** `deleted admin accounts are skipped!!`"
            else:
                del_stats = f"`👻 Found` **{del_total}** `total zombies..`\
                \n`🗑 Cleaned` **{del_users}** `zombie (deleted) accounts from this chat..`"
            await text.edit(f"{del_stats}")
        else:
            await msg.reply("`Give me rights to clean Zombies from this group.`")
    else:
        del_users = 0
        del_stats = r"`Zero zombie accounts found in this chat... WOOHOO group is clean.. \^o^/`"
        text = await msg.reply("`🔎 Searching for zombie accounts in this chat..`")
        async for member in bot.iter_chat_members(chat_id):
            if member.user.is_deleted:
                del_users += 1
        if del_users > 0:
            del_stats = f"`Found` **{del_users}** `zombie accounts in this chat.`"
            await text.edit(
                f"🕵️‍♂️ {del_stats} `you can clean them using .zombies -c`")
        else:
            await text.edit(f"{del_stats}")


@bot.on_message(
    Filters.command("pin") & filters.auth_chats & filters.auth_users)
async def pin_(msg: Message):
    chat_id = msg.chat.id
    if not check_rights(chat_id, msg.from_user.id, "can_pin_messages"):
        return
    if not check_rights(chat_id, (await bot.get_me()).id, "can_pin_messages"):
        await msg.reply("`Give me Rights to Pin Msgs.`")
        return
    msg_id = msg.reply_to_message.message_id
    if not msg_id:
        await msg.reply("`Reply Msg to Pin.`")
        return
    if "silent" in msg.text.lower():
        try:
            await bot.pin_chat_message(
                chat_id, msg_id, disable_notification=True)
        except Exception as e_f:
            await msg.reply(f"`Something went wrong! 🤔`\n\n**ERROR:** `{e_f}`")
    else:
        try:
            await bot.pin_chat_message(chat_id, msg_id)
        except Exception as e_f:
            await msg.reply(f"`Something went wrong! 🤔`\n\n**ERROR:** `{e_f}`")


@bot.on_message(
    Filters.command("unpin") & filters.auth_chats & filters.auth_users)
async def unpin_(msg: Message):
    chat_id = msg.chat.id
    if not check_rights(chat_id, msg.from_user.id, "can_pin_messages"):
        return
    if not check_rights(chat_id, (await bot.get_me()).id, "can_pin_messages"):
        await msg.reply("`Give me Rights to UnPin Msgs.`")
        return
    try:
        await bot.unpin_chat_message(chat_id)
    except Exception as e_f:
        await msg.reply(f"`Something went wrong! 🤔`\n\n**ERROR:** `{e_f}`")
