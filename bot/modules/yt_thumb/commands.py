from ...admin import auth
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
async def ytthumb_help(bot, message):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    await message.reply_text(
        text=TEXT,
        quote=True
    )
