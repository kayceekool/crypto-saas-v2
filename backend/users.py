from database import users

def create_user(email):

    users[email] = {
        "email": email,
        "plan": "free",
        "portfolio": [],
        "api_keys": {}
    }

    return users[email]