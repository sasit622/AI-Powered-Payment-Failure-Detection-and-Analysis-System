from fastapi import APIRouter
from pydantic import BaseModel
from Backend.model.user import AgentRequest,PaymentRequest
from Backend import session
from Backend.service.agent_service import analyze_error
router = APIRouter(
    prefix="/agent",
    tags=["AI Failure Agent"]
)

from Backend.repository.user_repo import get_user

current_sender_id = None


@router.post("/authenticate")
def authenticate_user(user_id: int, password: str):

    global current_sender_id

    user = get_user(user_id)

    if user is None:
        current_sender_id = None

        return {
            "authenticated": False,
            "reason": "user_not_found"
        }

    if str(user["pass"]) != str(password):
        current_sender_id = None

        return {
            "authenticated": False,
            "reason": "invalid_password"
        }

    # Store authenticated sender
    current_sender_id = user_id
    session.current_sender_id = user_id

    return {
        "authenticated": True,
        "user_id": user_id,
        "message": "Authentication successful"
    }

class PaymentRequest(BaseModel):
    amount: float
    receiver_id: int


@router.post("/pay")
def pay(request: PaymentRequest):

    global current_sender_id

    if current_sender_id is None:
        return {
            "status": "failed",
            "error": "not_authenticated",
            "message": "Please authenticate before making a payment."
        }

    return analyze_error(
        sender_id=current_sender_id,
        amount=request.amount,
        receiver_id=request.receiver_id
    )

@router.post("/analyze")
def analyze(request: AgentRequest):

    return analyze_error(
        amount=request.amount,
        balance=request.balance,
        authenticated=request.authenticated,
        bank_status=request.bank_status,
        failure_reason=request.failure_reason
    )