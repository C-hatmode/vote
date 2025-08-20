# check_voter.py
import os
import base64
import numpy as np
from pymongo import MongoClient
from utils.face_utils import decrypt_face_embedding, get_face_embedding
import face_recognition

# ------------------------------
# DB Setup
# ------------------------------
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "blockchain_voting"
COLLECTION_NAME = "voter"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

print("\n🔎 Checking voter embeddings...")

# ------------------------------
# Test Image for Matching
# ------------------------------
TEST_IMAGE_PATH = "C:\\Users\\Admin\\OneDrive\\Pictures\\Camera Roll 1\\WIN_20250819_19_25_18_Pro.jpg"  # 👈 put your test image here

if not os.path.exists(TEST_IMAGE_PATH):
    print(f"⚠️ Test image '{TEST_IMAGE_PATH}' not found. Please add one.")
    exit()

# Compute embedding for the test image
test_embedding = get_face_embedding(TEST_IMAGE_PATH)
if test_embedding is None:
    print("❌ Could not extract embedding from test image.")
    exit()

# ------------------------------
# Iterate Voters
# ------------------------------
for voter in collection.find({}):
    name = voter.get("name")
    aadhaar = voter.get("aadhaar")
    enc_embedding = voter.get("face_embedding")

    print(f"\n👤 Voter: {name} (Aadhaar: {aadhaar})")

    if not enc_embedding:
        print("   ⚠️ No face embeddings found (image not provided).")
        continue

    try:
        # Decrypt embedding
        decrypted_embedding = decrypt_face_embedding(enc_embedding)

        # Compare with test image embedding
        match = face_recognition.compare_faces(
            [decrypted_embedding], test_embedding, tolerance=0.6
        )[0]

        print(f"   🔹 Decrypted embedding (first 5): {np.round(decrypted_embedding[:5], 4)}")
        if match:
            print("   ✅ MATCH: Test image belongs to this voter!")
        else:
            print("   ❌ NO MATCH: Test image does not match this voter.")

    except Exception as e:
        print(f"   ❌ Error decrypting or matching: {str(e)}")
