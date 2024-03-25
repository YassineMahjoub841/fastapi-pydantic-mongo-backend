"""DATABASE
MongoDB database initialization
"""

# # Installed # #
#import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from beanie import init_beanie
from .. import models as models
from ..models import JobModel


# # Package # #
#__all__ = ("initiate_database")


# # Local # #
#client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
#db = client.test_db
#job_collection = db.get_collection("jobs")

async def initiate_database():
    """
    Asynchronously initializes the database by setting up the client through Motor and initializing Beanie with the specified document models.

    Returns:
        None
    """
    #Set up client through Motor
    client = AsyncIOMotorClient(os.environ["MONGODB_URL"])

    #Set up beanie & the document models
    await init_beanie(
        database=client.test_db, document_models=[JobModel]
    )