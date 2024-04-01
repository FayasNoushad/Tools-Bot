from .admin import auth
from vars import ADMINS
from .help import HELP_TEXT, HELP_BUTTONS, ADMIN_HELP_BUTTONS
from .modules.translate import set_language
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


START_TEXT = """Hello {},
I am a tools bot. \
I can help you in groups.

/help for more details."""


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

GROUP_COMMANDS = ["start", "help", "about"]


async def redirect_command(_, message):
    command = message.text.split()[1]
    if command == "start":
        await start(_, message, cb=True)
        return
    if command == "help":
        await help(_, message)
        return
    if command == "about":
        await about(_, message)
        return
    if command in set_language.SET_LANG_COMMANDS:
        await set_language.settings(_, message)
        return
    return


@Client.on_message(filters.group & filters.command(GROUP_COMMANDS))
async def group_commands(bot, message):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    command = message.text.split()[0].replace("/", "").split("@")[0]
    username = (await bot.get_me()).username
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton('Click here', url=f'https://telegram.me/{username}?start={command}')]]
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
            await redirect_command(bot, message)
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
    
    # For admins
    if message.from_user.id in ADMINS:
        buttons = ADMIN_HELP_BUTTONS
    else:
        buttons = HELP_BUTTONS
    if cb:
        await message.message.edit_text(
            text=HELP_TEXT,
            reply_markup=buttons,
            disable_web_page_preview=True
        )
    else:
        await message.reply_text(
            text=HELP_TEXT,
            reply_markup=buttons,
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
