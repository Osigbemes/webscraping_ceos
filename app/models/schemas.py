from pydantic import BaseModel
from typing import List

class CEORequest(BaseModel):
    ceo_name: str
    nicknames: List[str]
    company: str
