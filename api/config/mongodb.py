"""DATABASE
MongoDB database initialization
"""

# # Installed # #
import motor.motor_asyncio
import os


# # Package # #
__all__ = ("client","db", "job_collection")


# # Local # #
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.test_db
job_collection = db.get_collection("jobs")
