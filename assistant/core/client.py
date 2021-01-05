# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__all__ = ["Bot", "START_TIME"]

import os
import glob
import time
import importlib
from typing import Dict, List, Union, Optional

from pyrogram import Client, filters

from assistant import Config, logging, cus_filters
from assistant.utils.tools import parse_about

_LOG = logging.getLogger(__name__)
_LOG_STR = "<<<!  #####  %s  #####  !>>>"

START_TIME = time.time()


class Bot(Client):

    def __init__(self):

        super().__init__(
            session_name=":memory:",
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins={'root': "assistant.plugins"}
        )
        self.ALL_MODULES: Dict[str, List[str]] = {}
        self.CMDS_HELP: Dict[str, str] = {}
        self._get_all_plugins()

    def on_cmd(
        self,
        cmd: str,
        about: Union[str, Dict[str, Union[str, List[str], Dict[str, str]]]],
        admin_only: bool = False
    ):

        p_about = parse_about(about)
        self.__add_help(cmd, p_about)

        def decorator(func):
            _filters = filters.command(commands=cmd, prefixes='/') & cus_filters.auth_chats
            if admin_only:
                _filters = _filters & cus_filters.auth_users
            dec = self.on_message(filters=filters)
            return dec(func)
        return decorator
    
    def on_filters(
        self,
        filters,
        group: int = 0
    ):
        def decorator(func):
            dec = self.on_message(filters=filters, group=group)
            return dec(func)
        return decorator

    def __add_help(
        self,
        cmd: str,
        about: Union[str, Dict[str, Union[str, List[str], Dict[str, str]]]]
    ) -> None:
        self.CMDS_HELP.update({cmd: about})

    def get_help(self, key: str = None) -> Optional[List[str]]:
        if key:
            if key.startswith('/'):
                if not self.CMDS_HELP.get(key.lstrip('/')):
                    return None
                return self.CMDS_HELP[key.lstrip('/')]
            if not self.ALL_MODULES.get(key):
                return None
            return self.ALL_MODULES[key]
        return [x for x in self.ALL_MODULES]
    
    def _get_all_plugins(self) -> None:
        all_paths = sorted(glob.glob("/app/assistant/plugins/*.py"))
        plugins = [os.path.basename(f)[:-3] for f in all_paths if os.path.isfile(f) and f.endswith(
            ".py"
        ) and not f.endswith('__init__.py')]
        for plugin_name in plugins:
            imported_plugin = importlib.import_module("assistant.plugins." + plugin_name)
            if hasattr(imported_plugin, "__commands__") and imported_plugin.__commands__:
                self.ALL_MODULES[imported_plugin.__name__.lower()] = imported_plugin.__commands__

    def begin(self):
        _LOG.info(_LOG_STR, "Starting Assistant Bot!")
        self.run()
        _LOG.info(_LOG_STR, "Exiting Assistant Bot!")
             

_LOG.info(_LOG_STR, "Assistant-Bot initialized!")
