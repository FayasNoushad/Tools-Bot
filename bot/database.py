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
            qr_as_file=False,
            dictionary=dict(
                phonetics=dict(
                    phonetics=True,
                    text=True,
                    audio=True
                ),
                origin=True,
                meanings=dict(
                    meanings=True,
                    part_of_speech=True,
                    definitions=True,
                    example=True,
                    synonyms=False,
                    antonyms=False
                )
            )
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

    # returns True, if user is an authorised user
    # returns False, if user is not an authorised user
    async def is_authorised(self, id):
        user = await self.get_user(id)
        return user.get("auth", False)
    
    # authorise
    async def authorise(self, id):
        if id not in self.cache:
            self.cache[id] = await self.get_user(id)
        self.cache[id]["auth"] = True
        await self.col.update_one({"id": id}, {"$set": {"auth": True}})
    
    # unauthorise
    async def unauthorise(self, id):
        if id not in self.cache:
            self.cache[id] = await self.get_user(id)
        await self.col.update_one({"id": id}, {"$set": {"auth": False}})
    
    # get authorised users ids
    async def get_auth_users(self):
        auth_users = []
        async for user in self.col.find({"auth": True}):
            auth_users.append(user["id"])
        return auth_users
    
    # get gemini api key to using ai
    async def get_gemini_api(self, id):
        user = await self.get_user(id)
        return user.get("gemini_api", None)

    # add/update gemini api key
    async def update_gemini_api(self, id, api):
        if id not in self.cache:
            self.cache[id] = await self.get_user(id)
        self.cache[id]["gemini_api"] = api
        await self.col.update_one({"id": id}, {"$set": {"gemini_api": api}})
    
    # get translation language to translate
    async def get_tr_lang(self, id):
        user = await self.get_user(id)
        return user.get("tr_lang", "en")
    
    # update translation language
    async def update_tr_lang(self, id, language):
        if id not in self.cache:
            self.cache[id] = await self.get_user(id)
        self.cache[id]["tr_lang"] = language
        await self.col.update_one({"id": id}, {"$set": {"tr_lang": language}})
    
    # to upload qr code (as photo or file)
    async def is_qr_as_file(self, id):
        user = await self.get_user(id)
        return user.get("qr_as_file", False)

    # update qr code upload mode (photo or file)
    async def update_qr_as_file(self, id, as_file):
        if id not in self.cache:
            self.cache[id] = await self.get_user(id)
        self.cache[id]["qr_as_file"] = as_file
        await self.col.update_one({"id": id}, {"$set": {"qr_as_file": as_file}})
    
    # to get dictionary settings
    async def get_dictionary(self, id):
        user = await self.get_user(id)
        return user.get("dictionary", self.new_user(id)["dictionary"])
    
    # to get dictionary phonetics
    async def get_phonetics(self, id):
        user = await self.get_user(id)
        return user["dictionary"]["phonetics"]["phonetics"]
    
    # to update dictionary phonetics
    async def update_phonetics(self, id, phonetics):
        if id not in self.cache:
            self.cache[id] = await self.get_user(id)
        self.cache[id]["dictionary"]["phonetics"]["phonetics"] = phonetics
        await self.col.update_one({"id": id}, {"$set": {"dictionary.phonetics.phonetics": phonetics}})
    
    # to get dictionary phonetics text
    async def get_phonetics_text(self, id):
        user = await self.get_user(id)
        return user["dictionary"]["phonetics"]["text"]
    
    # to update dictionary phonetics text
    async def update_phonetics_text(self, id, text):
        if id not in self.cache:
            self.cache[id] = await self.get_user(id)
        self.cache[id]["dictionary"]["phonetics"]["text"] = text
        await self.col.update_one({"id": id}, {"$set": {"dictionary.phonetics.text": text}})
    
    # to get dictionary phonetics audio
    async def get_phonetics_audio(self, id):
        user = await self.get_user(id)
        return user["dictionary"]["phonetics"]["audio"]
    
    # to update dictionary phonetics audio
    async def update_phonetics_audio(self, id, audio):
        if id not in self.cache:
            self.cache[id] = await self.get_user(id)
        self.cache[id]["dictionary"]["phonetics"]["audio"] = audio
        await self.col.update_one({"id": id}, {"$set": {"dictionary.phonetics.audio": audio}})
    
    # to get dictionary origin
    async def get_origin(self, id):
        user = await self.get_user(id)
        return user["dictionary"]["origin"]
    
    # to update dictionary origin
    async def update_origin(self, id, origin):
        if id not in self.cache:
            self.cache[id] = await self.get_user(id)
        self.cache[id]["dictionary"]["origin"] = origin
        await self.col.update_one({"id": id}, {"$set": {"dictionary.origin": origin}})
    
    # to get dictionary meanings
    async def get_meanings(self, id):
        user = await self.get_user(id)
        return user["dictionary"]["meanings"]["meanings"]
    
    # to update dictionary meanings
    async def update_meanings(self, id, meanings):
        if id not in self.cache:
            self.cache[id] = await self.get_user(id)
        self.cache[id]["dictionary"]["meanings"]["meanings"] = meanings
        await self.col.update_one({"id": id}, {"$set": {"dictionary.meanings.meanings": meanings}})
    
    # to get dictionary part of speech
    async def get_part_of_speech(self, id):
        user = await self.get_user(id)
        return user["dictionary"]["meanings"]["part_of_speech"]
    
    # to update dictionary part of speech
    async def update_part_of_speech(self, id, part_of_speech):
        if id not in self.cache:
            self.cache[id] = await self.get_user(id)
        self.cache[id]["dictionary"]["meanings"]["part_of_speech"] = part_of_speech
        await self.col.update_one({"id": id}, {"$set": {"dictionary.meanings.part_of_speech": part_of_speech}})
    
    # to get dictionary definitions
    async def get_definitions(self, id):
        user = await self.get_user(id)
        return user["dictionary"]["meanings"]["definitions"]
    
    # to update dictionary definitions
    async def update_definitions(self, id, definitions):
        if id not in self.cache:
            self.cache[id] = await self.get_user(id)
        self.cache[id]["dictionary"]["meanings"]["definitions"] = definitions
        await self.col.update_one({"id": id}, {"$set": {"dictionary.meanings.definitions": definitions}})
    
    # to get dictionary example
    async def get_example(self, id):
        user = await self.get_user(id)
        return user["dictionary"]["meanings"]["example"]
    
    # to update dictionary example
    async def update_example(self, id, example):
        if id not in self.cache:
            self.cache[id] = await self.get_user(id)
        self.cache[id]["dictionary"]["meanings"]["example"] = example
        await self.col.update_one({"id": id}, {"$set": {"dictionary.meanings.example": example}})
    
    # to get dictionary synonyms
    async def get_synonyms(self, id):
        user = await self.get_user(id)
        return user["dictionary"]["meanings"]["synonyms"]
    
    # to update dictionary synonyms
    async def update_synonyms(self, id, synonyms):
        if id not in self.cache:
            self.cache[id] = await self.get_user(id)
        self.cache[id]["dictionary"]["meanings"]["synonyms"] = synonyms
        await self.col.update_one({"id": id}, {"$set": {"dictionary.meanings.synonyms": synonyms}})
    
    # to get dictionary antonyms
    async def get_antonyms(self, id):
        user = await self.get_user(id)
        return user["dictionary"]["meanings"]["antonyms"]
    
    # to update dictionary antonyms
    async def update_antonyms(self, id, antonyms):
        if id not in self.cache:
            self.cache[id] = await self.get_user(id)
        self.cache[id]["dictionary"]["meanings"]["antonyms"] = antonyms
        await self.col.update_one({"id": id}, {"$set": {"dictionary.meanings.antonyms": antonyms}})


db = Database()
