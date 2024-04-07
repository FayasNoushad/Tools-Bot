from ...authorise import auth
from ...common import MORE_HELP
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


HELP_TEXT = """--**QR Code Help**--

1. To generate a QR code, use the command /qr followed by the text or link you want to encode. For example: `/qr Hello World`
2. To decode a QR code, reply to a QR code image with the command /qrdecode. For example, reply to a QR code image with `/qrdecode`.
3. /qr_settings: To QR Code settings

Note: Only text and link QR codes are supported for encoding and decoding."""

# QR Code Help Message
@Client.on_message(
    filters.command(["qrhelp", "qr_help", "qr_code_help"])
)
async def qr_help(_, message, cb=False):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Settings", callback_data="qr-settings"),
                MORE_HELP
            ]
        ]
    )
    if cb:
        await message.message.edit_text(
            text=HELP_TEXT,
            reply_markup=buttons
        )
    else:
        await message.reply_text(
            text=HELP_TEXT,
            quote=True,
            reply_markup=buttons
        )

