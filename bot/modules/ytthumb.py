# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

import ytthumb
from ..admin import auth, add_user
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto


TEXT = """
- Send a youtube video link or video ID.
- Then reply /ytthumb with quality or /ytthumb only.
- I will send the thumbnail.
- Qualities (/ytthumb_qualities) are:
  - sd - Standard Quality
  - mq - Medium Quality
  - hq - High Quality
  - maxres - Maximum Resolution
"""

# YT Thumbnail Help Message
@Client.on_message(
    filters.command(["ytthumb_help", "ytthumbnail_help", "ytthumbhelp", "ytthumbnailhelp"])
)
async def ytthumb_help(bot, message):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    await message.reply_text(
        text=TEXT,
        quote=True
    )


photo_buttons = InlineKeyboardMarkup(
    [[InlineKeyboardButton('Other Qualities', callback_data='ytthumb-qualities')]]
)


async def ytthumb_cb_data(_, message):
    
    if (message.from_user.id != message.message.reply_to_message.from_user.id):
        await message.answer("This is not for you.")
        return
    if message.data.startswith("ytthumb"):
        data = message.data.split("-", 1)[1].lower()
    else:
        return
    if data == "qualities":
        await message.answer('Select a quality')
        buttons = []
        for quality in ytthumb.qualities():
            buttons.append(
                InlineKeyboardButton(
                    text=ytthumb.qualities()[quality],
                    callback_data="ytthumb-"+quality
                )
            )
        await message.edit_message_reply_markup(
            InlineKeyboardMarkup(
                [[buttons[0], buttons[1]], [buttons[2], buttons[3]]]
            )
        )
    if data == "back":
        await message.edit_message_reply_markup(photo_buttons)
    if data in ytthumb.qualities():
        thumbnail = ytthumb.thumbnail(
            video=message.message.reply_to_message.reply_to_message.text,
            quality=data
        )
        quality = ytthumb.qualities()[data]
        await message.answer('Updating to '+quality)
        await message.edit_message_media(
            media=InputMediaPhoto(
                media=thumbnail,
                caption=f"**Quality:** `{quality}`"
            ),
            reply_markup=photo_buttons,
        )
        await message.answer('Updated Successfully')


# YT Thumbnail Qualities
@Client.on_message(filters.command(["ytthumb_qualities"]))
async def ytthumb_qualities(_, message):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    text = "--**Qualities**--\n"
    for quality in ytthumb.qualities():
        text += f"\n**{quality}** - `{ytthumb.qualities()[quality]}`"
    await message.reply_text(
        text=text,
        quote=True
    )


@Client.on_message(filters.command(["ytthumb", 'ytthumbnail']))
async def send_yt_thumbnail(_, message):
    
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
