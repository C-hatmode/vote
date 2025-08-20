from database.connection import votes_collection
import hashlib
from datetime import datetime
import uuid

class VoteModel:
    @staticmethod
    def cast(voter_id: str, candidate_id: str):
        # Hash the voter_id (usually Aadhaar) for anonymity
        hashed_voter = hashlib.sha256(voter_id.encode()).hexdigest()
        blockchain_ref = str(uuid.uuid4())

        vote = {
            "voter_id": hashed_voter,
            "candidate_id": candidate_id,
            "blockchain_ref": blockchain_ref,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        votes_collection.insert_one(vote)
        return blockchain_ref

    @staticmethod
    def list_all():
        return list(votes_collection.find({}, {"_id": 0}))
