import base64
from utils.keysecret import SECRET_KEY
from pymongo import MongoClient
from Crypto.Cipher import AES
import numpy as np

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["blockchain_voting"]
voters = db["voter"]

aadhaar = "221051060"
voter = voters.find_one({"aadhaar": aadhaar})

if not voter:
    print(f"❌ No voter found with Aadhaar {aadhaar}")
    exit()

print(f"✅ Found voter: {voter['name']} (Aadhaar: {aadhaar})")

# Candidate key formats to test
keys_to_try = {
    "raw SECRET_KEY": SECRET_KEY,
    "base64 decoded": base64.b64decode("s1QRxVco6D+wz5mjhhwO+cwMiBmN75DPhDzs0UTOKtU="),
    "utf-8 bytes": "s1QRxVco6D+wz5mjhhwO+cwMiBmN75DPhDzs0UTOKtU=".encode("utf-8"),
}

# Pick encrypted embedding from Mongo
enc_front = voter.get("face_embeddings", {}).get("front")

if not enc_front:
    print("❌ No 'front' embedding found for this voter")
    exit()

for label, key in keys_to_try.items():
    try:
        ciphertext = base64.b64decode(enc_front["ciphertext"])
        nonce = base64.b64decode(enc_front["nonce"])
        tag = base64.b64decode(enc_front["tag"])

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)
        embedding = np.frombuffer(decrypted, dtype=np.float64)

        print(f"✅ Decryption success with [{label}] — length {len(embedding)}")
    except Exception as e:
        print(f"❌ Failed with [{label}]: {e}")
