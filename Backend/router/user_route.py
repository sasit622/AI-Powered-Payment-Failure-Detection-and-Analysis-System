#from fastapi import APIRouter,Body
#from Backend.service.user_service import check_user,login_user
#from Backend.model.user import UserResponse
#from Backend.service.user_query import query_response
#router=APIRouter()
#@router.get("/users/{user_id}",response_model=UserResponse)
##   return check_user(id)

#router.get("/login/{user_id}/{password}")
#def login(user_id:str,password:str):
 #   return login_user(user_id,password)

#@router.post("/QueryParameter")
#def query_api(query: str = Body(..., media_type="text/plain")):
 #   return query_response(query)