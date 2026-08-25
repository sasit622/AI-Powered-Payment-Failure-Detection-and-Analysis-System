from fastapi import APIRouter, HTTPException

from Backend import session
from Backend.repository.user_repo import get_user
from Backend.service.user_service import analyze_user_transactions


router = APIRouter(
    prefix="/agent",
    tags=["AI Failure Agent"]
)


@router.post("/analyaia_agent")
def analyze_user():

    # Check authentication
    if session.current_sender_id is None:
        raise HTTPException(
            status_code=401,
            detail="Please authenticate first"
        )

    # Get authenticated user
    user = get_user(session.current_sender_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Analyze this user's transactions
    return analyze_user_transactions(
        session.current_sender_id,
        user
    )