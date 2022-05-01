from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

data = {}

@app.get("/get")
def get(key: str):
    if key in data:
        return {"message": f"{data[key]}"}
    else:
        return {"message": f"Key {key} not found"}

class KeyValuePair(BaseModel):
    key: str
    value: str

@app.get("/set")
def set(key: str, value: str):
    data[key] = value
    return {"message": f"Value set for {key}"}

@app.get("/exists")
def exists(key: str):
    if key in data:
        return {"message": f"Key {key} exists"}
    else:
        return {"message": f"Key {key} does not exist"}