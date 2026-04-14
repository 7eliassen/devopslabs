from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import secrets
import string

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/generate-password")
def generate_password(length: int = 16, include_special: bool = True):
    length = max(8, min(128, length))
    
    chars = string.ascii_letters + string.digits
    if include_special:
        chars += string.punctuation
    
    password = ''.join(secrets.choice(chars) for _ in range(length))
    return {"password": password}
