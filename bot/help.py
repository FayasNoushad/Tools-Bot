from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


MODULES = {
    "ai": {
        "title": "Gemini AI",
        "command": "ai_help",
        "description": "Help message for the AI"
    },
    "info": {
        "title": "Info",
        "command": "info_help",
        "description": "Help message for the info"
    },
    "qr": {
        "title": "QR Code",
        "command": "qr_help",
        "description": "Help message for the QR"
    },
    "ytthumb": {
        "title": "YouTube Thumbnail",
        "command": "ytthumb_help",
        "description": "Help message for the YouTube thumbnail"
    },
    "tr": {
        "title": "Translation",
        "command": "tr_help",
        "description": "Help message for the translation"
    },
    "countryinfo": {
        "title": "Country Information",
        "command": "countryinfo_help",
        "description": "Help message for the country information"
    },
    "dictionary": {
        "title": "Dictionary",
        "command": "dictionary_help",
        "description": "Help message for the dictionary"
    }
}

# Help Text without module help commands
ONLY_HELP_TEXT = """--**More Help**--

- Just send me commands
- I will reply

**Available Commands:**

- /start: Start the bot
- /help: Get help and command information
- /about: Get information about the bot"""


# Help Text with module help commands
def help_text():
    text = ONLY_HELP_TEXT + "\n"
    # add module help commands
    for module in MODULES:
        text += f"\n- /{MODULES[module]['command']} - {MODULES[module]['description']}"
    return text


def help_buttons(admin=False):
    buttons = []
    for module in MODULES:
        buttons.append(InlineKeyboardButton(MODULES[module]['title'], callback_data=module+'-help'))
    all_buttons = []
    for button in buttons:
        if len(all_buttons) == 0 or (len(all_buttons[-1]) >= 2):
            all_buttons.append([button])
        else:
            all_buttons[-1].append(button)
    if admin:
        all_buttons.append(
            [
                InlineKeyboardButton('Admin Help', callback_data='admin-help-help')
            ]
        )
    all_buttons.append(
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    )
    return all_buttons


HELP_TEXT = help_text()
HELP_BUTTONS = InlineKeyboardMarkup(help_buttons())
ADMIN_HELP_BUTTONS = InlineKeyboardMarkup(help_buttons(admin=True))
MORE_HELP =  InlineKeyboardButton("More Help", callback_data="help")
MORE_HELP_ONLY = InlineKeyboardMarkup([[MORE_HELP]])
