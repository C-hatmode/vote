from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

voters_collection = db["voter"]
candidates_collection = db["candidate"]
admins_collection = db["admin"]
votes_collection = db["vote"]
