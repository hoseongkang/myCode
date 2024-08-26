import os

def get_current_user_info():
    username = os.getenv('USERNAME')
    domain = os.getenv('USERDOMAIN')
    full_username = os.getenv('USERDOMAIN') + '\\' + os.getenv('USERNAME')
    return {
        'username': username,
        'domain': domain,
        'full_username': full_username,
    }


user_info = get_current_user_info()
print(user_info['username'])