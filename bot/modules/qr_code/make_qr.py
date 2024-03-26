import os
import pyqrcode
from ...database import db
from ...admin import auth
from pyrogram import Client, filters


@Client.on_message(
    filters.command(
        ["qr", "qrcode", "qr_code", "makeqr", "make_qr", "createqr", "create_qr", "genqr", "gen_qr"]
    )
)
async def qr(bot, message):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    if message.reply_to_message and message.reply_to_message.text:
        text = message.reply_to_message.text
    else:
        if (" " in message.text):
            text = message.text.split(" ", 1)[1]
        else:
            await message.reply_text(
                text="You haven't entered any text to encode.",
                quote=True
            )
            return
    qr = await message.reply_text(
        text="Making your QR Code...",
        quote=True
    )
    s = str(text)
    qrname = f"./downloads/{str(message.from_user.id)}_qr_code.png"
    try:
        qrcode = pyqrcode.create(s.encode('utf-8'))  # Encode the text using UTF-8
        qrcode.png(qrname + '.png', scale=6)
    except UnicodeDecodeError:
        qr.edit_text("Unsupported characters found in the text.")
        await qr.delete()
        return
    except Exception as error:
        qr.edit_text(error)
        await qr.delete()
        return
    img = qrname + '.png'
    as_file = await db.is_qr_as_file(message.from_user.id)
    try:
        await qr.edit_text("Trying to Uploading....")
        if as_file:
            await message.reply_document(
                document=img
            )
        else:
            await message.reply_photo(
                photo=img
            )
        await qr.delete()
    except Exception as error:
        print(error)
    try:
        os.remove(img)
    except Exception as error:
        print(error)
