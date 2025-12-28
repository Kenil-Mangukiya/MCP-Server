import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise RuntimeError("❌ MONGODB_URI is not set in .env file")

client = MongoClient(MONGODB_URI)

db = client.get_default_database()

def get_db():
    """
    Returns the MongoDB database instance.
    This connection is reused by all MCP tools.
    """
    return db
