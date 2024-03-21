from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
# pwd_context = CryptContext(schemes=["argon2"], argon2__memory_cost=65536, argon2__time_cost=3, argon2__parallelism=4, argon2__variant="id")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)