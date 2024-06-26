from .database import db
from vars import ADMINS
from .common import MORE_HELP_ONLY
from pyrogram import Client, filters


ADMIN_HELP = """
--**Admin Help**--

/auth: To authorise a user
/unauth: To unauthorise a user
/auth_users: To get authorised users
/admins: To get all admins
/status: To get bot status
"""


# admin help
@Client.on_message(filters.private & filters.command(["admin_help"]))
async def admin_help(_, message, cb=False):
        
        # Checking admin or not
        if message.from_user.id not in ADMINS:
            return
        
        if cb:
            await message.message.edit_text(
                text=ADMIN_HELP,
                reply_markup=MORE_HELP_ONLY,
                disable_web_page_preview=True
            )
        else:
            await message.reply_text(
                text=ADMIN_HELP,
                quote=True,
                reply_markup=MORE_HELP_ONLY
            )


async def admin_cb_data(_, message):
    if not message.data.startswith("admin"):
        return
    if message.from_user.id not in ADMINS:
        await message.answer("Only admin can use this command.", show_alert=True)
        return
    data = message.data.split("-", 1)[1]
    if data == "help":
        await admin_help(_, message, cb=True)


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

# bot status
@Client.on_message(filters.private & filters.command(["status", "bot_status"]))
async def status(bot, message):
    
    # Checking admin or not
    if message.from_user.id not in ADMINS:
        return
    
    total_users = await db.total_users_count()
    text = "**Bot Status**\n"
    text += f"\n**Total Users:** `{total_users}`"
    await message.reply_text(
        text=text,
        quote=True,
        disable_web_page_preview=True
    )
