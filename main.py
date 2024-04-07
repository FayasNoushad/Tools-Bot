import vars
from pyrogram import Client


Bot = Client(
    vars.BOT_NAME,
    bot_token=vars.BOT_TOKEN,
    api_id=vars.API_ID,
    api_hash=vars.API_HASH,
    plugins = dict(
        root="bot"
    )
)

Bot.run()
