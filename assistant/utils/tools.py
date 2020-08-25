# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

from assistant import Config


def time_formatter(seconds: float) -> str:
    """ humanize time """
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2]


def is_admin(chat_id: int, user_id: int, check_devs: bool = False) -> bool:
    """ check user is admin or not in this chat """
    if check_devs and is_dev(user_id):
        return True
    if chat_id not in Config.ADMINS:
        return False
    return user_id in Config.ADMINS[chat_id]


def is_dev(user_id: int) -> bool:
    """ returns user is dev or not """
    return user_id in Config.DEV_USERS
