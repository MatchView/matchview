from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# CORS setup so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

profile_file = "profiles.json"

# Initialize file if it doesn't exist
if not os.path.exists(profile_file):
    with open(profile_file, "w") as f:
        json.dump({}, f)

def load_profiles():
    with open(profile_file, "r") as f:
        return json.load(f)

def save_profiles(data):
    with open(profile_file, "w") as f:
        json.dump(data, f, indent=4)

@app.get("/profile/{code}")
def get_profile(code: str):
    profiles = load_profiles()
    if code in profiles:
        return profiles[code]
    else:
        raise HTTPException(status_code=404, detail="Profile not found")

@app.post("/profile/{code}")
def save_profile(code: str, profile: dict):
    profiles = load_profiles()
    profiles[code] = profile
    save_profiles(profiles)
    return {"message": "Profile saved successfully"}
