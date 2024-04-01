from ...database import db
from ...admin import auth
from ...help import MORE_HELP
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.private & filters.command(["qr_settings", "qrsettings"]))
async def display_settings(bot, message, cb=False):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    chat_id = message.from_user.id
    as_file = await db.is_qr_as_file(chat_id)
    as_file_btn = [
        InlineKeyboardButton("Upload Mode", callback_data="qr-lol")
    ]
    if as_file:
        as_file_btn.append(
            InlineKeyboardButton('Upload as File', callback_data='qr-set_af')
        )
    else:
        as_file_btn.append(
            InlineKeyboardButton('Upload as Photo', callback_data='qr-set_af')
        )
    
    help_buttons = [
        InlineKeyboardButton("QR Code Help", callback_data="qr-help"),
        MORE_HELP
    ]
    close_btn = [
        InlineKeyboardButton('Close ✖️', callback_data='close')
    ]
    settings_buttons = InlineKeyboardMarkup([as_file_btn, help_buttons, close_btn])
    qr_text = f"--**QR Code Settings**--\n\n**Current Mode:** `{'File' if as_file else 'Photo'}`"
    try:
        if cb:
            await message.message.edit_text(
                text=qr_text,
                disable_web_page_preview=True,
                reply_markup=settings_buttons
            )
        else:
            await message.reply_text(
                text=qr_text,
                quote=True,
                disable_web_page_preview=True,
                reply_markup=settings_buttons
            )
    except Exception as error:
        print(error)

