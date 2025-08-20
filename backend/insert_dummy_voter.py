import numpy as np
from pymongo import MongoClient
from utils.face_utils import encrypt_face_embedding
from utils.keysecret import SECRET_KEY

# 1. Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["blockchain_voting"]   # adjust if your DB name is different
voters = db["voter"]

# 2. Create dummy face embedding (128 floats like face_recognition)
dummy_embedding = np.random.rand(128)

# 3. Encrypt the embedding using your existing function
encrypted_embedding = encrypt_face_embedding(dummy_embedding)

# 4. Insert a dummy voter document
dummy_voter = {
    "aadhaar": "999999999999",   # test Aadhaar
    "name": "Test Voter",
    "face_embedding": encrypted_embedding
}

voters.insert_one(dummy_voter)
print("✅ Dummy voter with encrypted embedding inserted!")
