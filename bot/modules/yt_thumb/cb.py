import ytthumb
from .thumbnail import photo_buttons
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto



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
    if data in ytthumb.qualities():
        thumbnail = ytthumb.thumbnail(
            video=message.message.reply_to_message.reply_to_message.text,
            quality=data
        )
        quality = ytthumb.qualities()[data]
        await message.answer("Updating to "+quality)
        await message.edit_message_media(
            media=InputMediaPhoto(
                media=thumbnail,
                caption=f"**Quality:** `{quality}`"
            ),
            reply_markup=photo_buttons,
        )
        await message.answer("Updated Successfully")
