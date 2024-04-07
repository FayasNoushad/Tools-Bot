from pyrogram import Client
from .help import MODULES
from .authorise import auth
from .admin import admin_cb_data
from .commands import start, help, about


@Client.on_callback_query()
async def cb_data(_, message):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    if message.data.startswith("admin"):
        await admin_cb_data(_, message)
        return
    
    for module in MODULES:
        if message.data.startswith(module):
            await MODULES[module]["cb_data"](_, message)
            return
    
    if message.data == "home":
        await start(_, message, cb=True)
    elif message.data == "help":
        await help(_, message, cb=True)
    elif message.data == "about":
        await about(_, message, cb=True)
    else:
        await message.message.delete()