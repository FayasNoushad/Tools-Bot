from vars import DATABASE_URL, DATABASE_NAME
import motor.motor_asyncio


class Database:
    def __init__(self, url=DATABASE_URL, database_name=DATABASE_NAME):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(url)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.cache = {}
    
    def new_user(self, id):
        return dict(
            id=id,
            auth=False,
            gemini_api=None,
            tr_lang="en",
            qr_as_file=False
        )
    
    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)
    
    async def get_user(self, id):
        user = self.cache.get(id)
        if user is not None:
            return user
        
        user = await self.col.find_one({"id": int(id)})
        self.cache[id] = user
        return user
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return True if user else False
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
    
    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users
    
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def is_authorised(self, id):
        user = await self.get_user(id)
        return user.get("auth", False)
    
    async def authorise(self, id):
        if id not in self.cache:
            self.cache[id] = await self.get_user(id)
        self.cache[id]["auth"] = True
        await self.col.update_one({"id": id}, {"$set": {"auth": True}})
    
    async def unauthorise(self, id):
        await self.col.update_one({"id": id}, {"$set": {"auth": False}})
    
    async def get_gemini_api(self, id):
        user = await self.get_user(id)
        return user.get("gemini_api", None)

    async def update_gemini_api(self, id, api):
        await self.col.update_one({"id": id}, {"$set": {"gemini_api": api}})
    
    async def get_tr_lang(self, id):
        user = await self.get_user(id)
        return user.get("tr_lang", "en")
    
    async def update_tr_lang(self, id, language):
        await self.col.update_one({"id": id}, {"$set": {"tr_lang": language}})
    
    async def is_qr_as_file(self, id):
        user = await self.get_user(id)
        return user.get("as_file", False)

    async def update_qr_as_file(self, id, as_file):
        await self.col.update_one({"id": id}, {"$set": {"as_file": as_file}})


db = Database()
