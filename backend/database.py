import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from pymongo import MongoClient
from pymongo.collection import Collection

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "nonprofit_db")

_client: Optional[MongoClient] = None
_db = None


def get_db():
    global _client, _db
    if _db is not None:
        return _db
    _client = MongoClient(DATABASE_URL)
    _db = _client[DATABASE_NAME]
    return _db


def collection(name: str) -> Collection:
    return get_db()[name]


def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    col = collection(collection_name)
    now = datetime.utcnow()
    doc = {**data, "created_at": now, "updated_at": now}
    result = col.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc


def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
    col = collection(collection_name)
    cursor = col.find(filter_dict or {}).sort("created_at", -1).limit(limit)
    items: List[Dict[str, Any]] = []
    for d in cursor:
        d["_id"] = str(d.get("_id"))
        items.append(d)
    return items
