from pydantic import BaseModel
from typing import List
class UserResponse(BaseModel):
    exists:bool

class ResUser(BaseModel):
    category:str
    interest:str
    recom:List[str]
class FailureRequest(BaseModel):
    amount: float
    balance: float
    internet_speed: float
    authenticated: bool
    bank_status: str
    
class AnalysisRequest(BaseModel):
    user_id: int

class AgentRequest(BaseModel):
    amount: float
    balance: float
    authenticated: bool
    bank_status: str
    failure_reason: str | None = None

class PaymentRequest(BaseModel):
    amount: float
    receiver_id: int

class LoanRequest(BaseModel):
    user_id: str
    name: str