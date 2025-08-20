import base64

# your raw key string (Base64URL)
key_str = "s1QRxVco6D-wz5mjhhwO-cwMiBmN75DPhDzs0UTOKtU=32"

# ✅ decode using URL-safe base64
SECRET_KEY = base64.urlsafe_b64decode(key_str)

# Debug check
if len(SECRET_KEY) != 32:
    raise ValueError(f"❌ SECRET_KEY must be 32 bytes, got {len(SECRET_KEY)}")
