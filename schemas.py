"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Example schemas (you can keep these for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# App-specific schemas for the non-profit organization

class DonationPledge(BaseModel):
    """Donation pledges made by supporters"""
    name: str = Field(..., min_length=2)
    email: EmailStr
    amount: float = Field(..., gt=0)
    message: Optional[str] = Field(None, max_length=500)

class ContactMessage(BaseModel):
    """General contact or volunteer interest submissions"""
    name: str = Field(..., min_length=2)
    email: EmailStr
    subject: str = Field(..., min_length=3, max_length=120)
    message: str = Field(..., min_length=5, max_length=1000)

class Story(BaseModel):
    """Impact stories displayed on the website"""
    title: str = Field(..., min_length=3, max_length=120)
    summary: str = Field(..., min_length=10, max_length=400)
    image_url: Optional[str] = Field(None, description="Public image URL")

class VolunteerApplication(BaseModel):
    """Volunteer sign-ups"""
    name: str = Field(..., min_length=2)
    email: EmailStr
    skills: Optional[str] = Field(None, max_length=200)
    availability: Optional[str] = Field(None, max_length=120)

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
