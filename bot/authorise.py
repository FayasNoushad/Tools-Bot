from .database import db
from vars import AUTH, ADMINS


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
