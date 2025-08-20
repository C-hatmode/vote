from flask import Flask
from flask_cors import CORS
from config import SECRET_KEY
from flask_jwt_extended import JWTManager

# Import Blueprints
from routes.voter_routes import voter_bp
from routes.candidate_routes import candidate_bp
from routes.admin_routes import admin_bp
from routes.vote_routes import vote_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# 🔑 Flask secret key (used internally by Flask, e.g., for sessions)
app.config["SECRET_KEY"] = SECRET_KEY  

# 🔑 JWT secret key (used to sign tokens)
app.config["JWT_SECRET_KEY"] = SECRET_KEY  

# ✅ Make token never expire
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False  

# Initialize JWT
jwt = JWTManager(app)

# Register routes
app.register_blueprint(voter_bp, url_prefix="/voter")
app.register_blueprint(candidate_bp, url_prefix="/candidate")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(vote_bp, url_prefix="/vote")

@app.route("/", methods=["GET"])
def home():
    return {"message": "Blockchain Voting System API is running "}

if __name__ == "__main__":
    app.run(debug=True, port=5002)
