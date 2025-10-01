# # app/utils/security.py
# from datetime import datetime, timedelta
# from typing import Optional
# from jose import JWTError, jwt
# import os

# # try to import configuration from app.config; fall back to env / sensible defaults
# try:
#     from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
# except Exception:
#     SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")  # replace in production
#     ALGORITHM = os.getenv("ALGORITHM", "HS256")
#     ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
#     to_encode = {"sub": subject}
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# def decode_access_token(token: str) -> Optional[str]:
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         subject: str = payload.get("sub")
#         return subject
#     except JWTError:
#         return None

from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

