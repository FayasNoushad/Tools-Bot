from ...database import db
from .commands import tr_help
from .set_language import settings
from .languages_list import languages_list
from pyrogram.types import InlineKeyboardMarkup
from googletrans.constants import LANGUAGES
from .set_language import language_buttons, LANG_SET_TEXT


async def tr_cb_data(_, message):
    
    if message.data.startswith("tr"):
        data = message.data.split("-", 1)[1]
    else:
        return
    
    if data == "help":
        await tr_help(_, message, cb=True)
        return
    
    if data == "settings":
        await settings(_, message, cb=True)
        return
    
    if data == "languages":
        await languages_list(_, message, cb=True)
        return
    
    if data.startswith("page+"):
        await message.answer("Processing")
        page_no = int(data.split("+", 1)[1]) - 1
        await message.message.edit_reply_markup(
            InlineKeyboardMarkup(
                language_buttons()[page_no]
            )
        )
    
    if data.startswith("set+"):
        language = data.split("+", 1)[1]
        try:
            await db.update_tr_lang(message.from_user.id, language)
            lang_text = f"{LANGUAGES[language].capitalize()} ({language})"
            await message.message.edit_text(
                text=LANG_SET_TEXT.format(lang_text),
                disable_web_page_preview=True,
                reply_markup=message.message.reply_markup
            )
            alert_text = f"Language changed to {lang_text}"
            await message.answer(text=alert_text, show_alert=True)
        except Exception as error:
            if 'MESSAGE_NOT_MODIFIED' in str(error):
                return
            print(error)
            await message.message.edit_text("Something wrong.")
