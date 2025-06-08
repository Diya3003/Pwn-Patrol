import hashlib
import requests

def calculate(password_pwned_count):
    if password_pwned_count == 0:
        return 0
    elif password_pwned_count < 10:
        return 1
    elif password_pwned_count < 200:
        return 2
    elif password_pwned_count < 3000:
        return 3
    else:
        return 4

def check_password_pwned(password: str) -> int:
    # Hash password using SHA-1 (uppercase hex digest)
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    # Query HIBP Pwned Passwords API with prefix
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if response.status_code != 200:
        raise RuntimeError(f"Error fetching data: {response.status_code}")

    # Parse response and look for suffix match
    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return int(count)  # Number of times password appeared in breaches

    return 0  # Not found (not pwned)

