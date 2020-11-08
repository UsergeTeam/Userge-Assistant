# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram.types import (
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton)


USERGE_THUMB = "https://imgur.com/download/Inyeb1S"
BOT_THUMB = "https://i.imgur.com/zRglRz3.png"
CONTENT_THUMB = "https://i.imgur.com/v1XSJ1D.png"
REPO_THUMB = "https://i.imgur.com/39VV3Ho_d.png"
GC_THUMB = "https://i.imgur.com/lDpSgmg_d.png"

userge_wiki = "https://github.com/UsergeTeam/Userge/wiki"
decorators = "https://github.com/UsergeTeam/Userge/wiki/Decorators"
deployment = "https://github.com/UsergeTeam/Userge/wiki/Deployment"
examples = "https://github.com/UsergeTeam/Userge/wiki/Examples"
faqs = "https://github.com/UsergeTeam/Userge/wiki/FAQs"

USERGE = [
    InlineQueryResultArticle(
        title="About UserGe",
        input_message_content=InputTextMessageContent(
             "📚 **UserGe**\n\n"
            f"[UserGe](https://github.com/usergeteam/userge) "
             "is a Powerful , Pluggable Telegram UserBot written in "
            f"[Python](https://www.python.org/) using "
            f"[Pyrogram](https://github.com/pyrogram).",
            disable_web_page_preview=True
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👥 Community", url="https://t.me/TheUserGe")
                ],
                [
                    InlineKeyboardButton("🌐 GitHub", url="https://github.com/UserGeTeam/UserGe"),
                    InlineKeyboardButton("📂 Docs", url=f"{userge_wiki}")
                ]
            ]
        ),
        description="UserGe is a Powerful , Pluggable Telegram UserBot.",
        thumb_url=USERGE_THUMB
    ),
    InlineQueryResultArticle(
        title="About UserGe Assistant",
        input_message_content=InputTextMessageContent(
            HELP, disable_web_page_preview=True, parse_mode="markdown"
        ),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                 "🗂 Source Code",
                url="https://github.com/UserGeTeam/UserGe-Assistant"
            ),
            InlineKeyboardButton(
                 "😎 Use Inline!",
                switch_inline_query=""
            )
        ]]),
        description="How to use UserGe Assistant Bot.",
        thumb_url=BOT_THUMB,
    ),
    InlineQueryResultArticle(
        title="Table Of Contents",
        input_message_content=InputTextMessageContent(
             "📚 **UserGe Docs**\n\n"
             "`Table of Contents avalaible in UserGe Wiki.`",
            disable_web_page_preview=True,
        ),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                 "Online Docs 📚", url=f"{userge_wiki}#table-of-contents"
            )
        ]]),
        description="See Contents available in UserGe wiki.",
        thumb_url=CONTENT_THUMB
    ),
    InlineQueryResultArticle(
        title="UserGe-Repository",
        input_message_content=InputTextMessageContent(
             "📚 **UserGe Docs**\n\n"
             "`UserGe-Repositories.`",
            disable_web_page_preview=True,
        ),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                 "Github 🗂", url=f"{userge_wiki}#userge-repository"
            )
        ]]),
        description="All UserGe-Repositories.",
        thumb_url=REPO_THUMB
    ),
    InlineQueryResultArticle(
        title="UserGe-Repository",
        input_message_content=InputTextMessageContent(
             "📚 **UserGe Docs**\n\n"
             "`UserGe-Repositories.`",
            disable_web_page_preview=True,
        ),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                 "Groups and Channels 👥",
                 url=f"{userge_wiki}#join-for-updates--support"
            )
        ]]),
        description="Join UserGe support Group and Updates Channel.",
        thumb_url=GS_THUMB
    )
]

HELP = (
     "🤖 **UserGe Assistant**\n\n"


     "You can use this bot in inline mode to search for UserGe Docs And FAQs"
    f"and All Methods available in [UserGe Wiki]({userge_wiki}).\n\n"

     "**__Search__**\n"
     "`@Userge_Assistant_Bot <query>`\n\n"

     "**__List__**\n"
     "`@Userge_Assistant_Bot Decorators`\n"
     "`@Userge_Assistant_Bot Deployment`\n"
     "`@Userge_Assistant_Bot Vars`\n"
     "`@Userge_Assistant_Bot Modes`\n"
     "`@Userge_Assistant_Bot Example`\n"
     "`@Userge_Assistant_Bot Faqs`"
)

DECORATORS = [
    (
        "UserGe Callback Decorators.",
        "Userge have it's own custom decorators.",
       f"[UserGe Callback Decorators.]({decorators}#userge-callback-decorators)"
    ),
    (
        "Parameters",
        "Required and Non-required Parameters of Decorators.",
       f"[Parameters]({decorators}#parameters)"
    ),
    (
        "Examples",
        "Example of Decorators.",
       f"[Example of Decorators]({decorators}#examples)"
    )
]

DEPLOYMENT = [
    (
        "Config Vars.",
        "About Config Vars and Explanation.",
       f"[Config Vars]({deployment}#config-vars)"
    ),
    (
        "Branches",
        "Check available Branches in UserGe repo.",
       f"[Branches]({deployment}#branches-in-userge-repo)"
    ),
    (
        "Deploy to Heroku",
        "Directly Deploy to Heroku.",
       f"[Deploy to Heroku]({deployment}#deploying-to-heroku--)"
    ),
    (
        "Deploying with Docker",
        "Deploy UserGe using Docker.",
       f"[Deploy with Docker]({deployment}#deploying-with-docker-)"
    ),
    (
        "Deploy With gitPython",
        "Deploy UserGe using gitpython pip.",
       f"[Deploy with gitpython pip]({deployment}#deploying-with-gitpython--pip)"
    )
]

VARS = [
    (
        "Api Id and Api hash",
        "How to get Api Id and Api hash",
       f"[API_ID and API_HASH]({deployment}#1-api_id-and-api_hash)"
    ),
    (
        "Database Url",
        "How to get Database Url.",
       f"[DATABASE_URL]({deployment}#2-database_url)"
    ),
    (
        "Log Channel Id",
        "How to get Log Channel Id",
       f"[LOG_CHANNEL_ID]({deployment}#3-log_channel_id)"
    ),
    (
        "Heroku App Name",
        "How to get Heroku App Name",
       f"[HEROKU_APP_NAME]({deployment}#25-heroku_app_name)"
    ),
    (
        "Heroku Api Key",
        "How to get Heroku Api Key.",
       f"[HEROKU_API_KEY]({deployment}#24-heroku_api_key)"
    ),
    (
        "Load Unofficial Plugins",
        "How to Load Unofficial Plugins.",
       f"[LOAD_UNOFFICIAL_PLUGINS]({deployment}#1-load_unofficial_plugins)"
    ),
    (
        "Workers",
        "Explained Workers Var.",
       f"[Workers]({deployment}#2-workers)"
    ),
    (
        "Client Id and Client Secret",
        "How to get G_DRIVE_CLIENT_ID and G_DRIVE_CLIENT_SECRET",
       f"[CLIENT_ID and CLIENT_SECRET)]({deployment}#3-g_drive_client_id--g_drive_client_secret)"
    ),
    (
        "G_DRIVE_ID_TD",
        "Explained G_DRIVE_IS_TD",
       f"[G_DRIVE_IS_TD]({deployment}#4-g_drive_is_td)"
    ),
    (
        "G_DRIVE_INDEX_LINK",
        "How to get Index Link",
       f"[G_DRIVE_INDEX_LINK]({deployment}#5-g_drive_index_link)"
    ),
    (
        "Gdrive Parent folder Id",
        "How to get Gdrive Parent folder Id",
       f"[G_DRIVE_PARENT_ID]({deployment}#14-g_drive_parent_id)"
    ),
    (
        "Down Path",
        "Explained about Download Path",
       f"[DOWN_PATH]({deployment}#6-down_path)"
    ),
    (
        "Preferred Language",
        "Explained Preferred Language",
       f"[PREFERRED_LANGUAGE]({deployment}#7-preferred_language)"
    ),
    (
        "Currency Api",
        "How to get Currency Api",
       f"[CURRENCY_API]({deployment}#8-currency_api)"
    ),
    (
        "Ocr Space Api Key",
        "How to get Ocr Space Pai Key.",
       f"[OCR_SPACE_API_KEY]({deployment}#9-next-var-is-ocr_space_api_key)"
    ),
    (
        "Weather Defcity",
        "Weather Default City.",
       f"[WEATHER_DEFCITY]({deployment}#10-weather_defcity)"
    ),
    (
        "Spamwatch Api",
        "How to get SpamWatch Api.",
       f"[SPAM_WATCH_API]({deployment}#11-spam_watch_api)"
    ),
    (
        "Open Weather Map",
        "How to get Open Weather Map.",
       f"[OEPN_WEATHER_MAP]({deployment}#12-open_weather_map)"
    ),
    (
        "Remove Background Api",
        "How to get Remove Background Api.",
       f"[REMOVE_BG_API_KEY]({deployment}#13-remove_bg_api_key)"
    ),
    (
        "Command Trigger",
        "What is Command Trigger.",
       f"[CMD_TRIGGER]({deployment}#15-cmd_trigger)"
    ),
    (
        "Sudo Trigger",
        "What is Sudo Trigger.",
       f"[SUDO_TRIGGER]({deployment}#16-sudo_trigger)"
    ),
    (
        "Upstream Repo",
        "What is Upstream Repo",
       f"[UPSTREAM_REPO]({deployment}#17-upstream_repo)"
    ),
    (
        "Finished Progress Bar",
        "What is Finished Progress Bar.",
       f"[FINISHED_PROGRESS_STR]({deployment}#18-finished_progress_str)"
    ),
    (
        "UnFinished Progress Bar",
        "What is UnFinished Progress Bar.",
       f"[UNFINISHED_PROGRESS_STR]({deployment}#19-unfinished_progress_str)"
    ),
    (
        "Custom Pack Name",
        "What is Custom Pack Name.",
       f"[CUSTOM_PACK_NAME]({deployment}#20-custom_pack_name)"
    ),
    (
        "Alive Media",
        "How to get Alive Media var.",
       f"[ALIVE_MEDIA]({deployment}#21-alive_media)"
    ),
    (
        "Insta Id",
        "What is Insta Id.",
       f"[INSTA_ID]({deployment}#22-insta_id)"
    ),
    (
        "Insta Pass",
        "What is Insta Pass.",
       f"[INSTA_Pass]({deployment}#23-insta_pass)"
    ),
    (
        "Heroku String Session",
        "How to Heroku String Session.",
       f"[HU_STRING_SESSION]({deployment}#22-insta_pass)"
    )
]

MODES = [
    (
        "User Mode",
        "Explained Docs for User Mode.",
       f"[What is User Mode?]({deployment}#1-user-mode)"
    ),
    (
        "Bot Mode",
        "Explained Docs for Bot Mode.",
       f"[What is Bot Mode?]({deployment}#2-bot-mode)"
    ),
    (
        "Dual Mode",
        "Explained Docs for Dual Mode.",
       f"[What is Dual Mode?]({deployment}#3-dual-mode)"
    )
]

EXAMPLES = [
    (
        "Cmd Example",
        "Explained Docs for Cmd Example.",
       f"[Example Cmd]({deployment}#example-command)"
    ),
    (
        "Filter Example",
        "Explained Docs for Filter Example.",
       f"[Example Filters]({deployment}#example-filter)"
    )
]

FAQS = [
    ("What is dual mode?", f"{faqs}#1-what-is-dualmode-"),
    ("How to get all cmd list?", f"{faqs}#2-how-to-get-all-cmd-list-"),
    ("How to use a cmd?", f"{faqs}#3-how-to-use-a-cmd-"),
    ("What is parent id/folder id in gdrive?",
    f"{faqs}#4-what-is-parent-idfolder-id-in-gdrive-"),
    ("What is bot mode?", f"{faqs}#5-what-is-bot-mode-"),
    ("What is sudo?", f"{faqs}#6-what-is-sudo-"),
    ("How to enable sudo?", f"{faqs}#7-how-to-enable-sudo-"),
    ("What is dyno saver?", f"{faqs}#8-what-is-dyno-saver--what-is-die-"),
    ("How to Activate botmode?", f"{faqs}#9-how-to-active-botmode-"),
    ("How to Add unofficial plugins?",
    f"{faqs}#10-how-to-add-unofficial-plugins-"),
    ("How to Get string Session?", f"{faqs}#11-how-to-get-string-"),
    ("How to Setup userge?", f"{faqs}#12-how-to-setup-userge-"),
    ("How to get Help Menu as Buttons?",
    f"{faqs}#13-how-to-get-help-menu-as-buttons-"),
    ("How to add buttons in Notes/Filters?",
    f"{faqs}#14-how-to-add-buttons-in-notesfilters-"),
    ("How to setup Lydia ?",
    f"{faqs}#15-how-to-setup-lydia-"),
    ("What is floodwait?", f"{faqs}#16-what-is-floodwait"),
    ("How to setup deezloader?", f"{faqs}#17-how-to-setup-deezloader"),
    ("What is spamwatch?", f"{faqs}#18-what-is-spamwatch"),
    ("How to set your own custom media for .alive?",
    f"{faqs}#19how-to-set-your-own-custom-media-for-alive"),
    ("How to use YouTube cmd in UserGe?",
    f"{faqs}#20-how-to-use-youtube-cmd-of-userge-properly"),
    ("What are index link?", f"{faqs}#21what-are-index-link"),
    ("How to send secret message in userge bot ?",
    f"{faqs}#22how-to-send-secret-message-in-userge-bot-"),
    ("What is the purpose of Worker VAR?",
    f"{faqs}#23-whats-the-purpose-of-worker-var"),
    ("How to clear download path?", f"{faqs}#24-how-to-clear-download-path"),
    ("How to stop autopic?", f"{faqs}#25-how-to-stop-autopic"),
    ("How to use upload and download Using userge?",
    f"{faqs}#26-how-to-use-upload-and-download-feature-of-userge-properly-"),
    ("How to add media in pm permit?", f"{faqs}#27-how-to-add-media-in-custom-pm-permit"),
    ("How to delete profile pic in Telegram?",
    f"{faqs}#28-how-to-delete-all-profile-pic-of-your-telegram-account"),
    ("How to use spam watch api?", f"{faqs}#29-how-to-use-spam-watch-api"),
    ("How to update userbot?", f"{faqs}#30-how-to-update-userbot"),
    ("How to know dyno usage?", f"{faqs}#31-how-to-know-dyno-usage"),
    ("File type issue while downloading from direct link?"
    f"{faqs}#32-file-type-issue-while-downloading-from-direct-link"),
]
