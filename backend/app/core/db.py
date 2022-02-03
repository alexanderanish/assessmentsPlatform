import os

import motor.motor_asyncio
from fastapi_users.db import MongoDBUserDatabase

from app.users.models import UserDB


DATABASE_URL = os.environ["DATABASE_URL"]
#DATABASE_URL='mongodb://localhost:27017'
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["assessment_platform"]
collection_user = db["users"]


async def get_user_db():
    yield MongoDBUserDatabase(UserDB, collection_user)