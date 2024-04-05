from .commands import dictionary_help


async def dictionary_cb_data(_, message):
    
    if message.data.startswith("dictionary"):
        data = message.data.split("-", 1)[1]
    else:
        return
    
    if data == "help":
        await dictionary_help(_, message, cb=True)
