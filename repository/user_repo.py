import json
def get_user(id):
    with open("data/data.json") as f:
        data=json.load(f)
    return data["user"].get(str(id))
def get_password(id,password):
    with open("data/data.json") as f:
        data=json.load(f)
    return data["user"].get(str(id)).get("pass")==password