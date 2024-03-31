from ...admin import auth
from ...help import MORE_HELP_ONLY
from pyrogram import Client, filters


HELP_TEXT = """
--**Translate Help**--

- Just send a text and reply /tr
- Send /tr with message
- /languages - To get all supported languages
- /set_lang - To set a language"""


# Translate Help Message
@Client.on_message(
    filters.command(["trhelp", "tr_help", "translatehelp", "translate_help"])
)
async def tr_help(bot, message, cb=False):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    if cb:
        await message.message.edit_text(
            text=HELP_TEXT,
            reply_markup=MORE_HELP_ONLY
        )
    else:
        await message.reply_text(
            text=HELP_TEXT,
            quote=True,
            reply_markup=MORE_HELP_ONLY
        )
