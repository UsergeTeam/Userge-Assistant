# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__commands__ = ["help"]

from assistant import bot, Message


# TODO buttons for help 
@bot.on_cmd("help", about={
    'description': "Check help of a module",
    'usage': ["/help", "/help [plugin_name]", "/help [command_name]"]
})
async def _help(msg: Message):
    cmd = msg.text
    if msg.text and cmd == 5:
        plugins = bot.get_help()
        out_str = f"""⚒ <b><u>(<code>{len(plugins)}</code>) Plugin(s) Available</u></b>
        
**Usage**:

    `/help [plugin_name]`

**Available Modules:**\n\n"""
        for i in sorted(plugins):
            out_str += f"`{i}`   "
        await msg.reply(out_str)
        return
    _, _name = msg.text.split(maxsplit=1)
    if not _name.startswith('/'):
        commands = bot.get_help(_name)
        if not commands:
            return await msg.reply(f"__No Plugin Found!__: `{_name}`")
        out_str = f"""⚒ <b><u>(<code>{len(commands)}</code>) Cmd(s) Available</u></b>
        
**Usage**:

    `/help /[command_name]`

**Available Commands:**\n\n"""
        for i in sorted(commands):
            out_str += f"`/{i}`   "
        await msg.reply(out_str)
    else:
        help = bot.get_help(_name)
        if not help:
            return await msg.reply(f"__No Command Found!__: `{_name}`")
        await msg.reply(help)
