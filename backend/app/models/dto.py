from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict, ValidationError, field_validator
from typing import Optional
from dataclasses import dataclass


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str = ""

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthUser(BaseModel):
    # Accept input dicts that have "user_id" (from CSV/repo) but expose it as "id"
    id: int = Field(validation_alias="user_id")
    email: EmailStr
    name: str
    role: str
    # pydantic v2 config: allow extra keys (e.g., picture/contact_*) and support ORM style if needed
    model_config = ConfigDict(from_attributes=True, extra="ignore")


# -------- Items --------

class ItemCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    name: str
    category: str
    available: bool = True
    description: Optional[str] = ""

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    available: Optional[bool] = None
    description: Optional[str] = None

class ItemOut(BaseModel):
    id: int
    sku: str
    name: str
    category: str
    available: bool
    description: str
    model_config = ConfigDict(from_attributes=True)

class SearchQuery(BaseModel):
    q: Optional[str] = None
    category: Optional[str] = None
    available: Optional[bool] = None
    page: int = 1
    size: int = 10


# -------- Profile --------

class ContactInfo(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    @field_validator("phone")
    def phone_length(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if len(v) < 7 or len(v) > 15:
            raise ValueError("Invalid phone number length")
        return v


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    picture: Optional[str] = None
    contact: Optional[ContactInfo] = None



# -------- Export --------

class ExportSelectionRequest(BaseModel):
    ids: List[int] = Field(default_factory=list)

class ExportPayload(BaseModel):
    count: int
    items: List[ItemOut]


class AuthUser(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    # internal name: user_id, JSON key: "id"
    user_id: int = Field(alias="id")
    email: str
    name: str
    role: str