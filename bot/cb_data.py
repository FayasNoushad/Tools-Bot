from pyrogram import Client
from .admin import auth, admin_help
from .commands import start, help, about
from .modules.info.cb import info_cb_data
from .modules.qr_code.cb import qr_cb_data
from .modules.translate.cb import tr_cb_data
from .modules.gemini.cb import gemini_cb_data
from .modules.yt_thumb.cb import ytthumb_cb_data
from .modules.country_info.cb import country_cb_data
from .modules.dictionary.cb import dictionary_cb_data


@Client.on_callback_query()
async def cb_data(_, message):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    if message.data.startswith("admin"):
        data = message.data.split("-", 1)[1]
        if data == "help":
            await admin_help(_, message, cb=True)
    
    if message.data.startswith("country"):
        await country_cb_data(_, message)
        return
    
    if message.data.startswith("info"):
        await info_cb_data(_, message)
        return
    
    if message.data.startswith("ytthumb"):
        await ytthumb_cb_data(_, message)
        return
    
    if message.data.startswith("gemini") or message.data.startswith("ai"):
        await gemini_cb_data(_, message)
        return
    
    if message.data.startswith("tr"):
        await tr_cb_data(_, message)
        return
    
    if message.data.startswith("qr"):
        await qr_cb_data(_, message)
        return
    
    if message.data.startswith("dictionary"):
        await dictionary_cb_data(_, message)
        return
    
    if message.data == "home":
        await start(_, message, cb=True)
    elif message.data == "help":
        await help(_, message, cb=True)
    elif message.data == "about":
        await about(_, message, cb=True)
    else:
        await message.message.delete()