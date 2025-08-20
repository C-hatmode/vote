# test_mongo_decrypt.py
import pymongo
from utils.face_utils import decrypt_face_embedding
from utils.keysecret import SECRET_KEY

# 🔗 Connect to MongoDB (update URI if needed)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["blockchain_voting"]   # change if your DB has a different name
voters_collection = db["voter"]

# Aadhaar number of the voter you want to test
aadhaar_to_test = "221051060"   # change to a real Aadhaar in your DB

# Fetch voter
voter = voters_collection.find_one({"aadhaar": aadhaar_to_test})

if not voter:
    print(f"❌ No voter found with Aadhaar {aadhaar_to_test}")
    exit()

print(f"✅ Found voter: {voter['name']} (Aadhaar: {voter['aadhaar']})")

embeddings = voter.get("embeddings", {})
if not embeddings:
    print("❌ No embeddings found for this voter")
    exit()

# Try decrypting one embedding (front)
if "front" in embeddings:
    try:
        decrypted = decrypt_face_embedding(embeddings["front"])
        print("✅ Successfully decrypted 'front' embedding")
        print("📏 Embedding length:", len(decrypted))
        print("🔹 First 5 values:", decrypted[:5])
    except Exception as e:
        print("❌ Failed to decrypt 'front':", str(e))
else:
    print("❌ No 'front' embedding stored for this voter")
