from ..admin import auth
from pyrogram import Client as Bot
from pyrogram import filters


TEXT = """
- Send /info for your info
- Send /info reply to a forward message for chat or user info
- Send /info reply to another user's message for that user's info
- Send /info @username to get info about a user
- Send /info #chat_id to get info about a chat
"""

# Info Help Message
@Bot.on_message(filters.command(["info_help", "information_help"]))
async def info_help(_, message):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    await message.reply_text(
        text=TEXT,
        quote=True
    )


def user(user):
    text = "--**User Details:**--\n"
    text += f"\n**First Name:** `{user.first_name}`"
    text += f"\n**Last Name:** `{user.last_name},`" if user.last_name else ""
    text += f"\n**User Id:** `{user.id}`"
    text += f"\n**Username:** @{user.username}" if user.username else ""
    text += f"\n**User Link:** {user.mention}" if user.username else ""
    text += f"\n**DC ID:** `{user.dc_id}`" if user.dc_id else ""
    text += f"\n**Is Deleted:** True" if user.is_deleted else ""
    text += f"\n**Is Bot:** True" if user.is_bot else ""
    text += f"\n**Is Verified:** True" if user.is_verified else ""
    text += f"\n**Is Restricted:** True" if user.is_verified else ""
    text += f"\n**Is Scam:** True" if user.is_scam else ""
    text += f"\n**Is Fake:** True" if user.is_fake else ""
    text += f"\n**Is Support:** True" if user.is_support else ""
    text += f"\n**Language Code:** {user.language_code}" if user.language_code else ""
    text += f"\n**Status:** {user.status}" if user.status else ""
    return text


def chat(chat):
    text = "--**Chat Details**--\n" 
    text += f"\n**Title:** `{chat.title}`"
    text += f"\n**Chat ID:** `{chat.id}`"
    text += f"\n**Username:** @{chat.username}" if chat.username else ""
    text += f"\n**Type:** `{chat.type}`"
    text += f"\n**DC ID:** `{chat.dc_id}`"
    text += f"\n**Is Verified:** True" if chat.is_verified else ""
    text += f"\n**Is Restricted:** True" if chat.is_verified else ""
    text += f"\n**Is Creator:** True" if chat.is_creator else ""
    text += f"\n**Is Scam:** True" if chat.is_scam else ""
    text += f"\n**Is Fake:** True" if chat.is_fake else ""
    return text


@Bot.on_message((filters.private | filters.group) & filters.command(["info", "information"]))
async def info(_, message):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    if (not message.reply_to_message) and ((not message.forward_from) or (not message.forward_from_chat)):
        info = user(message.from_user)
    elif message.reply_to_message and message.reply_to_message.forward_from:
        info = user(message.reply_to_message.forward_from)
    elif message.reply_to_message and message.reply_to_message.forward_from_chat:
        info = chat(message.reply_to_message.forward_from_chat)
    elif (message.reply_to_message and message.reply_to_message.from_user) and ((not message.forward_from) or (not message.forward_from_chat)):
        info = user(message.reply_to_message.from_user)
    else:
        return
    try:
        await message.reply_text(
            text=info,
            disable_web_page_preview=True,
            quote=True
        )
    except Exception as error:
        await message.reply_text(error)
