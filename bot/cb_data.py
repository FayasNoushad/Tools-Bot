from pyrogram import Client
from .modules.ytthumb import ytthumb_cb_data
from .commands import start, help, about


@Client.on_callback_query()
async def cb_data(_, update):
    if update.data.startswith("ytthumb"):
        await ytthumb_cb_data(_, update)
        return
    if update.data == "home":
        await start(_, update, cb=True)
    elif update.data == "help":
        await help(_, update, cb=True)
    elif update.data == "about":
        await about(_, update, cb=True)
    else:
        await update.message.delete()