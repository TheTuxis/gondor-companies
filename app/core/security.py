from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import settings

bearer_scheme = HTTPBearer()


class CurrentUser(BaseModel):
    user_id: int
    company_id: int
    email: str | None = None
    roles: list[str] = []


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> CurrentUser:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user_id = payload.get("user_id")
    company_id = payload.get("company_id")
    if user_id is None or company_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token claims")

    return CurrentUser(
        user_id=user_id,
        company_id=company_id,
        email=payload.get("email"),
        roles=payload.get("roles", []),
    )
