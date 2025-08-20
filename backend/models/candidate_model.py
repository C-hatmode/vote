from database.connection import db
from bson import ObjectId

class CandidateModel:
    @staticmethod
    def register_candidate(data):
        if "votes" not in data:
            data["votes"] = 0
        db.candidate.insert_one(data)  # use 'candidate' collection

    @staticmethod
    def get_all():
        candidates = list(db.candidate.find({}, {"password": 0}))  # use 'candidate' collection
        for candidate in candidates:
            candidate["_id"] = str(candidate["_id"])
        return candidates

    @staticmethod
    def get_by_email(email):
        candidate = db.candidate.find_one({"email": email}, {"password": 0})
        if candidate:
            candidate["_id"] = str(candidate["_id"])
        return candidate

    @staticmethod
    def find_by_id(candidate_id):
        try:
            candidate = db.candidate.find_one({"_id": ObjectId(candidate_id)})
            if candidate:
                candidate["_id"] = str(candidate["_id"])
            return candidate
        except:
            return None

    @staticmethod
    def increment_vote(candidate_id):
        try:
            db.candidate.update_one(
                {"_id": ObjectId(candidate_id)},
                {"$inc": {"votes": 1}}
            )
            return True
        except:
            return False

    # Get candidates by region (assembly location)
    @staticmethod
    def find_by_region(region):
        candidates = list(db.candidate.find({"region": region}))
        for candidate in candidates:
            candidate["_id"] = str(candidate["_id"])
        return candidates
