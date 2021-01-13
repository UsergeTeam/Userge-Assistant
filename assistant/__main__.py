# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.
    
import os
import importlib

from assistant import bot, Config, DB, logging

_LOG = logging.getLogger(__name__)
msg = None


async def _init():
    global msg  # pylint: disable=global-statement
    if len(Config.PLUGINS_ID) > 0:
        msg = await bot.get_messages(DB.CHANNEL_ID, Config.PLUGINS_ID)


if __name__ == "__main__":
    bot.run()

    if msg and len(Config.PLUGINS_ID) > 0:
        _LOG.info("Loading Temp PLugins...")
        plg_list = []
        
        for i in len(Config.PLUGINS_ID):
            file = msg[i]
            document = file.document
            if file and document:
                if document.file_name.endswith('.py') and document.file_size < 2 ** 20:
                    path = "Userge-Assistant/assistant/plugins/"
                    if not os.path.isdir(path):
                        os.makedirs(path)
                    t_path = path + document.file_name
                    if os.path.isfile(t_path):
                        os.remove(t_path)
                    await file.download(file_name=t_path)
                    plugin = '.'.join(t_path.split('/'))[:-3]
                    try:
                        load_plugin(plugin)
                    except Exception:
                        os.remove(t_path)
                    else:
                        plg_list.append(document.file_name[:-3])
        _LOG.info(f"Loaded Plugins: {plg_list}")


def load_plugin(name: str):
    try:
        importlib.import_module(name)
    except ImportError as i_e:
        _LOG.error(i_e)
        raise
