from ...database import db
from .commands import qr_help
from .settings import display_settings


async def qr_cb_data(_, message):
    
    if message.data.startswith("qr"):
        data = message.data.split("-", 1)[1]
    else:
        return
    
    if data == "help":
        await qr_help(_, message, cb=True)
    
    elif data == "lol":
        await message.answer(text="Select a button below")
        
    elif data == "settings":
        await display_settings(_, message, cb=True)
        
    elif data == "set_af":
        as_file = await db.is_qr_as_file(message.from_user.id)
        new_type = not as_file # true or false
        await db.update_qr_as_file(message.from_user.id, new_type)
        if new_type:
            alert_text = "Upload mode changed to file successfully"
        else:
            alert_text = "Upload mode changed to photo successfully"
        await message.answer(text=alert_text, show_alert=True)
        try:
            await display_settings(_, message, cb=True)
        except Exception as error:
            if 'MESSAGE_NOT_MODIFIED' in str(error):
                return
            print(error)
