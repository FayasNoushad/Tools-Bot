from ...database import db
from ...authorise import auth
from .gemini import check_api
from ...common import MORE_HELP_ONLY
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


HELP = """
--**Gemini AI**--

**Text only:**
- Just send me question as text with /ai command
- I will reply with generated text

**Photo only:**
- Just send me photo
- Then reply /ai command to the photo
- I will reply with generated text

**Photo and Text:**
- Send me a photo
- Reply /ai command with text to the photo
- I will reply with generated text

--**Other Commands**--
/add_api: To add your Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/apikey)
/my_api: To get your Gemini API Key
/delete_api: To delete your Gemini API Key
"""

# Gemini AI Help Message
@Client.on_message(
    filters.command(
        ["aihelp", "ai_help", "geminihelp", "gemini_help", "geminiai_help", "bardhelp", "bard_help"]
    )
)
async def gemini_help(_, message, cb=False):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    if cb:
        await message.message.edit_text(
            text=HELP,
            disable_web_page_preview=True,
            reply_markup=MORE_HELP_ONLY
        )
    else:
        await message.reply_text(
            text=HELP,
            disable_web_page_preview=True,
            quote=True
        )


@Client.on_message(
    filters.private &
    filters.command(
        ["geminiapi", "add_api", "add_gemini_api", "addapi", "updateapi", "update_api"]
    )
)
async def add_api(bot, message):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    if (" " not in message.text):
        await message.reply_text("Send your Gemini API Key")
        return
    
    api = message.text.split(" ", 1)[1]
    m = await message.reply_text("Checking API Key...")
    if check_api(api):
        await db.update_gemini_api(id=message.from_user.id, api=api)
        if await db.get_gemini_api(message.from_user.id):
            text = "API Key updated successfully"
        else:
            text = "API Key added successfully"
        await m.edit_text(text)
    else:
        await m.edit_text("Invalid API Key")


@Client.on_message(
    filters.private &
    filters.command(
        ["my_api", "get_api", "show_api", "view_api", "viewapi", "myapi", "view_geminiapi", "view_geminiapi"]
    )
)
async def get_api(bot, message):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    api = await db.get_gemini_api(message.from_user.id)
    if api:
        await message.reply_text(f"Your Gemini API Key is\n`{api}`")
    else:
        await message.reply_text("You haven't added your Gemini API Key")


@Client.on_message(
    filters.private &
    filters.command(
        ["delete_api", "remove_api", "delete_gemini_api", "remove_gemini_api", "deleteapi", "removeapi"]
    )
)
async def delete_api(bot, message):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    text = "Are you sure to delete your Gemini API Key?"
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Yes', callback_data='gemini-confirm_delete_api'),
                InlineKeyboardButton('No', callback_data='gemini-cancel_delete_api')
            ]
        ]
    )
    await message.reply_text(
        text=text,
        reply_markup=buttons,
        quote=True
    )

