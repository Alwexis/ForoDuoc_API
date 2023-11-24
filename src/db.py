import motor.motor_asyncio

DB_URL = "mongodb+srv://CITT2023:CITT2023@cluster0.uzcxf.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "CITT2023"

class DB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DB, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
        self.db = self.client[DB_NAME]
    
    async def get(self, collection, query = {}):
        # El segundo parámetro excluye el campo _id de los resultados.
        print(query)
        return await self.db[collection].find(query, { '_id': 0 }).to_list(None)
    
    async def insert(self, collection, document):
        return await self.db[collection].insert_one(document)

    async def insert_many(self, collection, document):
        return await self.db[collection].insert_many(document)
    
    async def update(self, collection, query, document):
        return await self.db[collection].update_one(query, { '$set': document })
    
    async def delete(self, collection, query):
        return await self.db[collection].delete_one(query)