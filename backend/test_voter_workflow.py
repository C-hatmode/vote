import requests

BASE_URL = "http://127.0.0.1:5002"  # adjust if your Flask runs on another port

def test_voter_workflow():
    aadhaar = "123456789012"  # test voter Aadhaar
    password = "test1234"

    # 1. Login
    print("\n--- Voter Login ---")
    login_res = requests.post(f"{BASE_URL}/voter/login", json={
        "aadhaar": aadhaar,
        "password": password
    })
    print("Login Response:", login_res.json())

    # 2. Get candidates from voter's location
    print("\n--- Fetch Candidates for Voter's Region ---")
    candidates_res = requests.get(f"{BASE_URL}/voter/candidates/{aadhaar}")
    candidates_data = candidates_res.json()
    print("Candidates Response:", candidates_data)

    if "candidates" not in candidates_data or not candidates_data["candidates"]:
        print("❌ No candidates found for this region. Add some candidates first.")
        return

    # pick the first candidate in the region
    valid_candidate = candidates_data["candidates"][0]["_id"]

    # 3. Try to vote for a candidate outside region (simulate using fake id)
    print("\n--- Try Voting Outside Region ---")
    fake_candidate_id = "68a068acd9c661b53d8c2c4e"  # replace with a real candidate id from another region in DB
    wrong_vote_res = requests.post(f"{BASE_URL}/voter/vote", json={
        "aadhaar": aadhaar,
        "candidate_id": fake_candidate_id
    })
    print("Outside Region Vote Response:", wrong_vote_res.json())

    # 4. Vote for valid candidate (same region)
    print("\n--- Cast Valid Vote ---")
    vote_res = requests.post(f"{BASE_URL}/voter/vote", json={
        "aadhaar": aadhaar,
        "candidate_id": valid_candidate
    })
    print("Vote Response:", vote_res.json())

    # 5. Fetch voter details after vote
    print("\n--- Voter Details After Vote ---")
    voter_res = requests.get(f"{BASE_URL}/voter/aadhaar/{aadhaar}")
    print("Voter Details:", voter_res.json())


if __name__ == "__main__":
    test_voter_workflow()
