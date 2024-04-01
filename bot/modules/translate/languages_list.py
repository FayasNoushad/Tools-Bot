from ...admin import auth
from ...help import MORE_HELP
from googletrans import constants
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command(["languages", "langs", "languages_list"]))
async def languages_list(_, message, cb=False):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    languages = constants.LANGUAGES
    languages_text = "**Languages**\n"
    for language in languages:
        languages_text += f"\n`{languages[language].capitalize()}` -> `{language}`"
    
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Translate Help", callback_data="tr-help")],
            [MORE_HELP]
        ]
    )
    if cb:
        await message.message.edit_text(
            text=languages_text,
            disable_web_page_preview=True,
            reply_markup=buttons
        )
    else:
        await message.reply_text(
            text=languages_text,
            disable_web_page_preview=True,
            reply_markup=buttons,
            quote=True
        )
