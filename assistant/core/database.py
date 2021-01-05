# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

import json
from typing import Dict, Optional

from pyrogram.errors import MessageNotModified
from .client import Bot


class DB(Bot):
    CHANNEL_ID = -1001480669647
    WARN_LIMIT_ID = 7
    WARN_MODE_ID = 8
    WARN_DATA_ID = 9
    BLACKLIST_MODE_ID = 10
    BLACKLIST_DATA_ID = 11
    FLOOD_MODE_ID = 12
    FLOOD_LIMIT_ID = 13
    
    async def load_data(self, msg_id: int) -> Dict[Optional[str]]:
        msg = await self.get_messages(self.CHANNEL_ID, msg_id)
        if msg:
            return json.loads(msg.text)
        return {}
    
    async def save_data(self, msg_id: int, text: str) -> None:
        try:
            await self.edit_message_text(
                self.CHANNEL_ID,
                msg_id,
                f"`{text}`",
                disable_web_page_preview=True
            )
        except MessageNotModified:
            pass
