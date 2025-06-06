from pydantic import BaseModel
from typing import Optional, Any, List, Dict

class FeatureOut(BaseModel):
    properties: Dict[str, Any]

    class Config:
        from_attributes = True
