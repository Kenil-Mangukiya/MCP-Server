from mcp.server.fastmcp import FastMCP
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from db.db import get_db
from schemas.user import CreateUserSchema, UpdateUserSchema
import hashlib
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
    force=True
)

logger = logging.getLogger(__name__)


mcp = FastMCP("DB_Operations")

@mcp.tool()
def create_user(data: CreateUserSchema):
    """
    Create a new user in the database.
    """
    logger.info("Create user tool is called")
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
        logger.info(f"Result from create tool is : {result}")
    except DuplicateKeyError:
        return {
            "success": False,
            "message": "User with this email already exists"
        }
    
    return {
        "success": True,
        "message": str(result.inserted_id)
    }

@mcp.tool()
def fetch_all_users():
    """
    Fetch all users from the database
    """
    try:
        db = get_db()
        user_collection = db["users"]
        users = []
        for user in user_collection.find():
            users.append({
                "id": str(user["_id"]),
                "username": user.get("username"),
                "email": user.get("email")
            })
        return {
            "success": True,
            "message": f"Total users in the database are: {len(users)}",
            "users": users
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        } 

@mcp.tool()
def update_user(data: UpdateUserSchema):
    """
    Update user by id
    """
    try:
        db = get_db()
        user_collection = db["users"]
        update_data = {}
        
        if data.username is not None:
            update_data["username"] = data.username
        if data.password is not None:
            update_data["password"] = hashlib.sha256(
            data.password.encode()
        ).hexdigest()
            
        if not update_data:
            return {
                "success": False,
                "message": "No data provided to update"
            }
        result = user_collection.update_one({"email": data.email},
                                            {
                                                "$set": update_data
                                            }
                                            )
        if result.matched_count == 0:
            return {
                "success": False,
                "message": f"No user found for emailID: {data.email}"
            }
        return {
            "success": True,
            "message": "User updated successully",
            "updated_user": result
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }

if __name__ == "__main__":
    mcp.run()


