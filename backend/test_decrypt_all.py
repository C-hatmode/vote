# decrypt_all_embeddings.py
from pymongo import MongoClient
from Crypto.Cipher import AES
import base64
import json

# 🔑 Load secret key from keysecret.py
from utils.keysecret import SECRET_KEY

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["blockchain_voting"]
voters = db["voter"]

def decrypt_embedding(ciphertext_b64, nonce_b64, tag_b64):
    try:
        ciphertext = base64.b64decode(ciphertext_b64)
        nonce = base64.b64decode(nonce_b64)
        tag = base64.b64decode(tag_b64)

        cipher = AES.new(SECRET_KEY, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)
        return json.loads(decrypted.decode("utf-8"))  # embeddings stored as JSON
    except Exception as e:
        return f"❌ Decryption failed: {str(e)}"

def main():
    for voter in voters.find():
        print(f"\n👤 Voter: {voter.get('name')} (Aadhaar: {voter.get('aadhar')})")

        embeddings = voter.get("embeddings", {})
        for view in ["front", "left", "right"]:
            if view in embeddings:
                enc = embeddings[view]
                result = decrypt_embedding(enc["ciphertext"], enc["nonce"], enc["tag"])
                if isinstance(result, dict) or isinstance(result, list):
                    print(f"   ✅ {view} embedding decrypted (length: {len(result)})")
                else:
                    print(f"   {view} → {result}")
            else:
                print(f"   ⚠️ No {view} embedding found.")

if __name__ == "__main__":
    main()
