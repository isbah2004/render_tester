from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os

app = FastAPI()


load_dotenv()

app = FastAPI()

@app.get("/config")
def read_config():
    return {
        "app_name": os.getenv("APP_NAME"),
        "environment": os.getenv("APP_ENV"),
        "port": os.getenv("APP_PORT"),
        "database": {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "name": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
        }
    }

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

# In-memory mock data
items = []

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the Test FastAPI app!"}

# Get all items
@app.get("/items")
def get_items():
    return items

# Get item by ID
@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}

# Create a new item
@app.post("/items")
def create_item(item: Item):
    items.append(item.dict())
    return {"message": "Item added successfully", "item": item}

# Update item by ID
@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: Item):
    for idx, item in enumerate(items):
        if item["id"] == item_id:
            items[idx] = updated_item.dict()
            return {"message": "Item updated successfully", "item": updated_item}
    return {"error": "Item not found"}

# Delete item by ID
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for idx, item in enumerate(items):
        if item["id"] == item_id:
            deleted = items.pop(idx)
            return {"message": "Item deleted", "item": deleted}
    return {"error": "Item not found"}
