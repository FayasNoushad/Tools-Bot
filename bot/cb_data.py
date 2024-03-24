from pyrogram import Client
from .admin import add_user
from .modules.ytthumb import ytthumb_cb_data
from .commands import start, help, about


@Client.on_callback_query()
async def cb_data(_, message):
    
    # add user to database
    await add_user(message)
    
    if message.data.startswith("ytthumb"):
        await ytthumb_cb_data(_, message)
        return
    if message.data == "home":
        await start(_, message, cb=True)
    elif message.data == "help":
        await help(_, message, cb=True)
    elif message.data == "about":
        await about(_, message, cb=True)
    else:
        await message.message.delete()