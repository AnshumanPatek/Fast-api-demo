from typing import Optional, Dict, List
from pydantic import BaseModel, Field   


class MsgPayload(BaseModel):
    msg_id: Optional[int] = None
    msg_name: str
    content: Optional[str] = None
    is_active: bool = True

    class Config:
        schema_extra = {
            "example": {
                "msg_name": "Welcome",
                "content": "Welcome to FastAPI CRUD application",
                "is_active": True
            }
        }


class MsgResponse(BaseModel):
    success: bool
    data: Optional[Dict] = None
    message: str
