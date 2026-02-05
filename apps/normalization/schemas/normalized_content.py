from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ValidationError

class ContentSchema(BaseModel):
    title: str
    price: float
    currency: str
    category: str

class MetadataSchema(BaseModel):
    ingested_at: datetime

class NormalizedContentSchema(BaseModel):
    source: str
    external_id: Optional[str]
    content: ContentSchema
    metadata: MetadataSchema