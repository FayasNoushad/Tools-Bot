from pyrogram import Client
from .admin import auth, add_user
from .modules.ytthumb import ytthumb_cb_data
from .modules.gemini.cb import gemini_cb_data
from .commands import start, help, about


@Client.on_callback_query()
async def cb_data(_, message):
    
    # authorising
    if not auth(message.from_user.id):
        return
    
    # add user to database
    await add_user(message)
    
    if message.data.startswith("ytthumb"):
        await ytthumb_cb_data(_, message)
        return
    
    if message.data.startswith("gemini"):
        await gemini_cb_data(_, message)
        return
    
    if message.data == "home":
        await start(_, message, cb=True)
    elif message.data == "help":
        await help(_, message, cb=True)
    elif message.data == "about":
        await about(_, message, cb=True)
    else:
        await message.message.delete()