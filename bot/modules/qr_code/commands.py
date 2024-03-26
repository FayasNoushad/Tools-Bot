from ...admin import auth
from pyrogram import Client, filters


HELP_TEXT = """**Hey, Follow these steps:**

1. To generate a QR code, use the command /qr followed by the text or link you want to encode. For example: `/qr Hello World`
2. To decode a QR code, reply to a QR code image with the command /qrdecode. For example, reply to a QR code image with `/qrdecode`.

Note: Only text and link QR codes are supported for encoding and decoding."""

# QR Code Help Message
@Client.on_message(
    filters.command(["qrhelp", "qr_help", "qr_code_help"])
)
async def qr_help(bot, message):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    await message.reply_text(
        text=HELP_TEXT,
        quote=True
    )

