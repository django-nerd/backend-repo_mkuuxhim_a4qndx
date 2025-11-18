import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

from database import create_document, get_documents
from schemas import DonationPledge, ContactMessage, Story, VolunteerApplication

app = FastAPI(title="ChildHope API", description="Backend for the ChildHope organisation website")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "ChildHope backend is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from ChildHope backend!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = getattr(db, 'name', None) or ("✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set")
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# Public endpoints used by the website

@app.post("/api/pledge")
def create_pledge(payload: DonationPledge) -> Dict[str, str]:
    try:
        doc_id = create_document("donationpledge", payload)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contact")
def create_contact(payload: ContactMessage) -> Dict[str, str]:
    try:
        doc_id = create_document("contactmessage", payload)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/volunteer")
def create_volunteer(payload: VolunteerApplication) -> Dict[str, str]:
    try:
        doc_id = create_document("volunteerapplication", payload)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stories")
def list_stories(limit: int = 6) -> List[Dict[str, Any]]:
    try:
        docs = get_documents("story", {}, limit)
        # Normalize ObjectId and timestamps to strings for frontend safety
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])  # type: ignore
            for key in ("created_at", "updated_at"):
                if key in d:
                    d[key] = str(d[key])
        return docs
    except Exception as e:
        # Return a friendly fallback with sample stories if DB missing
        return [
            {
                "_id": "demo-1",
                "title": "A backpack of dreams",
                "summary": "Your support helped Aisha get back to school with supplies and mentorship.",
                "image_url": "https://images.unsplash.com/photo-1600880292089-90e7e86ec5e1?q=80&w=1200&auto=format&fit=crop"
            },
            {
                "_id": "demo-2",
                "title": "From street to classroom",
                "summary": "Rahul found a safe classroom and hot meals through our outreach program.",
                "image_url": "https://images.unsplash.com/photo-1529158062015-cad636e205a0?q=80&w=1200&auto=format&fit=crop"
            },
            {
                "_id": "demo-3",
                "title": "Community library opens",
                "summary": "A new reading room now serves 120 children every week.",
                "image_url": "https://images.unsplash.com/photo-1519681393784-d120267933ba?q=80&w=1200&auto=format&fit=crop"
            }
        ]

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
