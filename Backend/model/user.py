from pydantic import BaseModel
from typing import List
class UserResponse(BaseModel):
    exists:bool

class ResUser(BaseModel):
    category:str
    interest:str
    recom:List[str]
