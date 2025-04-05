import hmac
import hashlib
import base64

def hash_password(password: str, secret_key: str) -> str:
    """
    Hash a password using HMAC with HS256.

    Args:
        password (str): The password to hash.
        secret_key (str): The secret key used for hashing.

    Returns:
        str: The hashed password in base64 format.
    """
    hashed = hmac.new(secret_key.encode(), password.encode(), hashlib.sha256)
    return base64.b64encode(hashed.digest()).decode()

if __name__ == "__main__":
    # Example usage
    password = "secret"
    secret_key = "71352f5d937040fd91d29fa00379f4f5f2926bbd4ea981172ff3f71d460a8639"
    hashed_password = hash_password(password, secret_key)
    print(f"Hashed Password: {hashed_password}")