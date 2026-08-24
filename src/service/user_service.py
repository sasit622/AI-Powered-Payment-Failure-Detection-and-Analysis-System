from src.repository.user_repo import get_user,get_password
def check_user(id):
    user=get_user(id)
    if user is None:
        return {
            "exists":False
        }
    return {
        "exists":True
    }

def login_user(user:str,password:str):
    auth=get_password(user,password)
    if auth is None:
        return {
            "Success":False
        }
    return {
        "Success":True,
        "id":auth.get("conversations").get("users")
    }