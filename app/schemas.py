from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional, Dict, Any

class Issue(BaseModel):
    level: str  # error или warning
    message: str

class DocumentInfo(BaseModel):
    name: str
    detected_type: str
    size_kb: float

class CheckResponse(BaseModel):
    check_id: UUID
    status: str
    status_label: str
    reason: Optional[str] = None
    issues: List[Issue]
    documents: List[DocumentInfo]
    extracted: Dict[str, Any]
    checked_at: datetime

class CheckListResponse(BaseModel):
    id: UUID
    program: str
    status: str
    doc_count: int
    created_at: datetime