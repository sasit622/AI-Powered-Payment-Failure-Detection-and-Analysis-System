import json

with open("Backend/data/data.json", "r") as file:
    data = json.load(file)


def get_user(user_id):
    return data["user"].get(str(user_id))


def save_data():
    with open("Backend/data/data.json", "w") as file:
        json.dump(data, file, indent=4)
def get_password(data, id, password):
    user = data["user"].get(str(id))

    if user is None:
        return False

    return str(user.get("pass")) == str(password)