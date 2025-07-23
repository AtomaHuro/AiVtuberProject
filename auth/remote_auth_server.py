# 🔐 Remote Authentication Microservice (Twitch + YouTube Mod Verification)
import requests
from flask import Flask, request, jsonify, redirect
from urllib.parse import urlencode
import os
import threading

app = Flask(__name__)
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_SECRET = os.getenv("TWITCH_SECRET")
YT_API_KEY = os.getenv("YOUTUBE_API_KEY")
REDIRECT_URI = "http://localhost:7543/callback"
verified_users = set()

def simulate_test_login():
    verified_users.add("TEST_MOD_USER_ID")
    print("[TEST] ✅ Test mod user added: TEST_MOD_USER_ID")

@app.route("/auth")
def auth_entry():
    params = {
        "client_id": TWITCH_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "moderation:read chat:read"
    }
    return redirect("https://id.twitch.tv/oauth2/authorize?" + urlencode(params))

@app.route("/callback")
def auth_callback():
    code = request.args.get("code")
    token_res = requests.post("https://id.twitch.tv/oauth2/token", params={
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }).json()
    access_token = token_res.get("access_token")

    headers = {"Authorization": f"Bearer {access_token}", "Client-ID": TWITCH_CLIENT_ID}
    user_data = requests.get("https://api.twitch.tv/helix/users", headers=headers).json()
    user_id = user_data['data'][0]['id']

    # Verify if user is a mod (stubbed logic - replace with actual checks)
    if user_id:
        verified_users.add(user_id)
        return f"✅ Authenticated: {user_data['data'][0]['display_name']}"
    return "❌ Failed to verify."

@app.route("/verify", methods=["POST"])
def verify():
    user = request.json.get("user_id")
    if user in verified_users:
        return jsonify({"authorized": True})
    return jsonify({"authorized": False})

def start_auth_server():
    simulate_test_login()  # Allow testing with fallback ID
    app.run(port=7543)

if __name__ == '__main__':
    threading.Thread(target=start_auth_server).start()
