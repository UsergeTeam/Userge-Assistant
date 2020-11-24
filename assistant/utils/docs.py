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

intro = "**📚 UserGe Docs**\n\n"

USERGE_THUMB = "https://imgur.com/download/Inyeb1S"
USER_THUMB = "https://i.imgur.com/h6ZyB71.png"
BOT_THUMB = "https://i.imgur.com/zRglRz3.png"
DUAL_THUMB = "https://i.imgur.com/ZTcIANz.png"
CONTENT_THUMB = "https://i.imgur.com/v1XSJ1D.png"
REPO_THUMB = "https://i.imgur.com/hoRVXM3.png"
GC_THUMB = "https://i.imgur.com/lDpSgmg_d.png"

DECORATORS_THUMB = "https://i.imgur.com/xp3jld1.png"
DEPLOYMENT_THUMB = "https://i.imgur.com/S5lY8fy.png"
VARS_THUMB = "https://i.imgur.com/dw1lLBX.png"
EXAMPLE_THUMB = "https://i.imgur.com/NY4uasQ.png"
FAQS_THUMB = "https://i.imgur.com/b33rM21.png"

userge_wiki = "https://theuserge.github.io/"
decorators = "https://theuserge.github.io/decorators.html"
deployment = "https://theuserge.github.io/deployment.html"
vars = f"{deployment}#list-of-available-vars"
modes = f"{deployment}#userge-modes"
examples = "https://theuserge.github.io/examples.html"
faqs = "https://theuserge.github.io/faq.html"

HELP = (
    "🤖 **UserGe Assistant**\n\n"


    "You can use this bot in inline mode to search for UserGe Docs and FAQs"
    f" and All Methods available in [UserGe Docs]({userge_wiki}).\n\n"

    "**__Search__**\n"
    "`@UsergeBot <query>`\n\n"

    "**__List of Queries__**\n"
    "`Decorators`\n"
    "`Deployment`\n"
    "`Vars`\n"
    "`Modes`\n"
    "`Example`\n"
    "`Faqs`"
)

USERGE = [
    InlineQueryResultArticle(
        title="About UserGe",
        input_message_content=InputTextMessageContent(
            "**👑 UserGe**\n\n"
            "**[UserGe](https://github.com/usergeteam/userge) **"
            "**is a Powerful , Pluggable Telegram UserBot written in **"
            "**[Python](https://www.python.org/) using **"
            "**[Pyrogram](https://github.com/pyrogram).**",
            disable_web_page_preview=True
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👥 Community", url="https://t.me/UserGeOt")
                ],
                [
                    InlineKeyboardButton("🗂 GitHub", url="https://github.com/UserGeTeam/UserGe"),
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
        title="Quick Links",
        input_message_content=InputTextMessageContent(
            "📚 **UserGe Docs**\n\n"
            "`Quick Links.`",
            disable_web_page_preview=True,
        ),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "Online Docs 📚", url=f"{userge_wiki}#quick-links"
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
                "Github 🗂", url=f"{userge_wiki}"
            )
        ]]),
        description="All UserGe-Repositories.",
        thumb_url=REPO_THUMB
    ),
    InlineQueryResultArticle(
        title="Groups and Channels",
        input_message_content=InputTextMessageContent(
            "📚 **UserGe Docs**\n\n"
            "`Join Our Updates Channel and Support Group.`",
            disable_web_page_preview=True,
        ),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "Groups and Channels 👥",
                url=f"{userge_wiki}"
            )
        ]]),
        description="Join UserGe support Group and Updates Channel.",
        thumb_url=GC_THUMB
    )
]

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
        f"[Config Vars]({deployment}#config-vars--setting-up-vars)"
    ),
    (
        "Branches",
        "Check available Branches in UserGe repo.",
        f"[Branches]({deployment}#branches-in-userge-repository)"
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
        "How to get Database Url",
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
        "How to get Heroku Api Key",
        f"[HEROKU_API_KEY]({deployment}#24-heroku_api_key)"
    ),
    (
        "Heroku Session String",
        "How to get Heroku Session String",
        f"[HU_STRING_SESSION]({deployment}#1-user-mode)"
    ),
    (
        "Load Unofficial Plugins",
        "How to Load Unofficial Plugins.",
        f"[LOAD_UNOFFICIAL_PLUGINS]({deployment}#1-load_unofficial_plugins)"
    ),
    (
        "Workers",
        "Explained Workers Var",
        f"[Workers]({deployment}#2-workers)"
    ),
    (
        "Client Id and Client Secret",
        "How to get CLIENT_ID and CLIENT_SECRET",
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
        f"[INSTA_PASS]({deployment}#23-insta_pass)"
    )
]

MODES = [
    (
        "User Mode",
        "Explained Docs for User Mode.",
        f"[What is User Mode?]({deployment}#1-user-mode)",
        f"{USER_THUMB}"
    ),
    (
        "Bot Mode",
        "Explained Docs for Bot Mode.",
        f"[What is Bot Mode?]({deployment}#2-bot-mode)",
        f"{BOT_THUMB}"
    ),
    (
        "Dual Mode",
        "Explained Docs for Dual Mode.",
        f"[What is Dual Mode?]({deployment}#3-dual-mode)",
        f"{DUAL_THUMB}"
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
    ("How to Setup userge?", f"{faqs}#1-how-to-setup-userge"),
    ("How to Add unofficial plugins?",
    f"{faqs}#2-how-to-add-unofficial-plugins"),
    ("How to genrate String Session?", f"{faqs}#3-how-to-generate-string-session-"),
    ("How to get all cmd list?", f"{faqs}#4-how-to-get-all-commands-list"),
    ("How to use a cmd?", f"{faqs}#5-how-to-use-a-command"),
    ("What is sudo and how to enable it?", f"{faqs}#6-what-is-sudo-how-to-enable-it"),
    ("What is parent id/folder id in gdrive?",
    f"{faqs}#7-what-is-parent-id-folder-id-in-gdrive-how-to-get-it"),
    ("What is bot mode and how to enable bot mode?",
    f"{faqs}#8-what-is-bot-mode-how-to-enable-bot-mode"),
    ("How to get Help Menu as Inline Mode?",
    f"{faqs}#9-how-to-get-help-menu-as-inline-mode"),
    ("What is dyno saver and what is .die cmd?",
    f"{faqs}#10-what-is-dyno-saver-what-is-die-only-for-heroku-users"),
    ("How to add buttons in Notes/Filters?",
    f"{faqs}#11-how-to-add-buttons-in-notesfilters-"),
    ("How to setup Lydia ?",
    f"{faqs}#12-how-to-setup-lydia-"),
    ("What is floodwait?", f"{faqs}#13-what-is-floodwait"),
    ("How to setup deezloader?", f"{faqs}#14-how-to-setup-deezloader"),
    ("What is spamwatch?", f"{faqs}#15-what-is-spamwatch"),
    ("How to set your own custom media for .alive?",
    f"{faqs}#16how-to-set-your-own-custom-media-for-alive"),
    ("How to use YouTube cmd in UserGe?",
    f"{faqs}#17-how-to-use-youtube-cmd-of-userge-properly"),
    ("What are index link?", f"{faqs}#18what-are-index-link"),
    ("How to send secret message in userge bot ?",
    f"{faqs}#19how-to-send-secret-message-in-userge-bot-"),
    ("What is the purpose of Worker VAR?",
    f"{faqs}#20-whats-the-purpose-of-worker-var"),
    ("How to clear download path?", f"{faqs}#21-how-to-clear-download-path"),
    ("How to stop autopic?", f"{faqs}#22-how-to-stop-autopic"),
    ("How to use upload and download Using userge?",
    f"{faqs}#23-how-to-use-upload-and-download-feature-of-userge-properly-"),
    ("How to add media in pm permit?", f"{faqs}#24-how-to-add-media-in-custom-pm-permit"),
    ("How to delete profile pic in Telegram?",
    f"{faqs}#25-how-to-delete-all-profile-pic-of-your-telegram-account"),
    ("How to use spam watch api?", f"{faqs}#26-how-to-use-spam-watch-api"),
    ("How to update userbot?", f"{faqs}#27-how-to-update-userbot"),
    ("How to know dyno usage?", f"{faqs}#28-how-to-know-dyno-usage"),
    ("File type issue while downloading from direct link?",
    f"{faqs}#29-file-type-issue-while-downloading-from-direct-link")
]
