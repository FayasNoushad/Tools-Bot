from ...database import db
from .commands import dictionary_help
from .settings import display_settings


async def dictionary_cb_data(_, message):
    
    if message.data.startswith("dictionary"):
        data = message.data.split("-", 1)[1]
    else:
        return
    
    if message.data.startswith("dictionary"):
        data = message.data.split("-", 1)[1]
    else:
        return
    
    if data == "help":
        await dictionary_help(_, message, cb=True)
        
    elif data == "settings":
        await display_settings(_, message, cb=True)
    
    elif data == "set_phonetics":
        phonetics = await db.get_phonetics(message.from_user.id)
        new_type = not phonetics
        await db.update_phonetics(message.from_user.id, new_type)
        if new_type:
            alert_text = "Phonetics enabled successfully"
        else:
            alert_text = "Phonetics disabled successfully"
        await message.answer(text=alert_text, show_alert=True)
        try:
            await display_settings(_, message, cb=True)
        except Exception as error:
            if 'MESSAGE_NOT_MODIFIED' in str(error):
                return
            print(error)
    elif data == "set_origin":
        origin = await db.get_origin(message.from_user.id)
        new_type = not origin
        await db.update_origin(message.from_user.id, new_type)
        if new_type:
            alert_text = "Origin enabled successfully"
        else:
            alert_text = "Origin disabled successfully"
        await message.answer(text=alert_text, show_alert=True)
        try:
            await display_settings(_, message, cb=True)
        except Exception as error:
            if 'MESSAGE_NOT_MODIFIED' in str(error):
                return
            print(error)
    elif data == "set_meanings":
        meanings = await db.get_meanings(message.from_user.id)
        new_type = not meanings
        await db.update_meanings(message.from_user.id, new_type)
        if new_type:
            alert_text = "Meanings enabled successfully"
        else:
            alert_text = "Meanings disabled successfully"
        await message.answer(text=alert_text, show_alert=True)
        try:
            await display_settings(_, message, cb=True)
        except Exception as error:
            if 'MESSAGE_NOT_MODIFIED' in str(error):
                return
            print(error)
