from googletrans import constants
from ...admin import auth, add_user
from pyrogram import Client, filters


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

