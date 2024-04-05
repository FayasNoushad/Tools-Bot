from pyrogram import Client
from .help import MODULES
from .authorise import auth
from .admin import admin_help
from .commands import start, help, about


@Client.on_callback_query()
async def cb_data(_, message):
    
    # authorising
    if not (await auth(message.from_user.id)):
        return
    
    if message.data.startswith("admin"):
        data = message.data.split("-", 1)[1]
        if data == "help":
            await admin_help(_, message, cb=True)
    
    for module in MODULES:
        if message.data.startswith(module):
            data = message.data.split("-", 1)[1]
            if data == "help":
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