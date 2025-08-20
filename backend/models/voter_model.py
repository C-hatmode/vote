from database.connection import voters_collection
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class VoterModel:
    @staticmethod
    def register_voter(data):
        # Initialize has_voted field
        if "has_voted" not in data:
            data["has_voted"] = False

        # ✅ Hash the password before saving
        if "password" in data:
            data["password"] = generate_password_hash(data["password"])

        voters_collection.insert_one(data)
        return True

    @staticmethod
    def find_by_aadhaar(aadhaar):
        return voters_collection.find_one({"aadhaar": aadhaar})
    
    @staticmethod
    def find_by_email(email):
        return voters_collection.find_one({"email": email})

    @staticmethod
    def verify_password(stored_password, provided_password):
        """Check if provided password matches stored hash"""
        return check_password_hash(stored_password, provided_password)
    
    @staticmethod
    def get_all():
        voters = list(voters_collection.find({}, {"password": 0}))  # exclude passwords
        for voter in voters:
            voter["_id"] = str(voter["_id"])
        return voters
