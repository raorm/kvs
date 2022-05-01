import os
import secrets

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import httpx

app = FastAPI()

security = HTTPBasic()
auth_user = os.getenv("ADMIN_USERNAME", None)
auth_password = os.getenv("ADMIN_PASSWORD", None)
auth_required = os.getenv("AUTH_REQUIRED", "false").lower() in ["true", "t"]

routes = {}

N_SHARDS = 3

def get_admin_username(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    if not auth_required:
        return "guestuser"
    correct_username = secrets.compare_digest(credentials.username, auth_user)
    correct_password = secrets.compare_digest(credentials.password, auth_password)
    if auth_required and not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"}
        )
    return credentials.username

# Assume there are n shards
def simple_hash(key: str):
    return hash(key) % N_SHARDS

@app.get("/get")
def get(key: str, username: str = Depends(get_admin_username)):
    if len(key) == 0:
        raise HTTPException(status_code=400, detail="Key must not be empty")
    shard_numb = simple_hash(key)
    url = f"http://shard{shard_numb}.default:8000/get"
    params = {'key': key}
    r = httpx.get(url, params=params)
    return r.json()['message']

class KeyValuePair(BaseModel):
    key: str
    value: str

@app.post("/set")
def set(kvpair: KeyValuePair, username: str = Depends(get_admin_username)):
    if len(kvpair.key) == 0:
        raise HTTPException(status_code=400, detail="Key must not be empty")
    if len(kvpair.value) == 0:
        raise HTTPException(status_code=400, detail="Value must not be empty")
    shard_numb = simple_hash(kvpair.key)
    url = f"http://shard{shard_numb}.default:8000/set"
    r = httpx.get(url, params={'key': kvpair.key, 'value': kvpair.value})
    return r.json()

@app.get("/exists")
def exists(key: str, username: str = Depends(get_admin_username)):
    if len(key) == 0:
        raise HTTPException(status_code=400, detail="Key must not be empty")
    shard_numb = simple_hash(key)
    url = f"http://shard{shard_numb}.default:8000/exists"
    params = {'key': key}
    r = httpx.get(url, params=params)
    return r.json()['message']
