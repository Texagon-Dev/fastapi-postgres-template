from .graphql.types.user import UserCreateInput
from app.models.user import User, UserRole
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .schema import TokenResponse
from fastapi.security import OAuth2PasswordBearer
from app.utils.security import hash_password, verify_password, create_access_token, verify_access_token
from typing import Union
from app.utils.permissions import ROLE_PERMISSIONS, has_permission, Permission
from typing import Dict, Any, List, Optional
import uuid
import hashlib
from datetime import timedelta, datetime, timezone

def get_user_by_id(db: Session, user_id: uuid.UUID) -> Optional[User]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

def authenticate_user(db: Session, email: str, password: str) -> Union[User, bool]:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return False
    return user

def create_user_service(db: Session, user_input: UserCreateInput):
    existing_user = db.query(User).filter(User.email == user_input.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "invalid data",
                "errors": {
                    "email": ["email already exists"]
                }
            }
        )
    
    # Check password match here since we don't have Pydantic validation
    if user_input.password != user_input.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "invalid data",
                "errors": {
                    "password": ["passwords do not match"]
                }
            }
        )
    
    user_data = {
        "first_name": user_input.first_name,
        "last_name": user_input.last_name,
        "email": user_input.email,
        "role": user_input.role,
        "is_active": user_input.is_active,
        "password_hash": hash_password(user_input.password)
    }
    
    role_mapping = {
        "admin": UserRole.ADMIN,
        "manager": UserRole.MANAGER,
        "employee": UserRole.EMPLOYEE
    }
    user_data["role"] = role_mapping[user_data["role"]]
    
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login_service(db: Session, email: str, password: str) -> TokenResponse:
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return TokenResponse(access_token=access_token, token_type="bearer")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def get_current_user(token: str, db: Session) -> User:
    payload = verify_access_token(token)

    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email = payload.get("sub")
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def update_user_service(
    db: Session, 
    current_user: User, 
    user_id: uuid.UUID, 
    update_data: Dict[str, Any]
) -> User:
    
    user_to_update = db.query(User).filter(User.id == user_id).first()
    if not user_to_update:
        raise ValueError("User not found")
    
    is_self_update = current_user.id == user_id
    can_update_others = has_permission(current_user, Permission.UPDATE_USER)  # Role-based check
    
    if not (is_self_update or can_update_others):
        raise ValueError("Insufficient permissions: Cannot update this user")
    
    if 'email' in update_data and update_data['email']:
        existing_user = db.query(User).filter(
            User.email == update_data['email'],
            User.id != user_id
        ).first()
        
        if existing_user:
            raise ValueError(f"Email '{update_data['email']}' is already in use")
    
    # Permission matrix: which roles can update which fields
    field_permissions = {
        'first_name': {'self': True, 'update_user_permission': True},
        'last_name': {'self': True, 'update_user_permission': True},
        'email': {'self': True, 'update_user_permission': True},
        'role': {'self': False, 'update_user_permission': True},  # Only users with UPDATE_USER permission
        'is_active': {'self': False, 'update_user_permission': True}  # Only users with UPDATE_USER permission
    }
    
    for field, value in update_data.items():
        if value is None:
            continue
            
        field_perms = field_permissions.get(field, {'self': False, 'update_user_permission': False})
        
        can_update_field = (
            (field_perms['self'] and is_self_update) or
            (field_perms['update_user_permission'] and can_update_others)
        )
        
        if not can_update_field:
            raise ValueError(f"Insufficient permissions to update field: {field}")
        
        if field == 'role' and isinstance(value, str):
            role_mapping = {
                "admin": UserRole.ADMIN,
                "manager": UserRole.MANAGER, 
                "employee": UserRole.EMPLOYEE
            }
            user_to_update.role = role_mapping.get(value, user_to_update.role)
        elif hasattr(user_to_update, field):
            setattr(user_to_update, field, value)
    
    try:
        db.commit()
        db.refresh(user_to_update)
        return user_to_update
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to update user: {str(e)}")
    

def get_user_permissions_service(current_user: User) -> List[str]:
    if not current_user:
        return []
    
    user_permissions = ROLE_PERMISSIONS.get(current_user.role, [])
    return [permission.value for permission in user_permissions]

def change_password_service(
    db: Session, 
    current_user: User, 
    old_password: str, 
    new_password: str
) -> User:
    
    if not verify_password(old_password, current_user.password_hash):
        raise ValueError("Old password is incorrect")

    current_user.password_hash = hash_password(new_password)
    
    try:
        db.commit()
        db.refresh(current_user)
        return current_user
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to change password: {str(e)}")
    
async def create_password_reset_token_service(db: Session, email: str) -> Optional[str]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    
    token_data = {
        "id": str(user.id),
        "sub": user.email,
        "type": "password_reset"
    }

    token = create_access_token(token_data, expires_delta=timedelta(minutes=30))
    
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    user.last_password_reset_token_hash = token_hash
    
    db.add(user)
    db.commit()
    
    return user, token

async def verify_password_reset_service(db: Session, token: str) -> Optional[User]:
    payload = verify_access_token(token)
    if not payload:
        return False
    if payload.get("type") != "password_reset":
        return False
    
    user_id = uuid.UUID(payload.get("id"))
    user = get_user_by_id(db, user_id)

    if not user:
        return False
    if payload.get("sub") != user.email:
        return False
    
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    if user.last_password_reset_token_hash != token_hash:
        return False
    
    return user

async def reset_password_service(db: Session, token: str, new_password: str) -> bool:
    user = await verify_password_reset_service(db, token)
    if not user:
        return False

    user.password_hash = hash_password(new_password)
    user.last_password_reset_token_hash = None
    user.last_password_reset_at = datetime.now(timezone.utc)
    db.add(user)
    db.commit()
    return True