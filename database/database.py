import time
import pymongo
from pyrogram.types import Message
from config import DB_URI, DB_NAME

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]

user_data = database['users']
puser_collection = database["puser"]
admins_collection = database['admins']

def new_user(id):
    return {
        '_id': id,
        'premium':False
    }

async def present_user(user_id: int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def get_user(user_id: int):
    return user_data.find_one({'_id': user_id})

async def add_user(user_id: int):
    user = new_user(user_id)
    user_data.insert_one(user)  # Simply pass the full user object
    return


async def full_userbase():
    user_docs = user_data.find()
    user_ids = [doc['_id'] for doc in user_docs]
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

async def add_admin(user_id: int):
    try:
        admins_collection.insert_one({'_id': user_id})
        return True
    except Exception as e:
        print(f"Failed to add admin: {e}")
        return False

# Function to remove aa user from admin
async def remove_admin(user_id: int):
    try:
        admins_collection.delete_one({'_id': user_id})
        return True
    except Exception as e:
        print(f"Failed to remove admin: {e}")
        return False

# Function to check if a user is an admin
async def is_admin(user_id: int):
    return bool(admins_collection.find_one({'_id': user_id}))

async def get_admin_list():
    admin_docs = admins_collection.find()
    admin_ids = [doc['_id'] for doc in admin_docs]
    return admin_ids

# Function to check premium expire time
async def expire_premium_user(user_id: int, message: Message):
    current_ts = int(time.time())

    puser = puser_collection.find_one({"user_id": user_id})

    if puser:
        if puser.get("expire_timestamp", 0) < current_ts:
            user_data.update_one(
                {"_id": user_id},
                {
                    "$set": {
                        "premium": False
                    }
                }
            )
            puser_collection.delete_one({"user_id": user_id})
            await message.reply("🎀 Yᴏᴜʀ Pʀᴇᴍɪᴜᴍ Mᴇᴍʙᴇʀsʜɪᴘ ʜᴀs ʙᴇᴇɴ Exᴘɪʀᴇᴅ ❗❗❗")
    else:
        user_data.update_one(
            {"_id": user_id},
            {
                "$set": {
                        "premium": False,
                        "verify_status.is_verified": False
                    }
            }
        )

