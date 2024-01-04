import os
from typing import Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from models.client import Client
from models.apartment import Apartment
from models.reservation import Reservation

db_client: AsyncIOMotorClient = None


async def get_db_collection() -> AsyncIOMotorCollection:
    mongo_db = os.getenv('MONGO_DB')
    mongo_collection = os.getenv('MONGO_COLLECTION')

    return db_client.get_database(mongo_db).get_collection(mongo_collection)


async def connect_and_init_db():
    global db_client
    mongo_uri = "mongodb://localhost:27017"
    try:
        db_client = AsyncIOMotorClient(mongo_uri)
        await db_client.list_databases()
        print('Connected to mongo')
    except Exception as e:
        print(f'Exception was catched {e}')

async def close_db_connect():
    global db_client
    if db_client is None:
        return
    
    db_client.close()

def get_filter(id: str) -> dict:
    return {'_id': ObjectId(id)}


def map_client(client: Any) -> Client | None:
    if client is None:
        return None

    return Client(
        id=str(client['_id']), 
        name=client['name'], 
        surname=client['surname'], 
        age=int(client['age']), 
        phone=client['phone_number'], 
        email=client['email']
    )