from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List
from datetime import datetime

from schemas import DonationPledge, ContactMessage, VolunteerApplication, Story
from database import create_document, get_documents

app = FastAPI(title="ChildHope API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_root() -> Dict[str, Any]:
    return {"status": "ok", "service": "backend"}


@app.get("/api/hello")
def hello() -> Dict[str, str]:
    return {"message": "Hello from ChildHope backend"}


@app.get("/test")
def test_status() -> Dict[str, Any]:
    try:
        # Try reading stories; if collection missing it's fine
        stories = get_documents("story", limit=1)
        return {"backend": "ok", "database": "ok", "stories_sample": stories}
    except Exception as e:
        return {"backend": "ok", "database": f"error: {e}"}


@app.post("/api/pledge")
def submit_pledge(payload: DonationPledge) -> Dict[str, Any]:
    try:
        saved = create_document("donationpledge", payload.dict())
        return {"ok": True, "pledge_id": saved.get("_id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/contact")
def submit_contact(payload: ContactMessage) -> Dict[str, Any]:
    try:
        saved = create_document("contactmessage", payload.dict())
        return {"ok": True, "contact_id": saved.get("_id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/volunteer")
def submit_volunteer(payload: VolunteerApplication) -> Dict[str, Any]:
    try:
        saved = create_document("volunteerapplication", payload.dict())
        return {"ok": True, "volunteer_id": saved.get("_id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stories", response_model=List[Story])
def get_stories() -> List[Story]:
    try:
        items = get_documents("story", limit=12)
        if items:
            # Map to pydantic model
            return [Story(**{k: v for k, v in i.items() if k != "_id"}) for i in items]
    except Exception:
        # Fallback to demo data if DB not available
        pass

    demo: List[Story] = [
        Story(
            title="Asha's First Day Back",
            summary="After months out of school, Asha joined our bridge class and is thriving.",
            image_url="https://images.unsplash.com/photo-1604881987921-3bf2d01fa4b5?q=80&w=1600&auto=format&fit=crop",
            published_at=datetime.utcnow(),
        ),
        Story(
            title="Meals that Matter",
            summary="Your support served 4,500 nutritious lunches last month.",
            image_url="https://images.unsplash.com/photo-1564053489984-317bbd824340?q=80&w=1600&auto=format&fit=crop",
            published_at=datetime.utcnow(),
        ),
        Story(
            title="Safe Spaces",
            summary="Our community hubs offer counselling and creativity for kids.",
            image_url="https://images.unsplash.com/photo-1542810634-71277d95dcbb?q=80&w=1600&auto=format&fit=crop",
            published_at=datetime.utcnow(),
        ),
    ]
    return demo
