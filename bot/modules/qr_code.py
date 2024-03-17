import os
import pyqrcode
from PIL import Image
from pyzbar.pyzbar import decode
from ..admin import auth
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
    if not auth(message.from_user.id):
        return
    
    await message.reply_text(
        text=HELP_TEXT,
        quote=True
    )


@Client.on_message(
    filters.command(
        [
            "qr_decode", "qrdecode", "decodeqr", "decode_qr",
            "readqr", "read_qr", "qr_read", "qr_read",
            "scanqr", "scan_qr", "qrscan", "qr_scan"
        ]
    )
)
async def qr_decode(bot, message):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    if not message.reply_to_message:
        await message.reply_text(
            text="Reply to a QR code image to decode.",
            quote=True
        )
        return
    if (message.reply_to_message.document) and ("image" not in message.reply_to_message.document.mime_type):
        await message.reply_text(
            text="Send a QR code image to decode.",
            quote=True
        )
        return
    
    decode_text = await message.reply_text(text="Processing your request...")
    
    dl_location = f"./downloads/{str(message.from_user.id)}/qr_code"
    im_dowload = ''
    qr_text = ''
    try:
        await decode_text.edit("Trying to download....")
        im_dowload = await message.reply_to_message.download(file_name=dl_location+'.png')
    except Exception as error:
        await decode_text.edit(text=error)
        return
    try:
        await decode_text.edit(text="Decoding.....")
        qr_text_data = decode(Image.open(im_dowload))
        qr_text_list = list(qr_text_data[0])  # Listing
        qr_text_ext = str(qr_text_list[0]).split("'")[1]  # Text Extract
        qr_text = "".join(qr_text_ext)  # Text_join
    except Exception as error:
        await decode_text.edit(text=error)
        return
    await decode_text.edit_text(
        text=f"Decoded text/link :-\n\n{qr_text}",
        disable_web_page_preview=True
    )
    try:
        os.remove(im_dowload)
    except Exception as error:
        print(error)


@Client.on_message(
    filters.command(
        ["qr", "qrcode", "qr_code", "makeqr", "make_qr", "createqr", "create_qr", "genqr", "gen_qr"]
    )
)
async def qr(bot, message):
    
    # authorising
    if not auth(message.from_user.id):
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
    try:
        await qr.edit_text("Trying to Uploading....")
        await message.reply_photo(
            photo=img,
            quote=True
        )
        await qr.delete()
    except Exception as error:
        print(error)
    try:
        os.remove(img)
    except Exception as error:
        print(error)
