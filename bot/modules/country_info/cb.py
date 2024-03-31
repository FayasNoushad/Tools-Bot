from .commands import country_help


async def country_cb_data(_, message):
    
    if message.data.startswith("country"):
        data = message.data.split("-", 1)[1]
    else:
        return
    
    if data == "help":
        await country_help(_, message, cb=True)
