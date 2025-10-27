from pydantic import BaseModel, Field
from typing import Optional, List

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
    class Config:
        from_attributes = True

class ExportSelectionRequest(BaseModel):
    ids: List[int] = Field(default_factory=list)

class ExportPayload(BaseModel):
    count: int
    items: List[ItemOut]

