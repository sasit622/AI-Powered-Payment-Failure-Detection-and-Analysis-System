from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Backend.model.user import AgentRequest, AnalysisRequest, PaymentRequest, LoanRequest
from Backend import session
from Backend.service.agent_service import analyze_error
from Backend.service.user_service import analyze_user_transactions
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



@router.post("/check-loan")
def check_loan(request: LoanRequest):

    user = get_user(request.user_id)

    if user is None:
        return {
            "status": "failed",
            "message": "User ID not found"
        }

    if user["name"].lower() != request.name.lower():
        return {
            "status": "failed",
            "message": "User ID and name do not match"
        }

    loan = user.get("Loan", {})

    if loan.get("status", "").lower() == "yes":
        return {
            "status": "success",
            "has_loan": True,
            "loan_amount": loan.get("amount"),
            "due_date": loan.get("due_date")
        }

    return {
        "status": "success",
        "has_loan": False,
        "message": "You do not have an active loan"
    }

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
def analyze(request: AnalysisRequest):

    # Check authentication
    if session.current_sender_id is None:
        raise HTTPException(
            status_code=401,
            detail="Please authenticate first"
        )

    from Backend.repository.user_repo import get_user
    user = get_user(session.current_sender_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return analyze_user_transactions(
        session.current_sender_id,
        user
    )