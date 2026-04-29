from passlib.context import CryptContext

# 使用纯 Python 的 pbkdf2_sha256 方案，避免 bcrypt 的平台依赖问题
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def get_hash_password(password):
    """Hash a password using pbkdf2_sha256."""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)
