from fastapi import APIRouter
from src.service.speed_service import check_internet_speed

router = APIRouter()


@router.get("/internet-speed")
def internet_speed():
    return check_internet_speed()