import os
from PIL import Image
from pyzbar.pyzbar import decode
from ...admin import auth
from pyrogram import Client, filters

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
    if not (await auth(message.from_user.id)):
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
    
    decode_text = await message.reply_text(text="Processing your request...", quote=True)
    
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

