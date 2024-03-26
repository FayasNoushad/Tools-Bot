from ...admin import auth
from pyrogram import Client, filters


TEXT = """
- Send /info for your info
- Send /info reply to a forward message for chat or user info
- Send /info reply to another user's message for that user's info
- Send /info @username to get info about a user
- Send /info #chat_id to get info about a chat
"""

# Info Help Message
@Client.on_message(
    filters.command(["info_help", "information_help", "infohelp", "informationhelp"])
)
async def info_help(_, message):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    await message.reply_text(
        text=TEXT,
        quote=True
    )