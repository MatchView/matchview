import json
import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for now — in production, restrict this to your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the profile schema
class Profile(BaseModel):
    name: str
    surname: str
    gender: str
    province: str
    email: str = ""

# File path for profiles.json
PROFILE_FILE = "profiles.json"

# Function to load profiles
def load_profiles():
    if not os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "w") as f:
            json.dump({}, f)  # create empty JSON object
    with open(PROFILE_FILE, "r") as f:
        return json.load(f)

# Function to save profiles
def save_profiles(data):
    with open(PROFILE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Endpoint to get a profile by unique code
@app.get("/profile/{code}")
async def get_profile(code: str):
    data = load_profiles()
    if code in data:
        return data[code]
    return {"error": "Profile not found"}, 404

# Endpoint to save a profile linked to a unique code
@app.post("/profile/{code}")
async def save_profile(code: str, profile: Profile):
    data = load_profiles()
    data[code] = profile.dict()
    save_profiles(data)
    return {"message": "Profile saved successfully"}
