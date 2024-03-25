from .admin import auth, add_user
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


START_TEXT = """Hello {},
I am a tools bot. \
I can help you in groups.

/help for more details."""

HELP_TEXT = """--**More Help**--

- Just send me commands
- I will reply

**Available Commands:**

- /start: Start the bot
- /help: Get help and command information
- /about: Get information about the bot

- /ai_help: Help message for the AI plugin
- /info_help: Help message for the info plugin
- /qr_help: Help message for the QR plugin
- /ytthumb_help: Help message for the YouTube thumbnail plugin
- /tr_help: Help message for the translation plugin
- /countryinfo_help: Help message for the country information plugin
"""

# Add help messages for other plugins here

ABOUT_TEXT = """**About Me**

- **Bot :** `Tools Bot`
- **Developer :** [GitHub](https://github.com/FayasNoushad) | [Telegram](https://telegram.me/FayasNoushad)
- **Source :** [Click here](https://github.com/FayasNoushad/Tools-Bot)
- **Language :** [Python 3](https://python.org)
- **Library :** [Pyrogram](https://pyrogram.org)"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ],
        [
            InlineKeyboardButton('Feedback', url='https://telegram.me/FayasNoushad')
        ]
    ]
)

HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)

ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)

BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Feedback', url='https://telegram.me/FayasNoushad')
        ]
    ]
)


@Client.on_message(filters.group & filters.command(["start", "help", "about"]))
async def group_commands(bot, message):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    username = (await bot.get_me()).username
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton('Click here', url=f'https://telegram.me/{username}?start=help')]]
    )
    await message.reply_text(
        text="You can use this command in private chat with me.",
        reply_markup=buttons,
        quote=True
    )


@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, message, cb=False):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    if not cb:
        if len(message.text.split()) > 1:
            await help(bot, message)
            return
    
    text=START_TEXT.format(message.from_user.mention)
    if cb:
        await message.message.edit_text(
            text=text,
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await message.reply_text(
            text=text,
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS,
            quote=True
        )


@Client.on_message(filters.private & filters.command(["help"]))
async def help(bot, message, cb=False):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    if cb:
        await message.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await message.reply_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True,
            quote=True
        )


@Client.on_message(filters.private & filters.command(["about"]))
async def about(bot, message, cb=False):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    if cb:
        await message.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await message.reply_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True,
            quote=True
        )
