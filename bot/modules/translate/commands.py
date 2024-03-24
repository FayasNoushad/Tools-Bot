from ...admin import auth, add_user
from pyrogram import Client, filters

HELP_TEXT = """
- Just send a text and reply /tr
- Send /tr with message
- /languages - To get all supported languages
- /set_lang - To set a language"""


# Translate Help Message
@Client.on_message(
    filters.command(["trhelp", "tr_help", "translatehelp", "translate_help"])
)
async def tr_help(bot, message):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    # add user to database
    await add_user(message)
    
    await message.reply_text(
        text=HELP_TEXT,
        quote=True
    )
