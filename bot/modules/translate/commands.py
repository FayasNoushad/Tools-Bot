from ...admin import auth
from ...help import MORE_HELP
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
async def tr_help(_, message, cb=False):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Set Language", callback_data="tr-settings"),
                InlineKeyboardButton("Languages List", callback_data="tr-languages")
            ],
            [
                MORE_HELP
            ]
        ]
    )
    
    if cb:
        await message.message.edit_text(
            text=HELP_TEXT,
            reply_markup=buttons
        )
    else:
        await message.reply_text(
            text=HELP_TEXT,
            quote=True,
            reply_markup=buttons
        )
