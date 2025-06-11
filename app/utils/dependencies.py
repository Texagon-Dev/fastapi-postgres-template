from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated

from app.utils.database import get_db
from app.models.user import User
from app.features.auth.service import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def get_current_user_dependency(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    return get_current_user(token, db)

# Common dependencies that can be used across all features
CurrentUser = Annotated[User, Depends(get_current_user_dependency)]
DbSession = Annotated[Session, Depends(get_db)]