from ...admin import auth
from ...help import MORE_HELP_ONLY
from pyrogram import Client, filters


HELP_TEXT = """--**Dictionary Help**--

- Send me in words with /dict command
  eg:- `/dict Hello`
- or Just send me the word and reply /dict to it
- I will provide you the meaning of the word.
"""


# Dictionary Help Message
@Client.on_message(
    filters.command(["dict_help", "dictionary_help"])
)
async def dictionary_help(_, message, cb=False):
    
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
