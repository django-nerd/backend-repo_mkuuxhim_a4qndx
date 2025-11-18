from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, HttpUrl


class DonationPledge(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    amount: float = Field(..., gt=0)
    message: Optional[str] = Field(None, max_length=500)


class ContactMessage(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    subject: str = Field(..., min_length=1, max_length=150)
    message: str = Field(..., min_length=1, max_length=2000)


class VolunteerApplication(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=30)
    interest_area: Optional[str] = Field(None, max_length=120)
    availability: Optional[str] = Field(None, max_length=120)
    message: Optional[str] = Field(None, max_length=1000)


class Story(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    summary: str = Field(..., min_length=1, max_length=600)
    image_url: Optional[HttpUrl] = None
    published_at: Optional[datetime] = None
