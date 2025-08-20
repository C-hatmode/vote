import numpy as np
import face_recognition
from Crypto.Cipher import AES
import base64
import io
from PIL import Image
from utils.keysecret import SECRET_KEY   # ✅ AES-256 key (must be 32 bytes)

# ------------------------------
# Face Embedding (handles base64)
# ------------------------------
def get_face_embedding(image_input):
    try:
        # If it's a base64 string
        if isinstance(image_input, str) and image_input.startswith("data:image"):
            # Remove prefix like "data:image/jpeg;base64,"
            image_base64 = image_input.split(",")[1]
            image_data = base64.b64decode(image_base64)

            # Open image from memory
            image = Image.open(io.BytesIO(image_data)).convert("RGB")
            image_np = np.array(image)
        else:
            # Otherwise assume it's a file path
            image_np = face_recognition.load_image_file(image_input)

        # Extract face embeddings
        encodings = face_recognition.face_encodings(image_np)
        if len(encodings) > 0:
            return encodings[0]   # ✅ return NumPy array (not list)
        return None

    except Exception as e:
        print("❌ Error in get_face_embedding:", str(e))
        return None

# ------------------------------
# Encryption (EAX mode, same as registration form)
# ------------------------------
def encrypt_face_embedding(embedding):
    data = np.array(embedding, dtype=np.float64).tobytes()
    cipher = AES.new(SECRET_KEY, AES.MODE_EAX)  # ✅ use EAX instead of GCM
    ciphertext, tag = cipher.encrypt_and_digest(data)

    return {
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
        "nonce": base64.b64encode(cipher.nonce).decode("utf-8"),
        "tag": base64.b64encode(tag).decode("utf-8")
    }


def decrypt_face_embedding(enc_data):
    ciphertext = base64.b64decode(enc_data["ciphertext"])
    nonce = base64.b64decode(enc_data["nonce"])
    tag = base64.b64decode(enc_data["tag"])

    cipher = AES.new(SECRET_KEY, AES.MODE_EAX, nonce=nonce)  # ✅ use EAX
    decrypted = cipher.decrypt_and_verify(ciphertext, tag)

    return np.frombuffer(decrypted, dtype=np.float64)
