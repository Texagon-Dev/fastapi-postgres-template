from fastapi import Request, Depends
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.features.auth.service import get_current_user
from fastapi.security import HTTPBearer

security = HTTPBearer(auto_error=False)

async def get_context(
    request: Request,
    db: Session = Depends(get_db),
    token = Depends(security)
):
    current_user = None
    
    if token:
        try:
            current_user = get_current_user(token.credentials, db)
        except Exception:
            pass
    
    return {
        "request": request,
        "db": db,
        "current_user": current_user
    }