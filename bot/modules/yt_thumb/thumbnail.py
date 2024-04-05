import ytthumb
from ...authorise import auth
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


photo_buttons = InlineKeyboardMarkup(
    [[InlineKeyboardButton('Other Qualities', callback_data='ytthumb-qualities')]]
)


@Client.on_message(filters.command(["ytthumb", 'ytthumbnail']))
async def yt_thumbnail(_, message):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    m = await message.reply_text(
        text="`Analysing...`",
        disable_web_page_preview=True,
        quote=True
    )
    try:
        if (" " in message.text):
            text = message.text.split(" ", 1)[1]
            if text.startswith("http"):
                if " | " in text:
                    link = text.split(" | ", 1)[0]
                    quality = text.split(" | ", 1)[1]
                else:
                    link = text
                    quality = "sd"
            else:
                if (message.reply_to_message) and (message.reply_to_message.text):
                    if message.reply_to_message.text.startswith("http"):
                        link = message.reply_to_message.text.split(" ")[0]
                        quality = message.text.split(" ", 1)[1]
                        if quality not in ytthumb.qualities():
                            quality = "sd"
                else:
                    text = message.text.split(" ", 1)[1]
                    if " | " in text:
                        link = text.split(" | ", -1)[0]
                        quality = text.split(" | ", -1)[1]
                    else:
                        link = message.text.split(" ", 1)[1]
                        quality = "sd"
        else:
            if (message.reply_to_message) and (message.reply_to_message.text):
                link = message.reply_to_message.text
                quality = "sd"
            else:
                await m.edit_text(
                    text="Send a youtube video link or video ID.",
                    disable_web_page_preview=True
                )
                return
        thumbnail = ytthumb.thumbnail(
            video=link,
            quality=quality
        )
        buttons = photo_buttons if (message.reply_to_message and message.reply_to_message.text) else None
        await message.reply_photo(
            photo=thumbnail,
            reply_markup=buttons,
            caption=f"**Quality:** `{ytthumb.qualities()[quality]}`",
            quote=True
        )
        await m.delete()
    except Exception as error:
        await message.edit_text(
            text=error,
            disable_web_page_preview=True
        )
