import ytthumb
from ...admin import auth
from pyrogram import Client, filters


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

