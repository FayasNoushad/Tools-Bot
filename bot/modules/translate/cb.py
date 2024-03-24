from ...database import db
from pyrogram.types import InlineKeyboardMarkup
from googletrans.constants import LANGUAGES
from .set_language import language_buttons, LANG_SET_TEXT


async def tr_cb_data(_, message):
    
    if message.data.startswith("tr"):
        data = message.data.split("-", 1)[1]
    else:
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
            print(error)
            await message.message.edit_text("Something wrong.")
