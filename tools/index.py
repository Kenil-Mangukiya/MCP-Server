from mcp.server.fastmcp import FastMCP
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from db.db import get_db
from schemas.user import CreateUserSchema
import hashlib

mcp = FastMCP("DB_Operations")

@mcp.tool()
def create_user(data: CreateUserSchema):
    """
    Create a new user in the database.
    """
    db = get_db()
    user_collection = db["users"]

    hashed_password = hashlib.sha256(data.password.encode()).hexdigest()

    create_user = {
        "username": data.username,
        "email": data.email,
        "password": hashed_password
    }

    try:
        result = user_collection.insert_one(create_user)
        print(f"Result is : {result}")
    except DuplicateKeyError:
        return {
            "success": False,
            "message": "User with this email already exists"
        }
    
    return {
        "success": True,
        "message": str(result.inserted_id)
    }

