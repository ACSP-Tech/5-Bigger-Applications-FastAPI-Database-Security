from passlib.context import CryptContext

SECRET_KEY = "HGHJKJJJJJJJJ435LK3241"

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")