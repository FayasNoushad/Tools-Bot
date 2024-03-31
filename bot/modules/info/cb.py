from .commands import info_help


async def info_cb_data(_, message):
    
    if message.data.startswith("info"):
        data = message.data.split("-", 1)[1]
    else:
        return
    
    if data == "help":
        await info_help(_, message, cb=True)
