import os
from io import BytesIO
from ..admin import auth, add_user
from pyrogram import Client, filters
from googletrans import Translator, constants


HELP_TEXT = """
- Just send a text and reply /tr with language code
- /languages - To get all supported languages

example :- `/tr ml`"""

DEFAULT_LANGUAGE = os.environ.get("DEFAULT_LANGUAGE", "en")


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


@Client.on_message(filters.command(["languages", "langs", "languages_list"]))
async def languages_list(bot, message):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    # add user to database
    await add_user(message)
    
    languages = constants.LANGUAGES
    languages_text = "**Languages**\n"
    for language in languages:
        languages_text += f"\n`{languages[language].capitalize()}` -> `{language}`"
    await message.reply_text(
        text=languages_text,
        disable_web_page_preview=True,
        quote=True
    )


@Client.on_message(filters.command(["tr", "trans", "translate"]))
async def translate(bot, message):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    # add user to database
    await add_user(message)
    
    text = message.reply_to_message.text
    if " " in message.text:
        language = message.text.split(" ", 1)[1]
    else:
        language = DEFAULT_LANGUAGE
    
    translator = Translator()
    message = await message.reply_text("`Translating...`")
    
    try:
        translate = translator.translate(text, dest=language)
        translate_text = f"**Translated to {language}**"
        translate_text += f"\n\n`{translate.text}`"
        if len(translate_text) < 4096:
            await message.edit_text(
                text=translate_text,
                disable_web_page_preview=True
            )
        else:
            with BytesIO(str.encode(str(translate_text))) as translate_file:
                translate_file.name = language + ".txt"
                await message.reply_document(
                    document=translate_file,
                    quote=True
                )
                await message.delete()
    except Exception as error:
        print(error)
        await message.edit_text("Something wrong.")
