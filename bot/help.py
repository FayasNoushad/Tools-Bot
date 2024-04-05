from .modules import MODULES
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
