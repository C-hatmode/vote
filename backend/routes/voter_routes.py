from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.voter_model import VoterModel
from utils.face_utils import get_face_embedding, decrypt_face_embedding
from models.candidate_model import CandidateModel
from database.connection import voters_collection
from bson.objectid import ObjectId
import base64
import io
from PIL import Image
import numpy as np
import face_recognition
import bcrypt

voter_bp = Blueprint("voter", __name__, url_prefix="/voter")


# ------------------ IMAGE DECODING ------------------
def decode_base64_image(data_url):
    """Decode base64 data URL to PIL image"""
    header, encoded = data_url.split(",", 1)
    img_bytes = base64.b64decode(encoded)
    return Image.open(io.BytesIO(img_bytes))


def get_face_embedding_from_pil(image_pil):
    """Generate face embedding from PIL image"""
    img_array = np.array(image_pil)
    face_locations = face_recognition.face_locations(img_array)
    if not face_locations:
        return None
    embeddings = face_recognition.face_encodings(img_array, face_locations)
    return embeddings[0].tolist() if embeddings else None


# ------------------ VOTER REGISTRATION ------------------
@voter_bp.route("/register", methods=["POST"])
def register_voter():
    data = request.get_json(force=True)
    required_fields = [
        "name", "email", "aadhaar", "password", "phone",
        "assembly_location", "gender", "age",
        "image_front", "image_left", "image_right"
    ]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if VoterModel.find_by_aadhaar(data["aadhaar"]):
        return jsonify({"error": "Voter already registered"}), 400

    # Hash password before saving
    hashed_pw = bcrypt.hashpw(
        data["password"].encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    # Process images
    front_img = decode_base64_image(data["image_front"])
    left_img = decode_base64_image(data["image_left"])
    right_img = decode_base64_image(data["image_right"])

    front_embed = get_face_embedding_from_pil(front_img)
    left_embed = get_face_embedding_from_pil(left_img)
    right_embed = get_face_embedding_from_pil(right_img)

    if not (front_embed and left_embed and right_embed):
        return jsonify({"error": "Face not detected in all images"}), 400

    # Prepare data for MongoDB
    voter_data = {
        "name": data["name"],
        "email": data["email"],
        "aadhaar": data["aadhaar"],
        "password": hashed_pw,   # ✅ store hashed password
        "phone": data["phone"],
        "assembly_location": data["assembly_location"],
        "gender": data["gender"],
        "age": int(data["age"]),
        "images": {
            "front": data["image_front"],
            "left": data["image_left"],
            "right": data["image_right"]
        },
        "embeddings": {
            "front": front_embed,
            "left": left_embed,
            "right": right_embed
        },
        "has_voted": False
    }

    VoterModel.register_voter(voter_data)
    return jsonify({"message": "Voter registered successfully"}), 201


# ------------------ LIST VOTERS ------------------
@voter_bp.route("/list", methods=["GET"])
def list_voters():
    return jsonify({"voters": VoterModel.get_all()}), 200


# ------------------ LOGIN WITH AADHAAR + PASSWORD ------------------
@voter_bp.route("/login", methods=["POST"])
def login_voter():
    data = request.get_json()
    aadhaar = data.get("aadhaar")
    password = data.get("password")

    voter = VoterModel.find_by_aadhaar(aadhaar)
    if not voter:
        return jsonify({"error": "Voter not found"}), 404

    stored_hash = voter["password"].encode("utf-8")
    if not bcrypt.checkpw(password.encode("utf-8"), stored_hash):
        return jsonify({"error": "Invalid password"}), 401

    access_token = create_access_token(identity=aadhaar)
    return jsonify({
        "token": access_token,
        "message": "Login successful",
        "voter": {
            "aadhaar": voter["aadhaar"],
            "name": voter.get("name"),
            "email": voter.get("email"),
        }
    }), 200


# ------------------ UPDATE VOTER PROFILE ------------------
@voter_bp.route("/update/<aadhaar>", methods=["PUT"])
def update_voter(aadhaar):
    data = request.get_json(force=True)
    voter = VoterModel.find_by_aadhaar(aadhaar)
    if not voter:
        return jsonify({"error": "Voter not found"}), 404

    update_fields = {}
    for field in ["name", "email", "phone", "assembly_location"]:
        if field in data:
            update_fields[field] = data[field]

    if "password" in data:
        update_fields["password"] = bcrypt.hashpw(
            data["password"].encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    if not update_fields:
        return jsonify({"error": "No fields to update"}), 400

    voters_collection.update_one({"aadhaar": aadhaar}, {"$set": update_fields})
    return jsonify({"message": "Voter profile updated successfully"}), 200

# ------------------ GET VOTER BY AADHAAR ------------------
@voter_bp.route("/aadhaar/<aadhaar>", methods=["GET"])
def get_voter_by_aadhaar(aadhaar):
    voter = VoterModel.find_by_aadhaar(aadhaar)
    if not voter:
        return jsonify({"error": "Voter not found"}), 404
    
    voter["_id"] = str(voter["_id"])
    return jsonify(voter), 200


# ------------------ GET CURRENT VOTER PROFILE ------------------
@voter_bp.route("/me", methods=["GET"])
@jwt_required()
def get_profile():
    aadhaar = get_jwt_identity()
    voter = VoterModel.find_by_aadhaar(aadhaar)
    if not voter:
        return jsonify({"error": "Voter not found"}), 404
    voter["_id"] = str(voter["_id"])
    return jsonify(voter), 200


# ------------------ GET CANDIDATES FOR VOTER'S LOCATION ------------------
@voter_bp.route("/candidate", methods=["GET"])
@jwt_required()
def get_candidates_for_voter():
    aadhaar = get_jwt_identity()
    voter = VoterModel.find_by_aadhaar(aadhaar)
    if not voter:
        return jsonify({"error": "Voter not found"}), 404

    assembly_location = voter.get("assembly_location")
    candidates = CandidateModel.find_by_region(assembly_location)

    return jsonify({"candidates": candidates, "region": assembly_location}), 200


# ------------------ CAST VOTE ------------------
@voter_bp.route("/vote", methods=["POST"])
@jwt_required()
def vote():
    data = request.get_json(force=True)
    candidate_id = data.get("candidate_id")
    aadhaar = get_jwt_identity()

    voter = VoterModel.find_by_aadhaar(aadhaar)
    if not voter:
        return jsonify({"error": "Voter not found"}), 404
    if voter.get("has_voted"):
        return jsonify({"error": "Voter has already voted"}), 400

    candidate = CandidateModel.find_by_id(candidate_id)
    if not candidate:
        return jsonify({"error": "Candidate not found"}), 404

    if candidate.get("region") != voter.get("assembly_location"):
        return jsonify({"error": "You can only vote for candidates in your assembly location"}), 403

    voters_collection.update_one({"aadhaar": aadhaar}, {"$set": {"has_voted": True}})
    CandidateModel.increment_vote(candidate_id)

    return jsonify({"success": True, "message": "Vote cast successfully!"}), 200


# ------------------ VIEW RESULTS ------------------
@voter_bp.route("/results", methods=["GET"])
@jwt_required()
def view_results():
    aadhaar = get_jwt_identity()
    voter = VoterModel.find_by_aadhaar(aadhaar)
    if not voter:
        return jsonify({"error": "Voter not found"}), 404

    assembly_location = voter.get("assembly_location")
    candidates = CandidateModel.find_by_region(assembly_location)

    return jsonify({"region": assembly_location, "results": candidates}), 200

# ------------------ verify face ------------------
# ------------------ verify face ------------------
@voter_bp.route("/verify_face", methods=["POST"])
def verify_face():
    try:
        data = request.json
        print("📌 Incoming request data keys:", list(data.keys()))

        aadhaar = data.get("aadhaar")
        live_image = data.get("image")

        if not aadhaar:
            return jsonify({"error": "Missing aadhaar"}), 400
        if not live_image:
            return jsonify({"error": "Missing image"}), 400

        # Load voter record
        voter = voters_collection.find_one({"aadhaar": aadhaar})
        if not voter:
            return jsonify({"error": "Voter not found"}), 404

        # Get embeddings stored in DB
        embeddings = voter.get("embeddings", {})
        if not embeddings:
            return jsonify({"error": "No embeddings found for this voter"}), 404

        # Generate live embedding from uploaded image
        live_embedding = get_face_embedding(live_image)
        print("📌 Live embedding extracted?", live_embedding is not None)

        if live_embedding is None:
            return jsonify({"error": "No face detected in live image"}), 400

        match_found = False

        for pos, enc in embeddings.items():
            try:
                stored_embedding = decrypt_face_embedding(enc)
            except Exception as e:
                print(f"❌ Failed to decrypt {pos}: {e}")
                continue

            if stored_embedding is not None:
                distance = face_recognition.face_distance([stored_embedding], live_embedding)[0]
                result = face_recognition.compare_faces([stored_embedding], live_embedding, tolerance=0.6)
                print(f"➡️ Comparing {pos}: distance={distance:.4f}, match={result}")

                if result[0]:
                    match_found = True
                    break

        if match_found:
            return jsonify({"success": True, "message": "Face verified successfully"}), 200
        else:
            return jsonify({"success": False, "message": "Face verification failed"}), 401

    except Exception as e:
        print("❌ Error in verify_face:", str(e))
        return jsonify({"error": str(e)}), 500


# ------------------ FACE AUTHENTICATION LOGIN ------------------
@voter_bp.route("/face_login", methods=["POST"])
def face_login():
    try:
        data = request.json
        email = data.get("email")
        live_image = data.get("image")

        if not email or not live_image:
            return jsonify({"error": "Missing email or image"}), 400

        # Fetch voter by email
        voter = voters_collection.find_one({"email": email})
        if not voter:
            return jsonify({"error": "Voter not found"}), 404

        # Get stored embeddings
        embeddings = voter.get("embeddings", {})
        if not embeddings:
            return jsonify({"error": "No face embeddings found for this voter"}), 404

        # Generate embedding for live image
        live_embedding = get_face_embedding(live_image)
        if live_embedding is None:
            return jsonify({"error": "No face detected in live image"}), 400

        match_found = False

        for pos, enc in embeddings.items():
            try:
                stored_embedding = decrypt_face_embedding(enc)   # ✅ decrypt
            except Exception as e:
                print(f"❌ Failed to decrypt {pos}: {e}")
                continue

            if stored_embedding is not None:
                distance = face_recognition.face_distance([stored_embedding], live_embedding)[0]
                result = face_recognition.compare_faces([stored_embedding], live_embedding, tolerance=0.6)
                print(f"➡️ Face login compare {pos}: distance={distance}, match={result}")

                if result[0]:
                    match_found = True
                    break

        if match_found:
            return jsonify({"success": True, "message": "Face login successful", "voter_id": str(voter["_id"])}), 200
        else:
            return jsonify({"success": False, "message": "Face login failed"}), 401

    except Exception as e:
        print("❌ Error in face_login:", str(e))
        return jsonify({"error": "Internal server error"}), 500

# ------------------ GET VOTING STATUS ------------------
@voter_bp.route("/status/<aadhaar>", methods=["GET"])
def voting_status(aadhaar):
    voter = VoterModel.find_by_aadhaar(aadhaar)
    if not voter:
        return jsonify({"error": "Voter not found"}), 404
    return jsonify({"aadhaar": aadhaar, "has_voted": voter.get("has_voted", False)}), 200


# ------------------ DELETE VOTER (Optional, Admin Use) ------------------
@voter_bp.route("/delete/<aadhaar>", methods=["DELETE"])
def delete_voter(aadhaar):
    voter = VoterModel.find_by_aadhaar(aadhaar)
    if not voter:
        return jsonify({"error": "Voter not found"}), 404

    voters_collection.delete_one({"aadhaar": aadhaar})
    return jsonify({"message": "Voter deleted successfully"}), 200
