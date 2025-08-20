import numpy as np
from utils.face_utils import encrypt_face_embedding, decrypt_face_embedding

# Fake embedding (simulate what face_recognition would produce)
original_embedding = np.random.rand(128)  # 128-d face vector

print("🔹 Original Embedding (first 5 values):", original_embedding[:5])

# Encrypt
enc_data = encrypt_face_embedding(original_embedding)
print("✅ Encrypted data keys:", list(enc_data.keys()))

# Decrypt
decrypted_embedding = decrypt_face_embedding(enc_data)
print("🔹 Decrypted Embedding (first 5 values):", decrypted_embedding[:5])

# Verify
if np.allclose(original_embedding, decrypted_embedding, atol=1e-8):
    print("🎉 SUCCESS: Encryption/Decryption is working correctly with AES-EAX!")
else:
    print("❌ ERROR: Mismatch between original and decrypted embedding")
