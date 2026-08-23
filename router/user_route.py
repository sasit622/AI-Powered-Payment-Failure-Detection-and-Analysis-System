from fastapi import APIRouter
from myapp.service.user_service import check_user,login_user
from myapp.model.user import UserResponse
router=APIRouter()
@router.get("/users/{user_id}",response_model=UserResponse)
def get_user(id:int):
    return check_user(id)

@router.get("/login/{user_id}/{password}")
def login(user_id:str,password:str):
    return login_user(user_id,password)