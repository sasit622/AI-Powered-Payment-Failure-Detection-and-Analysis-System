from fastapi import APIRouter
from Backend.service.speed_service import check_internet_speed

router = APIRouter(
    prefix="/agent",
    tags=["AI Failure Agent"]
)


@router.get("/internet-speed")
def internet_speed():
    return check_internet_speed()