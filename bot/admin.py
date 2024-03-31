from .database import db
from vars import AUTH, ADMINS
from .help import MORE_HELP_ONLY
from pyrogram import Client, filters


ADMIN_HELP = """
--**Admin Help**--

/auth: To authorise a user
/unauth: To unauthorise a user
/auth_users: To get authorised users
/admins: To get all admins
"""

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


# admin help
@Client.on_message(filters.private & filters.command(["admin_help"]))
async def admin_help(_, message):
        
        # Checking admin or not
        if message.from_user.id not in ADMINS:
            return
        
        await message.reply_text(
            text=ADMIN_HELP,
            quote=True,
            reply_markup=MORE_HELP_ONLY
        )


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
async def unauthorise(_, message):
    
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


# get authorised users
@Client.on_message(filters.command(["auth_users", "authorised_users"]))
async def get_auth_users(bot, message):
    
    # Checking admin or not
    if message.from_user.id not in ADMINS:
        return
    
    m = await message.reply_text("Getting authorised users...", quote=True)
    
    try:
        auth_users = await db.get_auth_users()
        if len(auth_users) == 0:
            await m.edit_text("No authorised users found.")
            return
        text = "Authorised Users\n"
        for auth_user in auth_users:
            user = await bot.get_users(auth_user)
            text += f"\n{user.mention} (`{str(user.id)}`)"
        await m.edit_text(text)
    except Exception as error:
        print(error)
        await m.edit_text("Something wrong.")


# get all admins
@Client.on_message(filters.command(["admins"]))
async def get_admins(bot, message):
    
    # Checking admin or not
    if message.from_user.id not in ADMINS:
        return
    
    m = await message.reply_text("Getting all admins...", quote=True)
    
    try:
        text = "Admins\n"
        for admin in ADMINS:
            user = await bot.get_users(admin)
            text += f"\n{user.mention} (`{str(user.id)}`)"
        await m.edit_text(text)
    except Exception as error:
        print(error)
        await m.edit_text("Something wrong.")
