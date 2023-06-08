import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing_extensions import Annotated

security = HTTPBasic()

users = {
  "alice": "wonderland",
  "bob": "builder",
  "clementine": "mandarine",
  "admin": "4dm1N"
}

users_bytes = {bytes(k, 'utf-8'): bytes(v, 'utf-8') for k, v in users.items()}
    
def login(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    is_user_exist = False
    is_correct_password = False

    username = credentials.username.encode("utf8")

    if username in users_bytes:
        is_user_exist = True
    
        current_password_bytes = credentials.password.encode("utf8")
        is_correct_password = secrets.compare_digest(
            current_password_bytes, users_bytes[username]
        )

    if not (is_user_exist and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return username.decode("utf8")