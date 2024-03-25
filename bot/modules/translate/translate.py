import os
from io import BytesIO
from ...database import db
from googletrans import Translator
from ...admin import auth, add_user
from pyrogram import Client, filters


@Client.on_message(filters.command(["tr", "trans", "translate"]))
async def translate(bot, message):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    if (" " not in message.text):
        if message.reply_to_message:
            text = message.reply_to_message.text
        else:
            await message.reply_text("Reply to a message or write a text to translate.")
            return
    else:
        text = message.text.split(" ", 1)[1]
    
    language = await db.get_tr_lang(message.chat.id)
    
    translator = Translator()
    message = await message.reply_text("`Translating...`")
    
    try:
        translate = translator.translate(text, dest=language)
        translate_text = f"**Translated to {language}**"
        translate_text += f"\n\n`{translate.text}`"
        if len(translate_text) < 4096:
            await message.edit_text(
                text=translate_text,
                quote=True,
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
            os.remove(translate_file)
    except Exception as error:
        print(error)
        await message.edit_text("Something wrong.")
