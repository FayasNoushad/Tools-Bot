from .database import db
from vars import AUTH, ADMINS
from pyrogram import Client, filters


async def add_user(id):
    if not await db.is_user_exist(id):
        await db.add_user(id)
    return


async def auth(id):
    await add_user(id)
    authorised = (await db.is_authorised(id))
    if AUTH and ((id in ADMINS) or authorised):
        return True
    else:
        return False


# authorise user via database
@Client.on_message(filters.command(["auth", "authorise"]))
async def authorise(_, message):
    
    # Checking admin or not
    if message.from_user.id not in ADMINS:
        return
    
    m = await message.reply_text("Authorising...", quote=True)
    
    # avoid command only
    if (" " not in message.text):
        await m.edit_text("No ids found")
        return
    
    # for one or more than one ids
    ids_list = message.text.split(" ", 1)[1]
    ids = set(int(i) for i in ids_list.split())
    
    for id in ids:
        try:
            await db.authorise(id)
        except Exception as error:
            print(error)
    
    try:
        await m.edit_text("Authorised successfully.")
    except:
        pass


# unauthorise user via database
@Client.on_message(filters.command(["unauth", "unauthorise"]))
async def authorise(_, message):
    
    # Checking admin or not
    if message.from_user.id not in ADMINS:
        return
    
    m = await message.reply_text("Unauthorising...", quote=True)
    
    # avoid command only
    if (" " not in message.text):
        await m.edit_text("No ids found")
        return
    
    # for one or more than one ids
    ids_list = message.text.split(" ", 1)[1]
    ids = set(int(i) for i in ids_list.split())
    
    for id in ids:
        try:
            await db.unauthorise(id)
        except Exception as error:
            print(error)
    
    try:
        await m.edit_text("Unauthorised successfully.")
    except:
        pass
