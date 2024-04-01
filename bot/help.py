from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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

def help_buttons(admin=False):
    buttons = []
    buttons.append(InlineKeyboardButton("Gemini AI", callback_data="ai-help"))
    buttons.append(InlineKeyboardButton("Information", callback_data="info-help"))
    buttons.append(InlineKeyboardButton("QR Code", callback_data="qr-help"))
    buttons.append(InlineKeyboardButton("YouTube Thumbnail", callback_data="ytthumb-help"))
    buttons.append(InlineKeyboardButton("Translation Help", callback_data="tr-help"))
    buttons.append(InlineKeyboardButton("Country Info", callback_data="countryinfo-help"))
    all_buttons = []
    for button in buttons:
        if len(all_buttons) == 0 or (len(all_buttons[-1]) >= 2):
            all_buttons.append([button])
        else:
            all_buttons[-1].append(button)
    if admin:
        all_buttons.append(
            [
                InlineKeyboardButton('Admin Help', callback_data='admin-help')
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

HELP_BUTTONS = InlineKeyboardMarkup(help_buttons())
ADMIN_HELP_BUTTONS = InlineKeyboardMarkup(help_buttons(admin=True))
MORE_HELP =  InlineKeyboardButton("More Help", callback_data="help")
MORE_HELP_ONLY = InlineKeyboardMarkup([[MORE_HELP]])
