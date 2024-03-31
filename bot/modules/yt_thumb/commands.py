from ...admin import auth
from ...help import MORE_HELP_ONLY
from pyrogram import Client, filters


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
async def ytthumb_help(bot, message, cb=False):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    if cb:
        await message.message.edit_text(
            text=TEXT,
            reply_markup=MORE_HELP_ONLY
        )
    else:
        await message.reply_text(
            text=TEXT,
            quote=True,
            reply_markup=MORE_HELP_ONLY
        )
