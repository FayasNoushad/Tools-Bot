from ...database import db
from ...admin import auth
from googletrans.constants import LANGUAGES
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


LANG_SET_TEXT = "Select your language for translating. Current default language is `{}`."


def language_buttons():
    pages = []
    button_limit = 2
    line_limit = 8
    for language in LANGUAGES:
        button = InlineKeyboardButton(text=LANGUAGES[language].capitalize(), callback_data="tr-set+"+language)
        if len(pages) == 0 or len(pages[-1]) >= line_limit and len(pages[-1][-1]) >= button_limit:
            pages.append([[button]])
        elif len(pages[-1]) == 0 or len(pages[-1][-1]) >= button_limit:
            pages[-1].append([button])
        else:
            pages[-1][-1].append(button)
    page_no = 0
    no_buttons = []
    if len(pages) == 1:
        return pages
    for page in pages:
        page_no += 1
        page_buttons = []
        if page == pages[0]:
            page_buttons.append(
                InlineKeyboardButton(
                    text="-->",
                    callback_data="tr-page+"+str(page_no+1)
                )
            )
        elif page == pages[-1]:
            page_buttons.append(
                InlineKeyboardButton(
                    text="<--",
                    callback_data="tr-page+"+str(page_no-1)
                )
            )
        else:
            page_buttons.append(
                InlineKeyboardButton(
                    text="<--",
                    callback_data="tr-page+"+str(page_no-1)
                )
            )
            page_buttons.append(
                InlineKeyboardButton(
                    text="-->",
                    callback_data="tr-page+"+str(page_no+1)
                )
            )
        pages[page_no-1].append(page_buttons)
        no_buttons.append(
            InlineKeyboardButton(
                text=str(page_no),
                callback_data="tr-page+"+str(page_no)
            )
        )
        pages[page_no-1].append(no_buttons)
    return pages


@Client.on_message(
    filters.command(
        ["set_lang", "set_default_language", "set_tr", "setlang"]
    )
)
async def settings(bot, message):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    if message.chat.type != enums.ChatType.PRIVATE:
        username = (await bot.get_me()).username
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Click here",
                        url=f"https://telegram.me/{username}?start=set"
                    )
                ]
            ]
        )
        await message.reply_text(
            text="Set your language via private",
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )
        return
    
    language = await db.get_tr_lang(message.from_user.id)
    lang_text = f"{LANGUAGES[language].capitalize()} ({language})"
    await message.reply_text(
        text=LANG_SET_TEXT.format(lang_text),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            language_buttons()[0]
        ),
        quote=True
    )
