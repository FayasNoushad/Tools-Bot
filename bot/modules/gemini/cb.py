from ...database import db
from .commands import gemini_help


async def gemini_cb_data(_, message):
    
    m = message.message
    if message.data.startswith("gemini") or message.data.startswith("ai"):
        data = message.data.split("-", 1)[1].lower()
    else:
        return
    
    if data == "help":
        await gemini_help(_, message, cb=True)
    elif data == "confirm_delete_api":
        await m.edit_text("Deleting your Gemini API Key...")
        if await db.get_gemini_api(message.from_user.id):
            await db.update_gemini_api(message.from_user.id, None)
            await m.edit_text("API Key removed successfully")
        else:
            await m.edit_text("You haven't added your Gemini API Key")
    else:
        await m.edit_text("Cancelled the process")
