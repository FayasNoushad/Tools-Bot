from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

MORE_HELP =  InlineKeyboardButton("More Help", callback_data="help")
MORE_HELP_ONLY = InlineKeyboardMarkup([[MORE_HELP]])
