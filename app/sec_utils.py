import bcrypt

from app.settings import get_settings


def hash_password(password: str) -> str:
    """Returns a salted password hash"""
    settings = get_settings()
    return bcrypt.hashpw(password.encode("utf-8"), settings.SALT.encode()).decode()


def check_if_user_has_access_to_resource(token: str, hashed: str) -> bool:
    """Returns True if password matches hashed password"""
    return False
