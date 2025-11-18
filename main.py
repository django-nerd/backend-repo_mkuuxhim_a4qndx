from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from schemas import DonationPledge, ContactMessage, Story, VolunteerApplication
from database import db, create_document, get_documents

app = FastAPI(title="ChildHope API", version="1.0.0")

# CORS (allow all for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    message: str


@app.get("/", response_model=HealthResponse)
async def root():
    return {"status": "ok", "message": "ChildHope backend is running"}


@app.get("/api/hello")
async def hello():
    return {"message": "Hello from ChildHope API"}


@app.get("/test")
async def test():
    state = {
        "backend": "ok",
        "database": "connected" if db is not None else "not_configured",
    }
    # Try a harmless DB op if available
    if db is not None:
        try:
            db["__heartbeat__"].insert_one({"at": "ping"})
            state["db_write"] = "ok"
        except Exception as e:
            state["db_write"] = f"error: {e}" 
    return state


# Utilities

def serialize_doc(doc):
    if not doc:
        return doc
    d = dict(doc)
    _id = d.get("_id")
    if isinstance(_id, ObjectId):
        d["_id"] = str(_id)
    # Convert datetimes to isoformat if needed
    for k, v in list(d.items()):
        try:
            import datetime
            if isinstance(v, (datetime.datetime, datetime.date)):
                d[k] = v.isoformat()
        except Exception:
            pass
    return d


@app.post("/api/pledge")
async def create_pledge(payload: DonationPledge):
    try:
        inserted_id = create_document("donationpledge", payload)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/contact")
async def create_contact(payload: ContactMessage):
    try:
        inserted_id = create_document("contactmessage", payload)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/volunteer")
async def create_volunteer(payload: VolunteerApplication):
    try:
        inserted_id = create_document("volunteerapplication", payload)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stories")
async def list_stories(limit: Optional[int] = 6):
    # If DB configured, read from collection; otherwise return demo data
    try:
        if db is not None:
            docs = get_documents("story", {}, limit=limit)
            return [serialize_doc(d) for d in docs]
    except Exception:
        # fall back to demo data on any db error
        pass

    demo: List[dict] = [
        {
            "title": "Asha's First Day Back",
            "summary": "After months away, Asha returned to school with a backpack full of supplies and a heart full of hope.",
            "image_url": "https://images.unsplash.com/photo-1511988617509-a57c8a288659?q=80&w=1600&auto=format&fit=crop",
        },
        {
            "title": "Meals that Matter",
            "summary": "Your support funded 200 weekly meal kits for families in our community.",
            "image_url": "https://images.unsplash.com/photo-1472162072942-cd5147eb3902?q=80&w=1600&auto=format&fit=crop",
        },
        {
            "title": "Safe Spaces After School",
            "summary": "Children gather at our hubs to learn, play, and find mentors who believe in them.",
            "image_url": "https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=1600&auto=format&fit=crop",
        },
    ]
    return demo[: limit or 6]


# Optional: expose schemas for admin tools
@app.get("/schema")
async def get_schema_info():
    return {
        "collections": [
            "donationpledge",
            "contactmessage",
            "volunteerapplication",
            "story",
        ]
    }


# Run with: uvicorn main:app --reload
